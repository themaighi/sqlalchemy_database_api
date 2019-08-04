from setuptools import setup, find_packages

setup(
	name='weather_api',
	version='0.0.1',
	packages=find_packages(),
	install_requires=['pandas',
                      'requests',
					  'sqlalchemy',
					  'sqlite3',],
	entry_points={},
	extra_require={'dev': ['flake8',]},
	)
