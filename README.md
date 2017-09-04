# git_bump_version
This is a simple tool for automated versioning with Git. It assumes you follows a versioning scheme branch_prefix&lt;major.minor&gt; and use git tags in "&lt;version_prefix&gt;&lt;major&gt;.&lt;minor&gt;.&lt;build&gt;" scheme for releases. For instance say my branch structure looks something like this:

```
* release/1.0
release/2.0
release/3.0
```

While currently on release/1.0 with the latest tag being 1.0.5. If you run `git_bump_version`, it will tag the local and remote HEAD commit with `1.0.6` as well as output `1.0.6` to stdout. Alternatively, you can run `git_bump_version --dont_tag` to just output `1.0.6` and perform the tag yourself. The default branch prefix is "release/" and the default version prefix is empty though these can be customized via command line options.

## Install
Installs like a regular PyPI package.
- Simply run in your cloned directory: `python setup.py` OR
- Grab the latest version from the public PyPI: `pip install git-bump-version`

## Develop
This is a command line tool so development is pretty straight forward.

## Test
The additional test requirements are `nose` and `mock` which can both be installed with `pip`. After installing these packages, simply run `nosetests` in the directory where you cloned this repo and it will run the tests.
