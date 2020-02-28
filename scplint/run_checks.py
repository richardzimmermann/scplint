from logging import getLogger

from scplint.checkers import *

logger = getLogger()


def run_checks(report):
    logger.debug('run checks')
    check_schema.CheckSchema(report)
    check_limits.CheckLimits(report)
    check_actions.CheckActions(report)
    check_recommendations.CheckRecommendations(report)
