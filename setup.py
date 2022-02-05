import setuptools 
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='xarrayfrac',
    version='0.0.6',
    url='https://github.com/benjaminleighton/xarrayfrac',
    author='Ben Leighton',
    author_email='benplei@gmail.com',
    description='mandelbrot dynamically generated xarray backend',
    packages=['xarrayfrac'],
    long_description = long_description,
    long_description_content_type="text/markdown",
    install_requires=[
          'xarray',
          'dask',
          'distributed',
          'numpy>=1.21.5',
      ],
    entry_points={
        "xarray.backends": ["xarrayfrac=xarrayfrac.frac_backend:DynamicMandelbrotEntrypoint"],
    },
)
