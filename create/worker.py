#!/usr/bin/env python3
"""Celery worker wrapper.

Reads options from a config file (or command-line arguments), then execs a
celery worker process.
"""
import argparse
import os


def main():
    """Entrypoint into wrapper."""
    parser = argparse.ArgumentParser(
        description='Process incoming OCF account creation requests.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-l',
        '--log-level',
        type=str,
        default='info',
        help='Backend URI to use for Celery.',
    )
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        default='/etc/ocf-create/ocf-create.conf',
        help='Config file to read from.',
    )
    args = parser.parse_args()

    os.environ['CREATE_CONFIG_FILE'] = args.config
    os.execvp(
        'celery',
        (
            'celery',
            'worker',
            '-A', 'create.tasks',
            '-l', args.log_level,
        ),
    )


if __name__ == '__main__':
    main()
