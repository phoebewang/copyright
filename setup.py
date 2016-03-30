# setup.py:
import os
from distutils.core import setup

try:
    from pypandoc import convert
    readmd = lambda f: convert(f, 'rst')
except:
    readmd = lambda f: open(f).read()

# Allow setup.py to be run from any path.
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='copyright',
    packages=['copyright'],
    version='1.0.0.0',
    description='Add or replace license boilerplate in source code files.',
    long_description=readmd('README.md'),
    author='Remik Ziemlinski',
    author_email='first.last@gmail.com',
    license='GPLv3',
    scripts=['scripts/copyright'],
    url='https://www.github.com/rsmz/copyright',
    download_url='https://github.com/rsmz/copyright/archive/copyright-1.0.0.0.tar.gz',
)
