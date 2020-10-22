#!/bin/bash

#running automatically some tests saving the output on a file

model="BASIC"
count=1
file="Test_output.txt"
for (( epochs=5; epochs<=20; epochs+=5)) do
	for ((batch_size=8; batch_size<=32; batch_size+=8)) do
		for ((image_size=150;image_size<=250;image_size+=50)) do
			echo "============================================================" >>$file
			echo "Testing on epoch: $epochs;batch_size: $batch_size; image_size: $image_size">>$file
			echo>>$file
			python main.py -m $model -d DATASET1/realdataset_PREPROCESSED -b $batch_size -i ${image_size}x1 -e $epochs >>$file 
			echo>>$file
			echo "********Test $count Ended********">>$file
			((count++))
		done
	done
done
