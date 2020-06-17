#!/bin/sh
# script that retrieves MODIS images from the NASA Tile server and warps them to a Polar Projections using Gdal.
# Date and channel cominbations replaced from file WMS_TEMPLATE and provide to gdalwarp.
date=2019-06-10
# this combination is good for cloud masking
odir='/home/jovyan/shared/data-overcast/modis/'
type=Bands367
xmlfile='WMS'.${type}.${date}.'xml'
echo ${xmlfile}
cat WMS_TEMPLATE.xml | sed s/REPLACE_THIS_STRING_WITH_DATE/$date/ | sed s/REPLACE_THIS_STRING_WITH_TYPE/${type}/ > ${xmlfile}    
rm ${xmlfile}
outfile=${odir}'modis'.${date}.${type}.'250m.tif'
echo "Creating False Color: " $outfile

 gdalwarp -overwrite -t_srs '+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-145 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs' -te -800000 -2500000 1200000 -400000 -tr 250 250 $xmlfile $outfile

type=TrueColor
xmlfile='WMS'.${type}.${date}.'xml'
cat WMS_TEMPLATE.xml | sed s/REPLACE_THIS_STRING_WITH_DATE/$date/ | sed s/REPLACE_THIS_STRING_WITH_TYPE/${type}/ > ${xmlfile}    

outfile=${odir}'modis'.${date}.${type}.'250m.tif'
echo $xmlfile
echo "Creating True Color Image:" $outfile
 gdalwarp -overwrite -t_srs '+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-145 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs' -te -800000 -2500000 1200000 -400000 -tr 250 250 $xmlfile $outfile

rm ${xmlfile}