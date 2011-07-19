#!/bin/bash

cd outputtop
compare-histos *.aida
../paida.py
make-plots --png *.dat
gpicview *.png
