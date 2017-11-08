#!/bin/sh
#
# Finnish Meteorological Institute / Mikko Rauhala (2015-2016)
#
# SmartMet Data Ingestion Module for SYNOP Observations for RA IV
#

URL=https://ra4-gifs.weather.gov/data/RMTN/UA/

if [ -d /smartmet ]; then
    BASE=/smartmet
else
    BASE=$HOME
fi

IN=$BASE/data/incoming/sounding
OUT=$BASE/data/gts
EDITOR=$BASE/editor/in
TMP=$BASE/tmp/data/sounding
TIMESTAMP=`date +%Y%m%d%H%M`

OUTFILE=$TMP/${TIMESTAMP}_gts_world_sounding.sqd
TMPFILE=$TMP/sounding-$$.txt

mkdir -p $TMP
mkdir -p $OUT/sounding/world/querydata

echo "URL: $URL"
echo "IN:  $IN" 
echo "OUT: $OUT" 
echo "TMP: $TMP" 
echo "OUT File: $OUTFILE"
echo "TMP File: $TMPFILE"

echo "Fetching file list..."
FILES=$(wget -nv -O - $URL | grep -oP 'href="\KU[SK][^"]+(?=")')
echo "done";

for file in $FILES
do
    if [ -s $IN/$file ]; then
      	echo -n "Cached: "
    else
	echo "$download$URL/$file" >> $TMPFILE;
	echo -n "Download: "
    fi
    echo $file
done 

if [ -s $TMPFILE ]; then
    echo "Downloading files...";
    cat $TMPFILE | xargs -n 1 -P 50 wget -nv -N --no-check-certificate -P $IN
    echo "done"
    rm -f $TMPFILE
    /smartmet/run/data/sounding/bin/dosounding.php
else
    echo "No files to download"
fi

#temp2qd -t "$IN/*" > $OUTFILE

#if [ -s $OUTFILE ]; then
#    bzip2 -k $OUTFILE
#    mv -f $OUTFILE $OUT/sounding/world/querydata/
#    mv -f ${OUTFILE}.bz2 $EDITOR
#fi

#rm -f $TMP/*.sqd*
