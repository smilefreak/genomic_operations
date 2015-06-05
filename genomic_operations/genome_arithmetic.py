#!/usr/bin/env python
# Copyright (c) 2015 Boocock James <james.boocock@otago.ac.nz>
# Author: Boocock James <james.boocock@otago.ac.nz>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s' )
import argparse
import sys

from genomic_operations.sniff.sniffer import setup_sniffers 
from genomic_operations.dts.single_pos import SinglePositionList
from genomic_operations.dts.single_pos import PSEQPos, TwoColPos, GeminiPos
from genomic_operations.operations.merge import merge_single_pos


def sniff_and_add_datasets(sniffer, genome_datasets):
    single_pos_list = [] 
    logging.info("Sniffing and adding dataset")
    for i, genome_f in enumerate(genome_datasets):
        sniff_result = sniffer.sniff_datatype(genome_f)
        if sniff_result is None:
            logging.error("Could not determine datatype for file: {0},  continuing anyway\n".format(genome_f))
        else:
            if sniff_result.header is not None:
                single_pos_list.append(SinglePositionList(sniff_result.sniffer_class, sniff_result.header))
                start = 1
            else:
                single_pos_list.append(SinglePositionList(sniff_result.sniffer_class))
                start = 0
            with open(genome_f) as gf:
                for j, line, in enumerate(gf):
                    if j >= start:
                        single_pos_list[i].append(sniff_result.sniffer_class(line))
    logging.info("Successfully determined the filetypes of input files")
    return single_pos_list

def main():
    """
        Takes arbitrary genomic files containing any information and performs genomic arithmetic
    """

    parser = argparse.ArgumentParser(description="Genomic Arithmetic")
    subparsers = parser.add_subparsers(title='Arithmetic subcommands',
                                     description="Valid arithmetic subcommands")
    mer = subparsers.add_parser('merge')
    mer.add_argument('genome_files', nargs='*', help='Genome Arithmetic')
    mer.add_argument('-o','--output', dest='output', help='Output file')
    mer.set_defaults(func=merge_single_pos)
    args = parser.parse_args()
    if args.output is None:
        args.output = sys.stdout
    else:
        args.output = open(args.output, 'w')
    sniffer = setup_sniffers()
    datasets =  sniff_and_add_datasets(sniffer, args.genome_files)
    args.func(datasets, args.output)

if __name__ == "__main__":
    main()
