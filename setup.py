from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()
with open('readme.rst') as f:
    description=f.read()
setup(name='confpars', version='0.1.2', author='Lior Bass', author_email='mail@liorbass.dev',
      install_requires=required, scripts=['conf_parser'], url='https://github.com/liorbass/confpars', description=description)
