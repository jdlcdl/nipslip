#!/bin/bash

for filename in `ls *.py`
do
	echo "### python3 $filename ###"
	python3 $filename
done
