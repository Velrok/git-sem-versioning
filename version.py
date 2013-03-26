#!/usr/bin/env python

"""Manages versions via git tags.

Usage:
    version current
    version new (major | minor | patch)

"""
from sh import git, ErrorReturnCode, ErrorReturnCode_128
from docopt import docopt
import sys


def parse_version_str(ver_str):
    first = ver_str[0]
    rest = ver_str[1:]
    if ver_str[0] != "v":
        raise Exception("""Invalid version. First character should be a v
            got {} instead.""".format(first))

    return map(int, rest.strip().split("."))


def get_versions():
    version_lines = git("tag", "-l").split("\n")
    version_lines = filter(lambda x: len(x) > 0, version_lines)

    if len(version_lines) == 0:
        return []

    return map(parse_version_str, version_lines)


def latest(versions):
    return sorted(versions)[-1]


def inc_major(version):
    major, minor, patch = version
    return (major + 1, 0, 0)


def inc_minor(version):
    major, minor, patch = version
    return (major, minor + 1, 0)


def inc_patch(version):
    major, minor, patch = version
    return (major, minor, patch + 1)


def version_to_str(version):
    return "v" + ".".join(map(str, version))


def init_versioning():
    git("tag", "v0.0.0", "-a")


if __name__ == '__main__':
    args = docopt(__doc__)

    try:
        versions = get_versions()
    except ErrorReturnCode as e:
        print e.stderr
        sys.exit(1)

    if len(versions) == 0:
        print "No tags found. Will init with v0.0.0"
        print "Leave an empty message to cancel."
        try:
            init_versioning()
            print "Version initializied."
        except ErrorReturnCode_128:
            print "Version init aborted with empty message."
    else:
        latest_version = latest(versions)

        if(args['current']):
            print version_to_str(latest_version)
            sys.exit()

        new_version = None
        if(args['major']):
            new_version = inc_major(latest_version)
        elif(args['minor']):
            new_version = inc_minor(latest_version)
        elif(args['patch']):
            new_version = inc_patch(latest_version)

        try:
            git("tag", version_to_str(new_version), "-a")
        except ErrorReturnCode_128:
            print "Version increment aborted with empty message."
