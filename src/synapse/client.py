from abc import ABC

# from dataclasses import dataclass
from typing import Optional, Union
import urllib.parse as urllib_parse

import requests  # type: ignore

from synapse import __version__
from synapse.constants import (
    # SYNAPSE_DEFAULT_FILE_ENDPOINT,
    SYNAPSE_DEFAULT_REPO_ENDPOINT,
    CONTENT_TYPE_HEADER,
    JSON_CONTENT_TYPE,
)
from synapse.exceptions import check_status_code_and_raise_error


def _generate_request_url(server_url: str, endpoint_path: str) -> str:
    """Generate the URL for the HTTP request

    Args:
        server_url (str): the Synapse base endpoint
        endpoint_path (str): the unique endpoint path of the resource
                             (i.e. "/entity/syn123")

    Raises:
        ValueError: when one or more parameters have invalid value

    Returns:
        str: the URI of the resource
    """
    if server_url is None or endpoint_path is None:
        raise ValueError("server_url and endpoint_path are required.")
    if urllib_parse.urlparse(endpoint_path).path != endpoint_path:
        raise ValueError(f"Incorrect format for endpoint_path: {endpoint_path}")
    return server_url + endpoint_path


def _handle_response(response: requests.Response) -> Union[dict, str]:
    """Handle the reqeusts' Response

    Args:
        response (requests.Response): Response returned from requests

    Returns:
        Union[dict, str]: The response body

    Raises:
        SynapseClientError: please see each error message
    """
    check_status_code_and_raise_error(response)
    content_type = response.headers.get(CONTENT_TYPE_HEADER, None)
    if content_type is not None and content_type.lower().strip().startswith(
        JSON_CONTENT_TYPE
    ):
        return response.json()
    else:
        return response.text


class SynapseClient(ABC):
    """ABC meta class"""

    def __init__(self, auth_token: Optional[str] = None, profile: Optional[str] = None):
        self.auth_token = auth_token
        self.profile = profile

    @property
    def session(self) -> requests.Session:
        """Create Synapse Session

        Returns:
            requests.Session: An authenticated Synapse session
        """
        sess = requests.Session()
        user_agent = requests.utils.default_user_agent()
        sess.headers.update(
            {
                "User-Agent": f"py-synapse/{__version__} {user_agent}",
                "Authorization": f"Bearer {self.auth_token}",
            }
        )
        return sess

    def get(
        self, endpoint_path: str, server_url: Optional[str] = None, **kwargs
    ) -> Union[dict, str]:
        """Performs a HTTP Get request

        Args:
            endpoint_path (str): the unique path in the URI of the resource
                                 (i.e. "/entity/syn123")
            server_url (Optional[str], optional): The Synapse server endpoint.
                                                  Defaults to None.

        Returns:
            dict, str: the response body of the request

        Raises:
            SynapseClientError: please see each error message
        """
        if server_url is None:
            server_url = SYNAPSE_DEFAULT_REPO_ENDPOINT

        url = _generate_request_url(server_url, endpoint_path)
        # TODO: Add logger debug to print url
        resp = self.session.get(url, **kwargs)
        # TODO: Add logger debug to print resp
        return _handle_response(response=resp)

    # _services: dict = {
    #     "teams": "TeamsService",
    # }

    # def get_available_services(self) -> list:
    #     """Get available Synapse services
    #     This is a beta feature and is subject to change"""
    #     services = self._services.keys()
    #     return list(services)

    # def service(self, service_name: str):
    #     """Get available Synapse services
    #     This is a beta feature and is subject to change"""
    #     # This is to avoid circular imports
    #     # TODO: revisit the import order and method https://stackoverflow.com/a/37126790
    #     # To move this to the top
    #     import synapse.services
    #     assert isinstance(service_name, str)
    #     service_name = service_name.lower().replace(" ", "_")
    #     assert service_name in self._services, (
    #         f"Unrecognized service ({service_name}). Run the 'get_available_"
    #         "services()' method to get a list of available services."
    #     )
    #     service_attr = self._services[service_name]
    #     service_cls = getattr(synapse.services, service_attr)
    #     service = service_cls(self)
    #     return service
