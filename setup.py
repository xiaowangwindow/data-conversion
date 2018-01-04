from os.path import dirname, join

from setuptools import setup, find_packages

with open(join(dirname(__file__), 'data_conversion/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='data-conversion',
    version=version,
    url='https://github.com/xiaowangwindow/data-conversion',
    description='A ETL framework to convert data',
    long_description=open('README.rst').read(),
    author='Alex Wang',
    maintainer='Alex Wang',
    maintainer_email='xiaowangwindow@163.com',
    license='BSD',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['etl = data_conversion.cmdline:main']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'motor==1.1',
        'pymongo==3.4.0',
        'typing==3.6.1',
    ]
)
