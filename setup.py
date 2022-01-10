import setuptools 

setuptools.setup(
    name='xarrayfrac',
    version='0.0.1',
    url='https://github.com/',
    author='Ben Leighton',
    author_email='benplei@gmail.com',
    description='mandelbrot dynamically generated xarray backend',
    install_requires=[            # I get to this in a second
          'xarray',
          'dask',
          'distributed',
          'numpy',
      ],
    entry_points={
        "xarray.backends": ["xarrayfrac=xarrayfrac.frac_backend:DynamicMandelbrotEntrypoint"],
    },
)