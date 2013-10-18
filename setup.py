import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='anderssontree',
    version='0.1.0',
    author='Darko Poljak',
    author_email='darko.poljak@gmail.com',
    description='Package provides Andersson Tree implementation in pure Python.',
    license="GPLv3",
    keywords=['AA Tree', 'Andersson Tree'],
    url='https://github.com/darko-poljak/anderssontree',
    download_url='https://github.com/darko-poljak/anderssontree',
    packages=['anderssontree'],
    long_description=read('README.rst'),
    platforms="OS Independent",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
