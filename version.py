#!/usr/bin/env python

"""Manages versions via git tags.

Usage:
    version current
    version inc (major | minor | patch)

"""
from sh import git, ErrorReturnCode, ErrorReturnCode_128
from docopt import docopt
import sys
from semantic_version import Version


def parse_version_str(ver_str):
    first = ver_str[0]
    rest = ver_str[1:]
    if ver_str[0] != "v":
        raise Exception("""Invalid version. First character should be a v
            got {} instead.""".format(first))

    return Version(rest.strip())


def get_versions():
    version_lines = git("tag", "-l").split("\n")
    version_lines = filter(lambda x: len(x) > 0, version_lines)
    version_lines = filter(lambda x: x[0] == 'v', version_lines)

    if len(version_lines) == 0:
        return []

    return map(parse_version_str, version_lines)


def latest(versions):
    return sorted(versions)[-1]


def inc_major(version):
    v = Version(str(version))
    v.major = version.major + 1
    v.minor = 0
    v.patch = 0
    return v


def inc_minor(version):
    v = Version(str(version))
    v.minor = v.minor + 1
    v.patch = 0
    return v


def inc_patch(version):
    v = Version(str(version))
    v.patch = v.patch + 1
    return v


def version_to_str(version):
    return "v" + str(version)


def init_versioning():
    git("tag", "v0.0.0", "-a")


def sub_command_current(latest_version):
    print version_to_str(latest_version)
    sys.exit()


def sub_command_inc(latest_version, args):
    new_version = None
    if(args['major']):
        new_version = inc_major(latest_version)
    elif(args['minor']):
        new_version = inc_minor(latest_version)
    elif(args['patch']):
        new_version = inc_patch(latest_version)

    try:
        git("tag", version_to_str(new_version), "-a")
        sys.exit(0)
    except ErrorReturnCode_128:
        print "Version increment aborted with empty message."


if __name__ == '__main__':
    args = docopt(__doc__)

    try:
        versions = get_versions()
    except ErrorReturnCode as e:
        print e.stderr
        sys.exit(1)

    if len(versions) == 0:
        print "No sem version tags found. Will init with v0.0.0"
        print "Leave an empty message to cancel."
        try:
            init_versioning()
            print "Version initializied."
        except ErrorReturnCode_128:
            print "Version init aborted with empty message."
    else:
        latest_version = latest(versions)

        if args['current']:
            sub_command_current(latest_version)
        elif args['inc']:
            sub_command_inc(latest_version, args)
