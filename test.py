import rioxarray 
import xarray as xr
import rasterio

dataset = xr.open_dataset("/home/diego/Downloads/risk_edp_20220316.1.nc")
print(dataset.rio.crs)