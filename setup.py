# -*- coding: utf-8 -*-
#!/usr/bin/python                        
##################################################
# AUTHOR : Yandi LI
# CREATED_AT : 2015-11-13
# LAST_MODIFIED : 2015-12-06 20:57:25
# USAGE : python setup.py
# PURPOSE : TODO
##################################################
from __future__ import absolute_import
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='webpageValidator',
      version='0.1',
      description='Tools for ',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='webpage',
      url='',
      author='Yandi LI',
      author_email='yandi@staff.weibo.com',
      license='MIT',
      packages=['webValidator'],
      package_data = {'webValidator': ["conf/*"]}, 
      install_requires=[
      ],
      include_package_data=False,
      zip_safe=False)


