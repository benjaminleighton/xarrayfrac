# xarray_frac

A dynamic generative mandelbrot custom backend for xarray

```
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt

# request a 1 trillion pixel lazy xarray fractal
ds = xr.open_dataset(None, engine="xarray_frac", resolution=100000, chunks={"x": 2000, "y": 2000})
# sample every hundredth pixel
sampled = ds.frac.isel(x=slice(0, 100000, 100), y=slice(0, 100000, 100))
# compute and display
plt.imshow(sampled)
```

```
# request a 1 trillion pixel lazy xarray fractal
ds = xr.open_dataset(None, engine="xarray_frac", resolution=100000, chunks={"x": 2000, "y": 2000})
# zoom 
window = ds.where((ds.x > -0.1) & (ds.x < 0.1), drop=True).where((ds.y > 0.9) & (ds.y < 1.0), drop=True)
# plot every tenth pixel of the window
plt.imshow(window.frac[::10, ::10])
```
