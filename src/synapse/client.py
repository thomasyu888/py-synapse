from dataclasses import dataclass
from typing import Optional

import requests  # type: ignore

from synapse import __version__


def session(authtoken: str, profile: Optional[str] = None) -> requests.Session:
    """Create session

    Args:
        authtoken (str): Synapse auth token
        profile (str, optional): Profile to use for authentication. Defaults to None.

    Returns:
        Session: A requests session
    """
    sess = requests.Session()
    user_agent = requests.utils.default_user_agent()
    sess.headers.update(
        {
            "User-Agent": f"py-synapse/{__version__} {user_agent}",
            "Authorization": f"Bearer {authtoken}",
        }
    )
    return sess


@dataclass
class SynapseClient:
    """Client"""

    session: str

    def client(self):
        """call services"""
        pass
