"""
Module setup
"""
from setuptools import setup

setup(
    name='git_bump_version',
    packages=['git_bump_version'], # this must be the same as the name above
    use_scm_version=True,
    description='Automatically bumps version based on last tag and current branch',
    author='Nathan Grubb',
    author_email='mrnathangrubb@gmail.com',
    url='https://github.com/silent-snowman/git_bump_version',
    download_url='https://github.com/silent-snowman/git_bump_version/archive/1.0.2.tar.gz',
    keywords=['git', 'tag', 'version'],
    entry_points={
        'console_scripts' : [
            'git_bump_version = git_bump_version.__init__:main'
        ]},
    install_requires=[
        'GitPython',
    ],
)
