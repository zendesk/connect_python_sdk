import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'outbound'))
import version

long_description = '''
Outbound sends automated email, SMS, phone calls and push notifications based on the actions users take or do not take in your app. The Outbound API has two components:

Identify each of your users and their attributes using an identify API call.
Track the actions that each user takes in your app using a track API call.
Because every message is associated with a user (identify call) and a specific trigger action that a user took or should take (track call), Outbound is able to keep track of how each message affects user actions in your app. These calls also allow you to target campaigns and customize each message based on user data.

Example: When a user in San Francisco(user attribute) does signup(event) but does not upload a picture(event) within 2 weeks, send them an email about how they'll benefit from uploading a picture.
'''

setup(
    name='outbound',
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
    description='Outbound sends automated email, SMS, phone calls and push notifications based on the actions users take (or do not take) in your app.',
    long_description=long_description
)
