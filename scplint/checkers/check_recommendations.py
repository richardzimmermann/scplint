from logging import getLogger

logger = getLogger()

MSGS = {
    'O301': {
        'rule': 'Action unsorted',
        'msg': 'Actions are unsorted.'
    },
    'O302': {
        'rule': 'NotAction unsorted',
        'msg': 'NotActions are unsorted.'
    },
    'O303': {
        'rule': 'Add Wildcard',
        'msg': ('Action {action_1} and {action_2} can be abstracted by '
                'a wildcard {action_1}*.')
    },
    'O304': {
        'rule': 'Unnecessary Action',
        'msg': '{action_1} is already a wildcard for {action_2}.'
    }
}


class CheckRecommendations():
    def __init__(self, report):
        logger.debug('initialize: check optimizations')
        self.report = report
        self.scp = report.scp
        self._check_statements()

    def _check_statements(self):
        ''' check every statement if its sorted or if it can be optiomized
        '''
        for statement in self.scp.statements:
            self._check_sort(statement)
            self._check_optimizations(statement)

    def _check_sort(self, statement):
        ''' check if the given statement is already sorted
        '''

        if statement.actions and isinstance(statement.actions, list):
            if sorted(statement.actions) != statement.actions:
                self.report.add_recommendation(MSGS, 'O301', {})

        if statement.notactions and isinstance(statement.notactions, list):
            if sorted(statement.notactions) != statement.notactions:
                self.report.add_recommendation(MSGS, 'O302', {})

    def _check_optimizations(self, statement):
        ''' compare actions within a single statement and check if they can be
        abstracted by wildcards to reduce the policy size
        '''
        actions = statement.actions or statement.notactions

        if isinstance(actions, list) and len(actions) > 1:
            for action_1 in actions:
                for action_2 in actions:
                    details = {'action_1': action_1, 'action_2': action_2}

                    if action_1 == action_2:
                        continue

                    if action_1 in action_2:
                        self.report.add_recommendation(MSGS, 'O303', details)

                    if '*' in action_1 and action_1.split('*')[0] in action_2:
                        self.report.add_recommendation(MSGS, 'O304', details)
