import pytest

from scplint.scp import SCP


def test_scp_init(scp_valid_action):

    scp = SCP(scp=scp_valid_action)
    scp.minimize()
