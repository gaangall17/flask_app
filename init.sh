#!/bin/bash

& ./flask/Scripts/Activate.ps1
pip install -r requirements.txt

$env:FLASK_APP = "application.py"
$env:FLASK_DEBUG = 1
$env:FLASK_ENV = "development"

flask run -h 192.168.0.106