from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='agregator-mess',
    version='0.0.1',
    description='University project.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/moevm/gui-1h2018-28',
    author='MOEVM',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='vk telegram university messenger',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['vk_api', 'PyQt5', 'telethon'],
    entry_points={ 
        'console_scripts': [
            'messenger=core:main',
        ],
    },
)