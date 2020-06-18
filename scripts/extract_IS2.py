import numpy as np
import xarray as xr
import pandas as pd
from pathlib import Path
import h5py
from astropy.time import Time

from overcast import readers as rd
from overcast.utils import fn2rgt, datainfo, query_rgt, box_sel

ROI = 'BEAUFORT'
prd = 'ATL07'
beam = 'gt2l'
#prd = 'ATL09'
#beam = 'profile_2'
dataroot = Path.home()/'shared/data-overcast'/ROI
outroot  = Path.home()/'shared/data-overcast'/ROI/'subset'
outdir = outroot/prd/beam
outdir.mkdir(parents=True,exist_ok=True)
fns = sorted( (dataroot/prd).glob('*.h5') )


for fn in fns:
    print(fn)
    with h5py.File(fn, 'r') as f:
        epoch=f['/ancillary_data/atlas_sdp_gps_epoch'][0]
        if prd=='ATL07':
            dat = rd.getATL07(f,beam)
            dat = dat.to_xarray()
            dat = dat.swap_dims({'index':'dt'})
            dat = dat.drop('index')
        elif prd=='ATL09':
            dat = rd.getATL09(f,beam)
    if 'dt' in dat.keys(): 
        dat['time']=(['dt'],Time(epoch+dat['dt'],format='gps').utc.datetime)
        ofn = outdir/fn.name.replace('processed','subset') 
        dat.to_netcdf(ofn.with_suffix('.nc'))
