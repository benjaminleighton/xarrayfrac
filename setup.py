import setuptools 

setuptools.setup(
    name='xarrayfrac',
    version='0.0.2',
    url='https://github.com/benjaminleighton/xarrayfrac',
    author='Ben Leighton',
    author_email='benplei@gmail.com',
    description='mandelbrot dynamically generated xarray backend',
    packages=['xarrayfrac'],
    long_description_content_type="text/markdown",
    install_requires=[
          'xarray',
          'dask',
          'distributed',
          'numpy',
      ],
    entry_points={
        "xarray.backends": ["xarrayfrac=xarrayfrac.frac_backend:DynamicMandelbrotEntrypoint"],
    },
)
