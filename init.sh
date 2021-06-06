#!/bin/bash

pip install -r requierements.txt
& ./flask/Scripts/Activate.ps1

$env:FLASK_APP = "application.py"
$env:FLASK_DEBUG = 1
$env:FLASK_ENV = "development"

flask run -h 192.168.0.106