import argparse
import configparser
import json
import pathlib
import re
from glob import glob

import yaml

import scplint
from scplint.log import init_logging
from scplint.report import Report
from scplint.scp import SCP
from scplint.run_checks import run_checks

#
PARSER = argparse.ArgumentParser(
    description=('SCPlint to validate and optimize your AWS SCPs'))

PARSER.add_argument('-i', '--input', required=True,
                    help='Path to the SCP(s), e.g. "path/to/scp.json"')
PARSER.add_argument('-d', '--detailed', action='store_true',
                    help='Enable detailed report of your SCP(s)')
PARSER.add_argument('-m', '--minimize', action='store_true',
                    help='Minimize the SCP (remove linebreaks and blanks)')
PARSER.add_argument('-r', '--recursive', action='store_true',
                    help='Search recursive for json files the given folder.')
PARSER.add_argument('-o', '--output', choices=['json', 'yaml'], default='json',
                    help='Configure output format of the report')
PARSER.add_argument('-v', '--verbose', action='store_true',
                    help='Enable verbose logging.')
PARSER.add_argument('--version', action='version',
                    version=f'scplint v{scplint.__version__}',
                    help='Print the current version of scplint')

ARGS = vars(PARSER.parse_args())

if ARGS.get('verbose'):
    log_level = 'DEBUG'
else:
    log_level = 'ERROR'

logger = init_logging(log_level=log_level, formatter='console')


def verify_search_term():
    search_term = ARGS['input']
    logger.debug('input search term is %s', search_term)

    if search_term == '.' and ARGS.get('recursive'):
        search_term = '**/*.json'
    elif search_term == '.' and not ARGS.get('recursive'):
        search_term = '*.json'
    elif re.match(r'.*/$', search_term) and ARGS.get('recursive'):
        search_term += '**/*.json'
    elif re.match(r'.*/$', search_term) and not ARGS.get('recursive'):
        search_term += '*.json'

    logger.debug('continue with search term %s', search_term)
    return search_term


def get_file_paths():
    search_term = verify_search_term()
    files = glob(search_term, recursive=ARGS.get('recursive'))
    logger.debug('found %s file(s): %s', len(files), files)
    return files


def print_report(report: dict):
    # print('-----------------------------------------------------------\n')

    if ARGS['output'] == 'json':
        print(json.dumps(report, indent=4, sort_keys=True))
    elif ARGS['output'] == 'yaml':
        print(yaml.dump(report, width=79, indent=2))

    print('\n-----------------------------------------------------------')


def create_summary(all_results: list) -> dict:
    report = {
        'files': [],
        'summary': {
            'recommendations': 0,
            'infos': 0,
            'warnings': 0,
            'errors': 0
        }
    }

    for result in all_results:
        report['files'].append(result['file'])
        report['summary']['recommendations'] += (
            result['summary']['recommendations'])
        report['summary']['infos'] += result['summary']['infos']
        report['summary']['warnings'] += result['summary']['warnings']
        report['summary']['errors'] += result['summary']['errors']

    return report


def main():
    files = get_file_paths()
    all_results = []

    for file in files:
        logger.info('check file %s', file)

        policy = json.loads(open(file).read())
        minimize = ARGS.get('minimize')
        scp = SCP(scp=policy, filename=file, minimize=minimize)

        report = Report(scp)
        run_checks(report)

        if not ARGS.get('detailed'):
            results = report.get_report()
        else:
            results = report.get_report_detailed()

        all_results.append(results)
        print_report(results)

    if len(files) > 1:
        summary = create_summary(all_results)
        print_report(summary)
