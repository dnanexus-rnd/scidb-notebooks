#!/usr/bin/python

import vcf
import argparse
import sys

ti = 0
tv = 0
num_records = 0

# This version uses PyVCF functions.
# There are slight calling differences between the DIY version and
# this one.
def account_rec_native(rec):
    global ti, tv
    if not rec.is_snp:
        return
    if rec.is_transition:
        ti += 1
    else:
        tv += 1

def print_totals(i):
    ratio = float(ti) / float(tv)
    if i is not None:
        print("num records={}  tot={} ti={}  tv={}  ti/tv={}".format(i, num_records, ti, tv, ratio))
    else:
        print("tot={} ti={}  tv={}  ti/tv={}".format(num_records, ti, tv, ratio))
    sys.stdout.flush()

# Process all records in the file
def process_file(fname, nlimit):
    global num_records
    print("Processing VCF file {}".format(fname))
    with open(fname, 'r') as f:
        vcf_reader = vcf.Reader(f)
        i = 0
        while True:
            num_records += 1
            i = i + 1
            if i % 1000 == 0:
                print_totals(i)
            if (nlimit is not None and
                i >= nlimit):
                break
            rec = vcf_reader.next()
            account_rec_native(rec)

# parse command line
parser = argparse.ArgumentParser(description='Count ti/tv on a VCF file')
parser.add_argument('--file', dest="filenames", action='append',
                    help='VCF file name')
parser.add_argument('--nlimit', type=int,
                    help='how many records to process per file')
args = parser.parse_args()
if (args.filenames is None or
    len(args.filenames) == 0):
    print("must specify VCF file")
    exit(1)

# process all files
for fname in args.filenames:
    process_file(fname, args.nlimit)

print_totals(None)