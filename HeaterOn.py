#!/usr/bin/python3
import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BOARD)
Signal_Pin = 16


GPIO.setup(Signal_Pin, GPIO.OUT)
print('Current state: ', GPIO.input(Signal_Pin))
GPIO.output(Signal_Pin, GPIO.HIGH)
print('New state: ', GPIO.input(Signal_Pin))
