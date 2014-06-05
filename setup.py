import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'outbound'))
import version

long_description = '''
Josh should write this
'''

setup(
    name='outbound-python',
    version=version.VERSION,
    url='https://github.com/outboundio/lib-python',
    author='Travis Beauvais',
    author_email='travis@outbound.io',
    maintainer='Outbound.io',
    maintainer_email='support@segment.io',
    packages=['outbound'],
    license='MIT License',
    install_requires=[
        'requests',
    ],
    description='Josh should write this as well',
    long_description=long_description
)
