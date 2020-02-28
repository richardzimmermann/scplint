from logging import getLogger

logger = getLogger()

MSGS = {
    'E101': {
        'rule': 'Size Error',
        'msg': 'SCP hit maximum size ({size}/{size_max} bytes).'
    },
    'E102': {
        'rule': 'Size Error',
        'msg': ('SCP hit maximum size ({size}/{size_max} bytes). '
                'Please try it again with argument -m (--minimize).')
    },
    'W101': {
        'rule': 'Size Warning',
        'msg': ('Your SCP has already reached {percent}% of the maximum size.')
    },
    'W102': {
        'rule': 'Size Warning',
        'msg': ('Your SCP has already reached {percent}% of the maximum size. '
                'Please try it again with argument -m (--minimize).')
    }
}


class CheckLimits():
    def __init__(self, report):
        logger.debug('initialize: check limits')
        self.report = report
        self.scp = report.scp
        self._check_scp_limit()

    def _check_scp_limit(self):
        if self.scp.size > self.scp.size_max and self.scp.minimized:
            self.report.add_error(MSGS, 'E101', vars(self.scp))

        elif self.scp.size > self.scp.size_max and not self.scp.minimized:
            self.report.add_error(MSGS, 'E102', vars(self.scp))

        elif self.scp.percent > 90 and self.scp.minimized:
            self.report.add_warning(MSGS, 'W101', vars(self.scp))

        elif self.scp.percent > 90 and not self.scp.minimized:
            self.report.add_warning(MSGS, 'W102', vars(self.scp))
