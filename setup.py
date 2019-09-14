from setuptools import setup

setup(
name='snapshotalyzer',
version='1.0',
author='venugopal reddy',
email='venugopal.129@gmail.com',
description='''lets you start,stop and list your instances with a Project tag as parameter
        list volumes and take snapshots''',
license="GPLv3+",
packages=['shotty'],
url="https://github.com/venugopal129/Snapshotalyzer-6000",
install_requires=['click','boto3'],
entry_points='''
    [console_scripts]
    shotty=shotty.shotty:cli
    '''
)
