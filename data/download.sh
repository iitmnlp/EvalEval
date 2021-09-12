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

fi