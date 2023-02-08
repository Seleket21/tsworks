#!/bin/bash

filename=$1
while read line; do
	wget "https://query1.finance.yahoo.com/v7/finance/download/${line}?period1=1644302441&period2=1675838441&interval=1d&events=history&includeAdjustedClose=true"
done < $filename
