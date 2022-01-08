from xarray.backends import BackendEntrypoint
from xarray.backends import BackendArray
from xarray.core import indexing
import xarray as xr
import threading
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)

class DynamicMandelbrotEntrypoint(BackendEntrypoint):
  '''
  custom xarray entrypoint / aka engine for generating
  mandelbrot fractals
  '''
  lock = threading.Lock()
  open_dataset_parameters = ['resolution']

  def open_dataset(
      self,
      filename_or_obj,
      resolution=10,
      drop_variables=None
  ):
      '''
      generates a lazy dynamically generated xarray dataset
      resolution: number of pixels in the mandelbrot dataset
      filename_or_obj: should be None, dask seems to require it
      drop_variables: should be None seems to be required 
      '''
      backend_array = MandelbrotBackendArray((resolution, resolution), np.float32, DynamicMandelbrotEntrypoint.lock)
      data = indexing.LazilyIndexedArray(backend_array)
      vars = xr.Variable(("x", "y", ), data)
      ds = xr.Dataset({"frac" : vars}, coords = {"x": backend_array.x, "y": backend_array.y})
      # not sure if setting close method is required
      ds.set_close(self.my_close_method)
      return ds
  
  def my_close_method(self):
      return

class MandelbrotBackendArray(BackendArray):
    '''
    A Mandelbrot generator as an xarray backend
    '''
    def __init__(
        self,
        shape,
        dtype,
        lock,
    ):
        self.shape = shape
        self.dtype = dtype
        self.lock = lock
        self.x = np.linspace(-2, 2, num=shape[0])
        self.y = np.linspace(-2, 2, num=shape[1])
        
    def __getitem__(
        self, key: xr.core.indexing.ExplicitIndexer
    ) -> np.typing.ArrayLike:
        return indexing.explicit_indexing_adapter(
            key,
            self.shape,
            indexing.IndexingSupport.BASIC,
            self._raw_indexing_method,
        )

    def _raw_indexing_method(self, key: tuple) -> np.typing.ArrayLike:
        logging.debug(key)
        # probably this is thread safe anyhow and this might make things
        # slower
        with self.lock:
            x = self.x[key[1]]
            y = self.y[key[0]]
            xx, yy = np.meshgrid(x, y)
            frac = self._mandel(xx, yy)
            if isinstance(key[0], slice) or isinstance(key[1], slice):
              return frac
            try:
              return frac.item()
            except ValueError:
              return frac

    def _mandel(self, xx, yy):
        # code derived from https://www.learnpythonwithrune.org/numpy-compute-mandelbrot-set-by-vectorization/
        c = yy + xx * 1j 
        z = np.zeros(c.shape, dtype=np.complex128)
        div_time = np.zeros(z.shape, dtype=int)
        m = np.full(c.shape, True, dtype=bool)
        max_iterations = 32
        for i in range(max_iterations):
            # mandelbrot formula 
            z[m] = z[m]**2 + c[m]
            # check if the value of z is greater than a threshold yet
            diverged = np.greater(np.abs(z), 2, out=np.full(c.shape, False), where=m)
            # check how many iterations have been required before threshold
            div_time[diverged] = i     
            m[np.abs(z) > 2] = False  
        return div_time # return the number of iterations required before threshold