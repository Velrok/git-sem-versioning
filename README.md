# git-sem-versioning

A very tiny python tool, that lets you easily increment and tag the current version (major, minor or patch).

# usage

See: `version -h`

# dependencies

- git
- python 2.7
	- [docopt](http://docopt.org/)
	- [sh](http://amoffat.github.com/sh/)

# install

```
cd <some-local-dir>
git clone git@github.com:Velrok/git-sem-versioning.git
ln -s git-sem-versioning/version.py /usr/local/bin/version
```