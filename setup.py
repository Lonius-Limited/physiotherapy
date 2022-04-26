from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in physiotherapy/__init__.py
from physiotherapy import __version__ as version

setup(
	name="physiotherapy",
	version=version,
	description="Physiotherapy customizations and Features",
	author="Zaha Consulting",
	author_email="dsmwaura@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
