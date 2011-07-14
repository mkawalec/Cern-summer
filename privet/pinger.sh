#!/bin/bash

for i in {230..300}
do
    ping lxplus${i}.cern.ch -c 1
done
