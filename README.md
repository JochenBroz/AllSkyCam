# AllSkyCam

Code to operate an AllSkyCam based on Raspberry Pi using a Raspberry Pi High Quality Camera

## Installation

1. Checkout repository to working location.

2. build virtual environment with the dependencies
```
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

3. Start a jupyter notebook server for working remotely.
```
jupyter notebook --no-browser --port=8889 --ip=0.0.0.0
```

Now one can access http://pi3b:8889/tree?

