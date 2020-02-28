import json
import os
from logging import getLogger
from pathlib import Path

import botocore

logger = getLogger()


class AwsActions:
    def __init__(self):
        self.aws_actions = []

    def get_aws_actions(self) -> list:
        ''' read a local file with aws actions and returns a list

        Returns:
            aws_actions (list): a list with known aws actions
        '''
        script_dir = os.path.dirname(__file__)
        rel_path = 'data/aws_actions.txt'
        abs_file_path = os.path.join(script_dir, rel_path)
        file = open(abs_file_path, 'r')
        self.aws_actions = file.read().splitlines()
        return self.aws_actions

    def update_aws_actions(self):
        botocore_path = os.path.abspath(botocore.__file__)
        botocore_data_path = (
            f'{botocore_path.split("botocore")[0]}/botocore/data/')

        for path in Path(botocore_data_path).rglob('service*.json'):
            try:
                # print(f'{path}')
                item = open(path, 'r', encoding="utf8")
                item_content = json.loads(item.read())
                item.close()

                metadata = item_content.get('metadata', {})
                service_prefix = (metadata.get('signingName')
                                  or metadata.get('endpointPrefix'))
                operations = item_content.get('operations', {})

                for operation in operations.keys():
                    action = f'{service_prefix}:{operation}'
                    if action not in self.aws_actions:
                        self.aws_actions.append(action)

            except Exception as error:
                logger.exception(error)
                logger.error(path)

        script_dir = os.path.dirname(__file__)
        rel_path = 'data/aws_actions.txt'
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, 'w') as f:
            for item in self.aws_actions:
                f.write(f'{item}\n')
