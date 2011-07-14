#!/bin/bash

compare-histos output/*.aida
./paida.py
make-plots --png output/*.dat
gpicview output/*.png
