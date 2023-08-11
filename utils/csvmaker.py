import netCDF4 as nc
import os
os.chdir("C:/Users/hj/ERA5")
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import xarray as xr
from config.ncconfig import ncconfig, slice_config

def make_csv(nc_path, csv_path):
    ds = xr.open_dataset(nc_path)
    months = np.array(ds.time.values).astype("datetime64[M]")
    dic = {month:ds["count"].values[i].flatten() for i, month in enumerate(months)}
    lon1d = ncconfig.lon1d
    lat1d = ncconfig.lat1d
    df = pd.DataFrame(data={"lat":lat1d,"lon":lon1d})
    df2 = pd.DataFrame(data=dic)
    df2 = df2.applymap(lambda x: np.nan if x<0 else x)
    # df2 columns are datetime64[M]
    # make format to datetime64[M] (1901-01-01 00:00:00) to (1901-Jan)
    df2.columns = df2.columns.map(lambda x: x.strftime("%Y-%b"))
    df3 = pd.concat([df,df2],axis=1)
    df3.to_csv(csv_path,index=False)
