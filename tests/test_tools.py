import json
import os
from pathlib import Path

import pytest

from .fixtures import auth_live, tools_live  # pylint: disable=unused-import
from .context import Tools


@pytest.mark.live
def test_validate_manifest_valid(tools_live):
    _location_ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    fp = Path(_location_) / "mock_data/manifest.json"
    result = tools_live.validate_manifest(path_or_json=fp)
    assert result == {"valid": True, "errors": []}


@pytest.mark.live
def test_validate_manifest_invalid(tools_live):
    _location_ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    fp = Path(_location_) / "mock_data/manifest.json"
    with open(fp) as src:
        mainfest_json = json.load(src)
        mainfest_json.update(
            {
                "_up42_specification_version": 1,
                "input_capabilities": {
                    "invalidtype": {"up42_standard": {"format": "GTiff"}}
                },
            }
        )
    with pytest.raises(ValueError):
        tools_live.validate_manifest(path_or_json=mainfest_json)


def test_plot_result_not_accepted_file_format_raises():
    filepaths = [Path("abc/123.hdf", "abc/123.json")]
    with pytest.raises(ValueError):
        Tools().plot_result(filepaths=filepaths)