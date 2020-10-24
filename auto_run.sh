#!/bin/bash

#running automatically some tests saving the output on a file

model="VGG16"
count=1
image_size=224

for (( epochs=5; epochs<=20; epochs+=5)) do
	for ((batch_size=8; batch_size<=32; batch_size+=8)) do
		#for ((image_size=150;image_size<=250;image_size+=50)) do
		  file="Train_${epochs}${batch_size}${image_size}"
			echo "============================================================" >>$file
			echo "Testing on epoch: $epochs;batch_size: $batch_size; image_size: $image_size" >>$file

			python main.py -m $model -d DATASET1/realdataset_PREPROCESSED -b $batch_size -i ${image_size}x3 -e $epochs >>$file

			echo "********Test $count Ended********" >> $file
			((count++))
		#done
	done
done
