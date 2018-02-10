# -*- coding: UTF-8 -*-
# cli.py
# Noah Rubin
# 01/31/2018

import os
from argparse import ArgumentParser, ArgumentTypeError

def DBConnectConfig(arg):
    '''
    Args:
        arg: String => database connection string or filepath
    Returns:
        Database connection string
    Preconditions:
        arg is of type String   (assumed True)
    '''
    ext = os.path.splitext(arg)
    if ext in set(['.db', '.sqlite']) or not os.path.exists(os.path.dirname(arg)):
        return arg
    try:
        with open(os.path.abspath(arg), 'r') as config:
            connect = config.read().strip()
        return connect
    except Exception as e:
        raise ArgumentTypeError(str(e))

def initialize_parser():
    ## Main parser
    main_parser = ArgumentParser(prog='apf.py', description='Windows prefetch file parser')
    main_parser.add_argument('-V', '--version', action='version', version='%(prog)s v0.0.1')
    main_directives = main_parser.add_subparsers()

    ## Base output parent
    base_output_parent = ArgumentParser(add_help=False)
    base_output_parent.add_argument('-t', '--target', type=str, help='Path to output file', dest='target')

    ## CSV output parent parser
    csv_output_parent = ArgumentParser(parents=[base_output_parent], add_help=False)
    csv_output_parent.add_argument('--sep', default=',', help='Output file separator', dest='sep')

    ## Bodyfile output parent parser
    body_output_parent = ArgumentParser(parents=[base_output_parent], add_help=False)
    body_output_parent.add_argument('--sep', default='|', choices=['|'], help='Output file separator', dest='sep')

    ## DB connect parent parser
    db_connect_parent = ArgumentParser(add_help=False)
    db_connect_parent.add_argument('-d', '--driver', type=str, default='sqlite', help='Database driver to use (default: sqlite)', dest='driver')
    db_connect_parent.add_argument('-c', '--connect', type=DBConnectConfig, help='Database connection string, or filepath to file containing connection string', dest='conn_string')

    ## Parse directives
    parse_directive = main_directives.add_parser('parse', help='prefetch file parser directives')
    parse_subdirectives = parse_directive.add_subparsers()

    # CSV parse directive
    csv_parse_directive = parse_subdirectives.add_parser('csv', parents=[csv_output_parent], help='Parse prefetch file to csv')
    csv_parse_directive.add_argument('info_type', \
        type=str, \
        default='summary', \
        choices=['summary', 'header', 'finfo', 'fmetrics', 'tchains', 'fnstrings', 'vinfo', 'frefs', 'dstrings'], \
        help='Type of information to output')
    
    # Bodyfile parse directive
    body_parse_directive = parse_subdirectives.add_parser('body', parents=[body_output_parent], help='Parse prefetch MAC times to bodyfile')

    # JSON parse directive
    json_parse_directive = parse_subdirectives.add_parser('json', parents=[base_output_parent], help='Parse prefetch file to JSON')
    json_parse_directive.add_argument('-p', '--pretty', action='store_true', help='Whether to pretty-print the JSON output', dest='pretty')

    # Database parse directive
    db_parse_directive = parse_subdirectives.add_parser('db', help='Parse prefetch file to database')

    ## Convert directives
    convert_directives = main_directives.add_parser('convert', help='Parsed prefetch file output conversion directives')
    convert_subdirectives = convert_directives.add_subparsers()

    # CSV conversion directive
    csv_convert_directive = convert_subdirectives.add_parser('csv', help='Convert from CSV output')

    # Body conversion directive
    body_convert_directive = convert_subdirectives.add_parser('body', help='Convert from bodyfile output')
    
    # JSON conversion directive
    json_convert_directive = convert_subdirectives.add_parser('json', help='Convert from JSON output')

    # DB conversion directive
    db_convert_directive = convert_subdirectives.add_parser('db', help='Convert from database output')

    return main_parser
