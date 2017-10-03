#!/usr/bin/env python3

'''Trim low quality reads and remove sequences less than 35 base pairs.'''

import os
import subprocess
import argparse
import shutil
import logging
import sys
import json

EPILOG = '''
For more details:
        %(prog)s --help
'''

## SETTINGS

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.propagate = False
logger.setLevel(logging.INFO)


def get_args():
    '''Define arguments.'''
    parser = argparse.ArgumentParser(
        description=__doc__, epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-f', '--fastq',
                        help="The fastq file to run triming on.",
                        nargs='+',
                        required=True)

    parser.add_argument('-p', '--paired',
                        help="True/False if paired-end or single end.",
                        default=False,
                        action='store_true')

    args = parser.parse_args()
    return args


def check_tools():
    '''Checks for required componenets on user system'''

    logger.info('Checking for required libraries and components on this system')

    trimgalore_path = shutil.which("trim_galore")
    if trimgalore_path:
        logger.info('Found trimgalore: %s', trimgalore_path)
    else:
        logger.error('Missing trimgalore')
        raise Exception('Missing trimgalore')

    cutadapt_path = shutil.which("cutadapt")
    if cutadapt_path:
        logger.info('Found cutadapt: %s', cutadapt_path)
    else:
        logger.error('Missing cutadapt')
        raise Exception('Missing cutadapt')


def trim_reads(fastq, paired):
    '''Run trim_galore on 1 or 2 files.'''

    if paired: # paired-end data
        qc_command = "trim_galore --paired -q 25 --illumina --gzip --length 35 " \
                    + " ".join(fastq)
    else:
        qc_command = "trim_galore -q 25 --illumina --gzip --length 35 " \
                    + " ".join(fastq)

    logger.info("Running trim_galore with %s", qc_command)

    qual_fastq = subprocess.Popen(qc_command, shell=True)
    out, err = qual_fastq.communicate()


def main():
    args = get_args()

    # Create a file handler
    handler = logging.FileHandler('trim.log')
    logger.addHandler(handler)

    # Check if tools are present
    check_tools()

    # Run trim_reads
    trim_reads(args.fastq, args.paired)


if __name__ == '__main__':
    main()
