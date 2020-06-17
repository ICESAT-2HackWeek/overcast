from pathlib import Path
import pandas as pd
import warnings

def fn2rgt(filename):
    '''
    Extract rgt and cycle_number from IS2 ATL0x data standard filename.
    
    Parameters:
    ----------
    filename: full path with standard filename (including NSIDC processed) 
    
    return:
    ------
    rgt: reference ground track number (int)
    cyc: cycle number
    '''
    sfn = Path(filename).name
    wrds = sfn.split('_')
    irgt = 3 if wrds[0]=='processed' else 2
    rgttxt = wrds[irgt]
    rgt = int(rgttxt[:4])
    cyc = int(rgttxt[4:6])
    return rgt,cyc

def datainfo(fns):
    '''
    Generate a pandas dataframe containing the RGT, cycle number, and filename of data
    
    Parameters:
    ----------
    fns: a list of filename with full path to the data files
    
    Return: a pandas dataframe with RGT, cycle_number, and filename as columns    
    '''
    rgts = []
    cycs = []
    for fn in fns:
        rgt,cyc = fn2rgt(fn)
        rgts.append(rgt)
        cycs.append(cyc)
    return pd.DataFrame({'rgt':rgts,'cycle_number':cycs,'filename':fns})

def query_rgt(rgt,cyc,dat_df):
    '''
    Find filename of the granule matching the specified RGT and cycle number. 
    
    Parameters:
    ----------
    rgt: RGT number of the granule
    cyc: cycle number of the granule
    dat_df: a pandas dataframe with RGT, cycle_number, and filename as columns    
    
    Return: a list of filenames that match the rgt and cycle number
    '''
    new_df = dat_df[ (dat_df['rgt']==rgt) & (dat_df['cycle_number']==cyc) ]
    return new_df.filename.values

def box_sel(dat,bbox):
    lonmin,latmin,lonmax,latmax = bbox
    region = (dat.lats>latmin)&(dat.lats<latmax)&(dat.lons>lonmin)&(dat.lons<lonmax)
    return region
