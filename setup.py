try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(
	name='repirc',
	version='0.0.1',
	packages=["repirc", ],
	data_files=[
	],
	scripts=[
	],
	entry_points = {
		'console_scripts': [
			'papabot = repirc.papabot:main',                  
		],              
	},
)
