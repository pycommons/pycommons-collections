"""PyCommons Lang namespace."""
from __future__ import annotations

from importlib_metadata import PackageNotFoundError, version

__author__ = "Shashank Sharma"
__email__ = "shashankrnr32@gmail.com"

# Used to automatically set version number from GitHub actions
# as well as not break when being tested locally
try:
    __version__ = version(__package__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"
