#!/bin/bash

cd output
compare-histos *.aida
../paida.py
make-plots --png *.dat
gpicview *.png
