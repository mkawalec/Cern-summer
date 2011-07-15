#!/bin/bash

cd output2
compare-histos *.aida
../paida.py
make-plots --png *.dat
gpicview *.png
