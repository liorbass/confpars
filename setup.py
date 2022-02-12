from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()
setup(name='confpars', version='0.1.0', author='Lior Bass', author_email='mail@liorbass.dev',
      install_requires=required, scripts=['conf_parser'])
