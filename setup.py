from numpy.distutils.core import setup


setup(name='auto_plotter',
      version='1.0',
      description='auto_plotter',
      url='https://github.com/vturrisi/auto_plotter',
      author='Victor Turrisi',
      license='MIT',
      packages=['auto_plotter'],
      install_requires=[p.strip() for p in open('requirements.txt').readlines()],
      include_package_data=True,
      zip_safe=False)