from scplint.aws_actions import AwsActions

from logging import getLogger

logger = getLogger()

MSGS = {
    'W201': {
        'rule': 'Unknown Action',
        'msg': 'Action {action} is unknown. Do you mean {action_aws}?'
    },
    'I201': {
        'rule': 'Duplicate Action',
        'msg': ('There are {duplicates} duplicated Action/NotAction items. '
                'Ignore this message if you are using different '
                'resources/conditions.')
    }
}


class CheckActions():
    def __init__(self, report):
        logger.debug('initialize: check actions')
        self.report = report
        self.scp = report.scp
        self.actions_aws = AwsActions().get_aws_actions()
        self._check_actions()
        self._check_duplicates()

    def _check_actions(self):
        for action in self.report.actions:
            self._check_action_explicit(action)

            for action_aws in self.actions_aws:
                self._check_action_wildcard(action, action_aws)
                self._check_warning_actions(action, action_aws)

    def _check_action_explicit(self, action):
        if action in self.actions_aws:
            logger.debug('%s is a fully supported AWS action', action)
            self.report.actions_explicit.append(action)

    def _check_action_wildcard(self, action, action_aws):
        if len(action.split('*')) > 1 and action.split('*')[0] in action_aws:
            logger.debug('%s contains a wildcard for %s', action, action_aws)
            # self.report.infos.append(MSGS['I001'])
            self.report.actions_wildcard.append(action_aws)

    def _check_warning_actions(self, action, action_aws):
        details = {'action': action, 'action_aws': action_aws}
        # if len(action.split('*')) > 1:
        #     action = action.split('*')[0]

        if action not in self.report.actions_explicit:
            if (action != action_aws) and (action in action_aws
                                           or action_aws in action):
                self.report.actions_warning.append(action)
                self.report.add_warning(MSGS, 'W201', details)

    def _check_duplicates(self):
        actions = self.report.actions
        dedup_actions = list(set(actions))

        if len(dedup_actions) < len(actions):
            details = {'duplicates': (len(actions) - len(dedup_actions))}
            self.report.add_warning(MSGS, 'I201', details)
