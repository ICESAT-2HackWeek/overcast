#!/srv/conda/envs/notebook/bin/python
import sys
from datetime import datetime, time, date,timedelta
import os
import subprocess
import argparse
import glob
sys.path.append('/home/jovyan/overcast/modis_scripts/gibs-ml')
from gibs_layer import GIBSLayer

def build_cmd(proj_str,te_str,tr_str,xmlfile,outpath):
    cmd_list = ["gdalwarp","-overwrite","-t_srs",proj_str,"-te",te_str,"-tr",tr_str,xmlfile, outpath]
    cmd= ' '.join(cmd_list) # this makes it a single string. Different versions of subprocess.Popen seem to require 
    return cmd
def make_xml(layer_name, datestring):
    epsg='3413' # that's the input projection 
    tile_resolution='250m'
    layer = GIBSLayer.get_gibs_layer(layer_name)
    xmlfile='temp.xml'
    if layer is None:
        print("Invalid GIBS layer name")
        exit()
#  not sure if datestring is actually used here
    layer.generate_xml(protocol="tms", epsg=epsg, tile_resolution=tile_resolution, datestring=datestring)
    xml=layer.gibs_xml
    xml = xml.replace("{Time}", datestring)
    xml = xml.rstrip()  # remove all trailing whitespace
#  write output to a temporary xml file 
    with open(xmlfile, "w") as f:
        f.write(xml)       
    return xmlfile 

def run_cmd(cmd):    
    process = subprocess.Popen(cmd,shell='True',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = process.communicate()
    print(process.returncode, out,err, )
   
    # remove temporary file.. Return condition should be checked
    return process.returncode

def single_download(date):                    
#  This is the file where all the parameters need to be modified if needed. Need to put this elsewhere.
# select either True Color or Bands367
    type='TrueColor'
#type='Band367'
    layer_name='MODIS_Terra_CorrectedReflectance_'+type
# select directory where output data will be stored
    output_dir='/home/jovyan/shared/data-overcast/modis/'
#   output_dir="./"
    region='BEAUFORT'
    tile_resolution='250m'
    if not os.path.exists(output_dir):
        print("Creating directory " + output_dir)
        os.makedirs(output_dir)
# this needs to be simplified still 
    proj_str ="'+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-145 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'" 
#target extent
    te_str = '-800000 -2500000 1200000 -400000'
#target_resolution
    tr_str = '250 250'
# set up a GIBS layer used to build the input XML file 
    get_date = datetime.strptime(date, "%Y-%m-%d")
    datestring = get_date.strftime("%Y-%m-%d")
    outfile='modis.'+region+'.'+datestring.replace("-","")+ "."+type+'.tif' # needs to be changed so that the type is reflected in the name
    outpath = os.path.join(output_dir, outfile)
    print("Output will be written to: ",outpath)
    xmlfile=make_xml(layer_name,datestring)
    print(xmlfile)
    cmd=build_cmd(proj_str,te_str,tr_str,xmlfile,outpath)
    print("cmd:",cmd)
    check= run_cmd(cmd)
    
    if check == 0: 
        os.remove(xmlfile)    
    return check
    print("Done Writing File :", outpath)

    
# main program
#date="2019-06-11"
parser = argparse.ArgumentParser(description='Download MODIS data using the GIBS API')
parser.add_argument('--start_date', action='store', type=str, dest='sdate', required='True',
                    default=None,
                    help='The date from which to begin (inclusive) YYYY-MM-DD')

parser.add_argument('--end_date', action='store', type=str, dest='edate',
                    default=None,
                    help='The date from which to begin (inclusive) YYYY-MM-DD')

                    
args = parser.parse_args()
                    
sdate=args.sdate
sdate=datetime.strptime(sdate, "%Y-%m-%d")
print(sdate)
edate=args.edate
edate=datetime.strptime(edate, "%Y-%m-%d")
print(edate)
# got to check if something was specified there
date_range = [ sdate + timedelta(n) for n in range(int ((edate - sdate).days)+1)]
print(date_range)
for single_date in date_range:
    date = single_date.strftime("%Y-%m-%d")                   
    print(date)
    check= single_download(date)
