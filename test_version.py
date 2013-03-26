from nose.tools import *
from version import *


def test_parses_valid_versions():
    version = list(parse_version_str("v1.2.3"))
    eq_(version[:3], [1, 2, 3])


@raises(Exception)
def test_parse_version_enforces_v_prefix():
    parse_version_str("1.2.3")


def test_version_to_str_uses_v_prefix():
    v = parse_version_str("v1.2.3")
    eq_(version_to_str(v), "v1.2.3")


def test_latest_sorts_by_major_minor_path():
    versions = map(parse_version_str,
                   ["v0.0.1", "v2.1.0", "v2.11.0"])
    latest_version = version_to_str(latest(versions))
    eq_(latest_version, "v2.11.0")


def test_inc_major():
    v = parse_version_str("v1.0.0")
    result = version_to_str(inc_major(v))
    eq_(result, "v2.0.0")


def test_inc_major_resets_minor():
    v = parse_version_str("v1.1.0")
    result = version_to_str(inc_major(v))
    eq_(result, "v2.0.0")


def test_inc_major_resets_patch():
    v = parse_version_str("v1.1.1")
    result = version_to_str(inc_major(v))
    eq_(result, "v2.0.0")


def test_inc_minor():
    v = parse_version_str("v1.0.0")
    result = version_to_str(inc_minor(v))
    eq_(result, "v1.1.0")


def test_inc_minor_resets_patch():
    v = parse_version_str("v1.1.1")
    result = version_to_str(inc_minor(v))
    eq_(result, "v1.2.0")


def test_inc_patch():
    v = parse_version_str("v1.1.1")
    result = version_to_str(inc_patch(v))
    eq_(result, "v1.1.2")
