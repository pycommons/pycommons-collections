"""Test module for pycommons-collections."""

from pycommons.collections import __author__, __email__, __version__


def test_project_info():
    """Test __author__ value."""
    assert __author__ == "Shashank Sharma"
    assert __email__ == "shashankrnr32@gmail.com"
    assert __version__ == "0.0.0"
