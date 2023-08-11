# Define dimensions
import netCDF4 as nc
from netCDF4 import Dataset
import os
os.chdir("C:/Users/hj/ERA5")
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from config.ncconfig import ncconfig, slice_config
import xarray as xr

lat = ncconfig.lat
lon = ncconfig.lon
months = ncconfig.months

# Create dataset
# rootgrp = Dataset("test.nc", "w", format="NETCDF4")

def count_drought(nc_path, slice):
    pet = xr.open_dataset(nc_path).sel(time=slice)
    months = pet.time.values.astype("datetime64[M]")
    arr = np.zeros((len(months), pet.lat.shape[0], pet.lon.shape[0]))
    for i, pet in enumerate(pet.pet.values):
        arr2 = np.array([1 if x < -2 else 0 for x in pet.flatten()])
        arr[i] = arr2.reshape(pet.shape[0], pet.shape[1])
        # filter arr with nan values
        arr[i] = np.where(np.isnan(pet), np.nan, arr[i])
    return arr

def count_drought2(nc_path, slice):
    pet = xr.open_dataset(nc_path).sel(time=slice)
    months = pet.time.values.astype("datetime64[M]")
    arr = np.zeros((len(months), pet.lat.shape[0], pet.lon.shape[0]))
    for i, pet in enumerate(pet.pet.values):
        arr2 = np.array([1 if ((x < -1.5) & (x > -2)) else 0 for x in pet.flatten()])
        arr[i] = arr2.reshape(pet.shape[0], pet.shape[1])
        # filter arr with nan values
        arr[i] = np.where(np.isnan(pet), np.nan, arr[i])
    return arr


def create_dataset(path, month, month_unit, nc_path, slice, func):
    with Dataset(path, "w", format="NETCDF4") as rootgrp:
        rootgrp.createDimension("time", len(month))
        rootgrp.createDimension("lat", len(ncconfig.lat))
        rootgrp.createDimension("lon", len(ncconfig.lon))

        # Create variables
        times = rootgrp.createVariable("time", "i4", ("time",))
        lats = rootgrp.createVariable("lat", "f4", ("lat",))
        lons = rootgrp.createVariable("lon", "f4", ("lon",))
        count = rootgrp.createVariable("count", "f4", ("time", "lat", "lon",))
        # Add attributes
        rootgrp.description = "Drought data"
        lats[:] = ncconfig.lat.values
        lons[:] = ncconfig.lon.values
        times[:] = month
        count.units = "float"
        count.description = "Drought data"
        count[:] = func(nc_path, slice)
        times.units = month_unit
        times.calendar = "360_day"

