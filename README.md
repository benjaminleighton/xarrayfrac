![pypi version](https://badge.fury.io/py/xarrayfrac.svg)
# xarrayfrac

A dynamic generative mandelbrot custom backend for xarray

```
pip install xarrayfrac
```

```
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt

# request a 10 billion pixel lazy xarray fractal
ds = xr.open_dataset(None, engine="xarrayfrac", resolution=100000, chunks={"x": 2000, "y": 2000})
# sample 1 in every 10000 pixels
sampled = ds.frac.isel(x=slice(0, 100000, 100), y=slice(0, 100000, 100))
# compute and display
plt.imshow(sampled)
```
![mandelbrot fractal in xarray](https://raw.githubusercontent.com/benjaminleighton/xarray_frac/main/frac1.png)

```
# request a 10 billion pixel lazy xarray fractal
ds = xr.open_dataset(None, engine="xarrayfrac", resolution=100000, chunks={"x": 2000, "y": 2000})
# zoom 
window = ds.sel(x=slice(-0.1, 0.1), y=slice(0.9, 1.0))
# plot every hundredth pixel of the window
plt.imshow(window.frac[::10, ::10])
```

![zoomed mandelbrot fractal in xarray](https://raw.githubusercontent.com/benjaminleighton/xarray_frac/main/frac2.png)
