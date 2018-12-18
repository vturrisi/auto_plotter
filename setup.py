from setuptools import setup

with open('requirements.txt') as f:
      requirements = [p.strip() for p in f.readlines()]

setup(name='auto_plotter',
      version='0.1.0',
      description='Simple auto plotting library to provide cool looking graphs',
      url='https://github.com/vturrisi/auto_plotter',
      author='Victor Turrisi',
      license='MIT',
      packages=['auto_plotter'],
      install_requires=requirements,
      include_package_data=True,
      zip_safe=False)