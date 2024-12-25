"""For pip install."""

import setuptools
from os import path


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(name='pyssc',
                 version="0.1.0",
                 setup_requires=['setuptools-git-versioning'],
                 description='A Python package for discovering and controlling SSC devices',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 url='https://github.com/jj-wohlgemuth/pyssc',
                 author='Jeff Chen',
                 author_email='',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 package_data={'pyssc': []},
                 install_requires=['zeroconf'],
                 platforms='any',
                 python_requires='>=3.6',
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 zip_safe=True,
                 )
