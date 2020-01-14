from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='imagesbackend',
      version='1.0',
      description='backend for an image website',
      author='Roope Niemi',
      packages=find_packages(),
      install_requires=(required),
      scripts=["run.py"]
     )