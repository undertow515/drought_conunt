import numpy as np
import pandas as pd
from datetime import datetime
import netCDF4 as nc
from dataclasses import dataclass
import xarray as xr

sample = xr.open_dataset("c:/Users/hj/ERA5/cru_ts4.06.1901.2021.pet.dat.nc")
class slice_config:
    start1, end1 = '1901-01-01', '1933-12-31'
    start2, end2 = '1934-01-01', '1966-12-31'
    start3, end3 = '1967-01-01', '2021-12-31'
    slice1 = slice(start1, end1)
    slice2 = slice(start2, end2)
    slice3 = slice(start3, end3)
    time_series1 = sample.sel(time=slice1).time.values
    time_series2 = sample.sel(time=slice2).time.values
    time_series3 = sample.sel(time=slice3).time.values
    time_series = [time_series1, time_series2, time_series3]

@dataclass
class ncconfig:
    # Define dimensions
    lat = sample.variables['lat'][:]
    lon = sample.variables['lon'][:]
    month1_unit = 'months since '+slice_config.start1
    month2_unit = 'months since '+slice_config.start2
    month3_unit = 'months since '+slice_config.start3

    months1 = pd.date_range(slice_config.start1, slice_config.end1, freq='M')
    months1 = list(map(lambda x: x.strftime('%Y-%m'), months1))
    months1 = list(map(lambda x: datetime.strptime(x, '%Y-%m'), months1))
    
    months1 = nc.date2num(months1, month1_unit, calendar='360_day', has_year_zero=True)
    months2 = pd.date_range(slice_config.start2, slice_config.end2, freq='M')
    months2 = list(map(lambda x: x.strftime('%Y-%m'), months2))
    months2 = list(map(lambda x: datetime.strptime(x, '%Y-%m'), months2))
    months2 = nc.date2num(months2, month2_unit, calendar='360_day', has_year_zero=True)
    months3 = pd.date_range(slice_config.start3, slice_config.end3, freq='M')
    months3 = list(map(lambda x: x.strftime('%Y-%m'), months3))
    months3 = list(map(lambda x: datetime.strptime(x, '%Y-%m'), months3))
    months3 = nc.date2num(months3, month3_unit, calendar='360_day', has_year_zero=True)
    months = [months1, months2, months3]

    # make mesh grid of lat and lon
    mesh_lon, mesh_lat = np.meshgrid(lon, lat)
    # make 1d array of lat and lon
    lon1d = mesh_lon.flatten()
    lat1d = mesh_lat.flatten()

@dataclass
class pathconfig:
    pass





