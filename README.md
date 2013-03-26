# git-sem-versioning

A very tiny python tool, that lets you easily create new git tags (major, minor or patch) based on the current version.

# usage

```
Manages versions via git tags.

Usage:
    version current
    version new (major | minor | patch)
```

# dependencies

- git
- python 2.7
	- [docopt](http://docopt.org/)
	- [sh](http://amoffat.github.com/sh/)
	- [semantic_version](https://github.com/rbarrois/python-semanticversion)

for testing

- [nosetest](https://nose.readthedocs.org/en/latest/)

# install

```
cd <some-local-dir>
git clone git@github.com:Velrok/git-sem-versioning.git
ln -s git-sem-versioning/version.py /usr/local/bin/version
```