# coding: utf-8
"""
Robotframework AMQP library

https://github.com/ctradu/robotframework-amqp
"""
from setuptools import setup, find_packages
import os
from codecs import open

# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(name="robotframework-amqp",
      version="0.1",
      description="AMQP library for usage in robotframework tests",
      long_description=long_description,
      author="Costin Radu",
      license="MIT",
      py_modules=["AMQPSend"],
      zip_safe=False,
      platforms="any",
      include_package_data=True,
      install_requires=[
          "puka"
      ],
      # extras_require={"test": ["tox", "pytest"]},
      packages=find_packages(),
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7"
          "Topic :: Software Development :: Testing",
      ],
      keywords="robotframework testing amqp",
      url="https://github.com/ctradu/robotframework-amqp",
      )
