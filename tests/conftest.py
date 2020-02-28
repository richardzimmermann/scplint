import pytest


@pytest.fixture
def scp_valid_action():
    scp = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Deny",
            "Action": [
                "config:DeleteAggregationAuthorization",
                "config:DeleteDeliveryChannel",
                "config:DeleteDelivery*",
                "ec2:*"
            ],
            "Resource": "*"
        }]
    }

    yield scp


@pytest.fixture
def scp_valid_notaction():
    scp = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Deny",
            "NotAction": [
                "config:DeleteAggregationAuthorization",
                "config:DeleteDeliveryChannel",
                "config:DeleteDelivery*",
                "ec2:*"
            ],
            "Resource": "*"
        }]
    }
