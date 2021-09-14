#!/bin/bash

read -p "which task data do you want to download? " task
if [ $task == "AS" ]
then
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1VbqB2QnBV-1bkpE_-vNw8qzouMDP7Mux' -O as_data.jsonl
elif [ $task == "D2T" ]
then
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1YMcfBmKXhkhrLRqOYQIkaCrKTc2E1jDX' -O d2t_data.jsonl
elif [ $task == "MT" ]
then
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1VecSfDjPd3Pf8eacbR3pKfD7cEnAkv7j' -O mt_data.jsonl
elif [ $task ==' IC' ]
then 
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=19QGXG7YiwvYX_dEXPg0igMF3XUtsb_cR' -O ic_data.jsonl
elif [ $task == 'QG']
then 
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1x6OqbTHclSplk7O65n29EqVGqjn6OwZZ' -O qg_data.jsonl
elif [ $task == 'DG' ]
then 
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1fjxJYXwiUtkJyJQtgO1XkkiwF6om6ULE' -O dg_data.csv
else
echo 'please use correct ids'
fi