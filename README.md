# git_bump_version
This is a simple tool for automated versioning with Git for semantic versioning (major.minor.part). You simply specify the major and minor versions and it either increments the part if a major.minor version already existed otherwise creates major.minor.0.

## Install
- Simply run in your cloned directory: `pip install .` OR
- Grab the latest version from the public PyPI: `pip install git-bump-version`

## Develop
This is a command line tool so development is pretty straight forward.

## Test
The additional test requirements are `nose` and `mock` which can both be installed with `pip`. After installing these packages, simply run `nosetests` in the directory where you cloned this repo and it will run the tests.

