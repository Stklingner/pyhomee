from setuptools import setup, find_packages

setup(name='pyhomee',
      version='0.0.2',
      description='Access Homee Websocket API',
      url='http://github.com/Stklingner/pyhomee',
      author='Timo Wendt',
      license='MIT',
      install_requires=['websocket-client>=0.54.0', 'requests'],
      packages=find_packages(),
      zip_safe=True)
