from mcp_colima.tools.lifecycle import normalize_profile


def test_normalize_profile_defaults_to_default():
    assert normalize_profile(None) == "default"
    assert normalize_profile("") == "default"
    assert normalize_profile("foo") == "foo"
