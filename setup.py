import codecs
import os.path
import re
# import sys

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(HERE, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


SETUP_OPTIONS = dict(
    name='scplint',
    version=find_version('scplint', '__init__.py'),
    author='Richard Zimmermann',
    author_email='scplint@ganzokay.de',
    description='Lint your AWS Service Control Policies (SCPs)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='link to github',
    packages=find_packages(exclude=['tests']),
    package_data={'scplint': ['data/*.txt', 'models/*.json']},
    include_package_data=True,
    license=open('LICENSE.txt').read(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Operation System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: German'
    ],
    # py_modules=['src/scplint'],
    package_dir={'scplint': 'scplint'},
    install_requires=open('requirements.txt').read().splitlines(),
    scripts=['bin/scplint', 'bin/scplint.bat'])

# if 'py2exe' in sys.argv:
#     import py2exe
#     SETUP_OPTIONS['options'] = {
#         'py2exe': {
#             'optimize': 0,
#             'skip_archive': True,
#             'packages': ['scplint']
#         }
#     }

#     SETUP_OPTIONS['console'] = ['scplint']

setup(**SETUP_OPTIONS)
