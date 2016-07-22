from setuptools import setup

setup(name='sorta',
      version='0.1',
      description='A tool to tidy your files',
      url='http://github.com/loics2/sorta',
      author='Loic Stankovic',
      author_email='loicstankovic@hotmail.com',
      license='GNUv3',
      packages=['sorta'],
      install_requires=[
          'Click',
      ],
      entry_points='''
          [console_scripts]
          sorta=sorta.sorta:cli
      ''',
      zip_safe=False)
