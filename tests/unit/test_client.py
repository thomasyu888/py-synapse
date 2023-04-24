"""Test client"""
from unittest.mock import patch, Mock

import pytest
import requests  # type: ignore

from synapse import client
from synapse.exceptions import (
    SynapseBadRequestError,
)
from synapse.constants import (
    CONTENT_TYPE_HEADER,
    JSON_CONTENT_TYPE,
)
from synapse.client import _handle_response, _generate_request_url


def test__handle_response_error():
    """Test handling response error"""
    response = requests.Response()
    with patch.object(
        client,
        "check_status_code_and_raise_error",
        side_effect=SynapseBadRequestError(),
    ) as mock_check_status_func, pytest.raises(SynapseBadRequestError):
        _handle_response(response)
        mock_check_status_func.assert_called_once_with(response)


def test__handle_response_none_content_type():
    """Test handling response content type"""
    response = Mock(requests.Response)
    response.headers = {}
    response.text = "some text"
    with patch.object(
        client, "check_status_code_and_raise_error"
    ) as mock_check_status_func:
        assert _handle_response(response) == response.text
        mock_check_status_func.assert_called_once_with(response)


def test__handle_response_with_plain_text_content_type():
    response = Mock(requests.Response)
    response.headers = {CONTENT_TYPE_HEADER: "text/plain"}
    response.text = "some text"
    with patch.object(
        client, "check_status_code_and_raise_error"
    ) as mock_check_status_func:
        assert _handle_response(response) == response.text
        mock_check_status_func.assert_called_once_with(response)


def test__handle_response_with_json_content_type():
    response = Mock(requests.Response)
    response.headers = {CONTENT_TYPE_HEADER: JSON_CONTENT_TYPE}
    json = {"result": "a"}
    with patch.object(
        client, "check_status_code_and_raise_error"
    ) as mock_check_status_func, patch.object(response, "json", return_value=json):
        assert _handle_response(response) == json
        mock_check_status_func.assert_called_once_with(response)


# _generate_request_url


def test__generate_request_url_invalid_endpoint():
    with pytest.raises(ValueError):
        _generate_request_url(None, "/entity")


def test__generate_request_url_none_path():
    with pytest.raises(ValueError):
        _generate_request_url("https://synapse.org", None)


def test__generate_request_url_invalid_path():
    with pytest.raises(ValueError):
        _generate_request_url("https://synapse.org", "http:/path.com/path")


def test__generate_request_url():
    assert (
        _generate_request_url("https://synapse.org", "/entity")
        == "https://synapse.org/entity"
    )
