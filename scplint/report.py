import copy
from logging import getLogger

logger = getLogger()


def _format_msg(func):
    def wrapper(report, msgs, code, details):
        msgs_copy = copy.deepcopy(msgs)
        msg = msgs_copy[code]
        msg['code'] = code
        msg['msg'] = msg['msg'].format(**details)

        func(report, msg)

    return wrapper


class Report():
    def __init__(self, scp):
        logger.debug('initialize report')
        self.scp = scp
        self.file = scp.file
        self.size = scp.size
        self.size_max = scp.size_max
        self.percent = scp.percent

        self.statements = scp.statements
        self.actions = scp.actions
        self.notactions = scp.notactions
        self.actions_actual = []
        self.actions_explicit = []
        self.actions_wildcard = []
        self.actions_info = []
        self.actions_warning = []
        self.actions_error = []

        self.errors = []
        self.warnings = []
        self.infos = []
        self.recommendations = []

    def get_report(self):
        logger.debug('get report')

        report = {
            'file': self.file,
            'size': self.size,
            'size_maximum': self.size_max,
            'percent': f'{self.percent}%',
            'actions': {
                'actions': len(self.actions),
                'notactions': len(self.notactions),
                'actual': len(self.actions_actual),
                'explicit': len(self.actions_explicit),
                'wildcard': len(self.actions_wildcard),
                'info': len(self.actions_info),
                'warning': len(self.actions_warning),
                'error': len(self.actions_error)
            },
            'summary': {
                'recommendations': len(self.recommendations),
                'infos': len(self.infos),
                'warnings': len(self.warnings),
                'errors': len(self.errors)
            }
        }

        return report

    def get_report_detailed(self):
        logger.debug('get detailed report')

        report = self.get_report()

        report['details'] = {}
        if self.errors:
            report['details']['errors'] = self.errors

        if self.warnings:
            report['details']['warnings'] = self.warnings

        if self.infos:
            report['details']['infos'] = self.infos

        if self.recommendations:
            report['details']['recommendations'] = self.recommendations

        return report

    @_format_msg
    def add_error(self, msg):
        logger.error(msg)
        self.errors.append(msg)

    @_format_msg
    def add_warning(self, msg):
        logger.warning(msg)
        self.warnings.append(msg)

    @_format_msg
    def add_info(self, msg):
        logger.info(msg)
        self.infos.append(msg)

    @_format_msg
    def add_recommendation(self, msg):
        logger.info(msg)
        self.recommendations.append(msg)
