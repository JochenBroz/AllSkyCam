#!/bin/bash
cd "$(dirname "$0")"

venv/bin/python3 getTemperature.py
venv/bin/python3 GetHeaterStatus.py
venv/bin/python3 weatherInfo.py
venv/bin/python3 filesystems.py
