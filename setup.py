import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-plus',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Container for advertiser and ab_testing models for Yektanet distributed sub-systems',
    long_description=README,
    url='https://panel.yektanet.com/',
    author='Yektanet DEVs',
    author_email='info@yektanet.com',
    install_requires=[
        'django',
        'jdatetime',
        'deprecation',
        'python-dateutil'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10.1',
        'Intended Audience :: Yektanet Team',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
