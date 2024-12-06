#!/bin/bash
ALL="bip340.py client.py constants.py mock_client.py mock.py nip01.py nip02.py nip04.py nip06.py nip09.py nip10.py nip13.py nip14.py nip19.py output.py relay.py "

for filename in $ALL
do
	echo "### python3 $filename ###"
	python3 $filename
done
