import json
import os
from logging import getLogger
from pathlib import Path

from scplint.statement import Statement

logger = getLogger()


class SCP:
    def __init__(self, scp: dict, filename: str = 'my_scp',
                 size_max: int = 5120, minimize: bool = False):
        logger.debug('initialize scp')
        self.scp = scp
        self.file = filename
        self.minimized = minimize

        self.statements = self._get_statements()

        logger.debug('get scp metrics')
        self.size = self._get_size(min=minimize)
        self.size_max = size_max
        self.percent = self._get_percent(self.size)
        self.actions = self._get_actions()
        self.notactions = self._get_notactions()

    def _get_statements(self) -> list:
        '''
        '''
        logger.debug('Get every Statement from the SCP')
        statements = []

        for statement in self.scp.get('Statement', []):
            statements.append(Statement(statement))

        return statements

    def _get_actions(self) -> list:
        '''
        '''
        logger.debug('Get every Action from the SCP')
        actions = []

        for statement in self.statements:
            logger.info(statement.actions)
            actions += statement.actions

        logger.info(actions)
        logger.info(len(actions))

        return actions

    def _get_notactions(self) -> list:
        '''
        '''
        logger.debug('Get every NotAction from the SCP')
        notactions = []

        for statement in self.statements:
            notactions += statement.notactions

        return notactions

    def _get_size(self, min: bool = False) -> int:
        ''' checks the actual size of the json policy in bytes as aws
        does it if you create/update a scp

        Args:
            min (bool): True if policy should be minimized before calculating
                the size.

        Returns:
            scp_bytes (int): the size of the scp in bytes as int
        '''
        logger.debug('Get the size in bytes of the SCP (minimized=%s)', min)
        if min:
            scp_bytes = len(self.minimize().encode('utf-8'))
        else:
            scp_bytes = len(json.dumps(self.scp, indent=4).encode('utf-8'))

        return scp_bytes

    def _get_percent(self, size: int, precision: int = 1) -> float:
        ''' check the actual size of the minimized json policy as percentage
        against the maximum policy size of aws

        Args:
            size (int): the size of the policy in bytes
            precision (int): the precision of the percentage value

        Returns:
            percent (float): the size of the scp as percentage value
        '''
        logger.debug('Get the size in percent of the SCP')
        percent = round(100 / 5120 * size, precision)

        return percent

    def minimize(self) -> str:
        ''' convert the json scp into a minifed str (remove blanks, tabs and
        linebreaks)

        Returns:
            scp_minified (str): a minified version of the json policy
        '''
        logger.debug('Format the json policy into a minized text')
        scp_minified = json.dumps(self.scp).replace(" ", "")
        return scp_minified
