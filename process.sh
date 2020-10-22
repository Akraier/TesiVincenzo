#!/bin/bash

#Dividere in 3 directory Malware e Trusted
#Test 10% - Training 90%
#In trainig: Train 90% - Validation 10%




#ARGOMENTI
#$1:#dir;$2..$n+1:path;

#funzione che calcola i valori di soglia per scorrere il file in base ai parametri che le vengono passati

calc_percentage(){
#$1path;$2:%
#1)quanti files in dir?
#2)%
	if [[ "$#" = "2" ]] ; then
		cd "$1"
		files=$(ls -1 | wc -l)
		treshold=$(bc <<< "scale = 0; (($(ls -1 | wc -l) *$2)/100)")
	else
		echo "calc_percentage _path _percentage"
	fi
}

#echo "What's testing percentage?" in realtà probabilmente questa è esclusiva rispetto a training, ne basta una delle due(?)
#read test


n_arg=$1
if [[ "$#" = "$((n_arg+1))" ]]; then
	#echo
	#echo "What's training percentage?"
	#read training
	#echo "What's validation percentage?"
	#read validation
	#echo "What's destionation path?"
	#read dest_path
	#echo
	label1=malware
	label2=trusted
	training=90
	validation=10
	dest_path=/home/vincenzo/TesiVincenzo/DATASET1/realdataset_PREPROCESSED
	mkdir /home/vincenzo/TesiVincenzo/DATASET1/
	mkdir "${dest_path}"
	mkdir "${dest_path}/training"
	mkdir "${dest_path}/test"
	mkdir "${dest_path}/training/train"
	mkdir "${dest_path}/training/validation"
	#scorro i path passati come argomenti e creo Training e Test
	for arg in "${@:2:$#}"; do
		calc_percentage "$arg" $training
		#scorro i file nella directory e li sposto in training/test
		temp=1
		if grep -q "Malware" <<< "$arg"; then
			label=$label1
			mkdir  ${dest_path}/training/${label}
			mkdir  ${dest_path}/training/validation/${label}/
			mkdir  ${dest_path}/training/train/${label}/
			mkdir  ${dest_path}/test/${label}/
		elif grep -q "Trusted" <<< "$arg"; then
			label=$label2
			mkdir ${dest_path}/training/${label}
			mkdir ${dest_path}/training/validation/${label}/
			mkdir ${dest_path}/training/train/${label}/
			mkdir ${dest_path}/test/${label}/
		fi
		for filepath in "${arg}"/*.png; do
			filename=$(basename "$filepath")
			if [[ $temp -lt $treshold ]]; then
			#inizialmente in training creo malware e trusted per mantenere la label
				cp "$filepath" ${dest_path}/training/${label}/
				echo "copying $filename in $dest_path/training/$label/"
			else
				cp "$filepath" $dest_path/test/${label}/
				echo "copying $filename in $dest_path/test/${label}/"
			fi
			((temp++))
		done
	done

	for label in $label1 $label2; do
		calc_percentage "$dest_path/training/${label}" $validation
		temp=1
		for filepath in "${dest_path}/training/${label}"/*.png; do
		#devo dividere Training in train e validation partendo da /training/label
			filename=$(basename $filepath)
			if [[ $temp -lt $treshold ]]; then
				mv  "$filepath" "$dest_path/training/validation/${label}/"
				echo "copying $filename in $dest_path/training/validation/${label}/"
			else
				mv "$filepath" "$dest_path/training/train/${label}/"
				echo "copying $filename in $dest_path/training/train/${label}/"
			fi
			((temp++))
		done
		rm -r ${dest_path}/training/${label}/
	done
else
	echo "$0 #dir [path1..pathn] "
fi






