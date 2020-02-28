import pytest

from scplint.scp import SCP
from scplint.report import Report


def test_report_init(scp_valid_action):
    scp = SCP(scp=scp_valid_action)
    report = Report(scp)


def test_report_get_report(scp_valid_action):
    scp = SCP(scp=scp_valid_action)
    report = Report(scp)
    report.get_report()


def test_report_get_report_detailed(scp_valid_action):
    scp = SCP(scp=scp_valid_action)
    report = Report(scp)
    report.get_report_detailed()
