import picamera
from picamera import mmal, mmalobj, exc
from picamera.mmalobj import to_rational
import time
import exifread
import numpy as np
from io import BytesIO


MMAL_PARAMETER_ANALOG_GAIN = mmal.MMAL_PARAMETER_GROUP_CAMERA + 0x59
MMAL_PARAMETER_DIGITAL_GAIN = mmal.MMAL_PARAMETER_GROUP_CAMERA + 0x5A

def set_gain(camera, gain, value):
    """Set the analog gain of a PiCamera.
    
    camera: the picamera.PiCamera() instance you are configuring
    gain: either MMAL_PARAMETER_ANALOG_GAIN or MMAL_PARAMETER_DIGITAL_GAIN
    value: a numeric value that can be converted to a rational number.
    """
    if gain not in [MMAL_PARAMETER_ANALOG_GAIN, MMAL_PARAMETER_DIGITAL_GAIN]:
        raise ValueError("The gain parameter was not valid")
    ret = mmal.mmal_port_parameter_set_rational(camera._camera.control._port, 
                                                    gain,
                                                    to_rational(value))
    if ret == 4:
        raise exc.PiCameraMMALError(ret, "Are you running the latest version of the userland libraries? Gain setting was introduced in late 2017.")
    elif ret != 0:
        raise exc.PiCameraMMALError(ret)

        
def set_analog_gain(camera, value):
    """Set the gain of a PiCamera object to a given value."""
    set_gain(camera, MMAL_PARAMETER_ANALOG_GAIN, value)

    
def set_digital_gain(camera, value):
    """Set the digital gain of a PiCamera object to a given value."""
    set_gain(camera, MMAL_PARAMETER_DIGITAL_GAIN, value)

def wait_for_period(p):
    """sleep until time period is over"""
    t = time.time()
    st = (int(t/p)+1)*p-t
    time.sleep(st)
    
    
def strip_bayer_data(buffer):
    buffer.seek(0)
    stream = buffer.read()
    rawDataLocation = stream.find(b'BRCM')
    return BytesIO(stream[0:rawDataLocation])


def get_bayer_data_from_stream(buffer):
    # return the sensor bayer data from raspberry pi camera data stream.
    tags = exifread.process_file(buffer)
    stream = buffer.read()

    ver = {
        'RP_ov5647': 1,
        'RP_imx219': 2,
        'RP_imx477': 3
        }[tags['Image Model'].values]

    rawDataLocation = stream.find(b'BRCM')
    data = np.frombuffer(stream[rawDataLocation+2**15:],'uint8')
    # For the V1 module, the data consists of 1952 rows of 3264 bytes of data.
    # The last 8 rows of data are unused (they only exist because the maximum
    # resolution of 1944 rows is rounded up to the nearest 16).
    #
    # For the V2 module, the data consists of 2480 rows of 4128 bytes of data.
    # Each row consists of 3280 pixels of 10 bits, leading to 3280*10/8=4100 bytes.
    # There's actually 2464 rows of data, but the sensor's raw size is 2466
    # rows, rounded up to the nearest multiple of 16: 2480.
    #
    # For the HQ Camera Module, the data consists of 3040 rows of 6112 bytes.
    # Each row consists of 4056 pixels of 12 bits stored in 4056*12/8 = 6084 bytes,
    # followed by a padding of 28 bytes.
    # There's actually 3056 rows of data.
    #
    # Likewise, the last few bytes of each row are unused (why?). Here we
    # reshape the data and strip off the unused bytes.

    reshape, crop = {
        1: ((1952, 3264), (1944, 3240)),
        2: ((2480, 4128), (2464, 4100)),
        3: ((3056, 6112), (3040, 6084))
        }[ver]
    data = data.reshape(reshape)[:crop[0], :crop[1]]

    # For v1 and v2 camera:
    # Horizontally, each row consists of 10-bit values. Every four bytes are
    # the high 8-bits of four values, and the 5th byte contains the packed low
    # 2-bits of the preceding four values. In other words, the bits of the
    # values A, B, C, D and arranged like so:
    #
    #  byte 1   byte 2   byte 3   byte 4   byte 5
    # AAAAAAAA BBBBBBBB CCCCCCCC DDDDDDDD AABBCCDD
    #
    # For hq camera:
    # Horizontally, each row consists of 12-bit values. Every two bytes are
    # the high 8-bits of four values, and the 3th byte contains the packed low
    # 4-bits of the preceding two values. In other words, the bits of the
    # values A and B are arranged like so:
    #
    #  byte 1   byte 2   byte 3
    # AAAAAAAA BBBBBBBB BBBBAAAA
    #
    # Here, we convert our data into a 16-bit array, shift all values left by
    # 2-bits and unpack the low-order bits from every 5th byte in each row,
    # then remove the columns containing the packed bits

    if (ver==1) or (ver==2):
        data = data.astype(np.uint16) << 2
        for byte in range(4):
            data[:, byte::5] |= ((data[:, 4::5] >> ((4 - byte) * 2)) & 0b11)
        data = np.delete(data, np.s_[4::5], 1)
    elif ver==3:
        data = data.astype(np.uint16) << 4
        data[:, 0::3] |= ((data[:, 2::3] >> 4) & 0b1111)
        data[:, 1::3] |= ((data[:, 2::3] >> 8) & 0b1111)
        data = np.delete(data, np.s_[2::3], 1)
    return data

# Based on code copyrighted by Dave Jones, see https://picamera.readthedocs.io/en/release-1.13/license.html

#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

#Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


