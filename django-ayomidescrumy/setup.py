import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-ayomidescrumy',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description="A simple Django app that returns 'welcome to django'",
    long_description=README,
    url='http://3.143.112.43:8000/ayomidescrumy/',
    author='Ayomide Bakre',
    author_email='ayomidebakre@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: X.Y',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python ::3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WW/HTTP',
        'Topic :: Internet :: WW/HTTP :: Dynamic Content',
    ],
)

