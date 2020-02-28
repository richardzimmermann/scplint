import json
import os
from logging import getLogger

logger = getLogger()


class Statement:
    def __init__(self, statement: dict):
        self.statement = statement
        self.sid = statement.get('Sid')
        self.effect = statement.get('Effect')
        self.actions = self._get_items('Action')
        self.notactions = self._get_items('NotAction')
        self.resources = self._get_items('Resource')

        # self.actions = statement.get('Action', [])
        # self.notactions = statement.get('NotAction', [])
        # self.resources = statement.get('Resource', [])

        self.conditions = statement.get('Condition', [])

    def _get_items(self, item: str):
        items = self.statement.get(item, [])

        if isinstance(items, list):
            return items
        else:
            return [items]

    def _sort_actions(self):
        self.actions.sort()

    def _sort_notactions(self):
        self.notactions.sort()
