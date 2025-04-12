#!/bin/bash
export DISPLAY=:0
export XAUTHORITY=$HOME/.Xauthority
exec /usr/lib/guideos_privacy_wizard/guideos_privacy_wizard.py
