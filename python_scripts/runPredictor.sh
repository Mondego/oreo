#!/bin/bash
start_port="${1:-9900}"
end_port="${2:-9903}"
echo "*****************************************************"
echo "running for ports ranging from $start_port to $end_port"
echo "*****************************************************"


for i in $(seq $start_port 1 $end_port)
do
  python Predictor.py $i > out_$i &
done
