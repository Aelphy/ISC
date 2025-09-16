from setuptools import find_packages, setup

setup(
    author='Oleg Ponomarev',
    author_email='onponomarev@gmail.com',
    license='BSD',
    test_suite='nose.collector',
    tests_require=['nose'],
    packages=find_packages(exclude=['test', 'test.*']),
    name='csvtools',
    version='0.1',
    scripts=['bin/csvpp'],

)
