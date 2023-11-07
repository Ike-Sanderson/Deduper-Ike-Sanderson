#!/usr/bin/env python

#ver 0.8.3

import re
import argparse

parser = argparse.ArgumentParser(description="A program to open a SAM file and write only unique reads into a new SAM file")
parser.add_argument("-f", '--file', type=str, help="needs a sorted SAM file as input", required=True)
parser.add_argument("-o", '--outfile', type=str, help="name of SAM output file for unique reads", required=True)
parser.add_argument("-d", '--dupesfile', type=str, help="name of output file for duplicate reads", required=True)
parser.add_argument("-u", '--umifile', type=str, help="name of output file for known UMIs", required=True)
parser.add_argument("-s", '--summaryfile', type=str, help="name of summary file", required=True)

args = parser.parse_args()

# Global variables
samfile_in = args.file
samfile_out = args.outfile
dupesfile = args.dupesfile
summaryfile = args.summaryfile
umifile = args.umifile
knownumilist = set()
UMIdict = {}
duplicatereads = 0
uniquereads = 0
currentchrom = None 
unknownumis = 0


#strand function
'''This function will parse the bitwise flag and return a string identifying the 
        strand as either + (forward) or - (reverse)'''
def which_strand(flag: int) -> str:
    if ((flag & 16) ==16):
        STRAND = "-"
    else:
        STRAND = "+"
    return STRAND

#Position_correct function
def position_correct(sam_pos: int, STRAND: str, cigar: str):
    '''This function will fix all starting (5') positions, 
        accounting for soft clip where needed. Will return a corrected 5' POS'''
    A = 0
    rhsc = 0
    lhsc = 0
    if STRAND == "+":
        # plus strand: sam_pos - LHSC
        s = re.match(r'(\d+)S', cigar) #Note: re.match stops at first instance
        if ('S' in cigar) and (s != None):
            lhsc = int(s[0][:-1])
            return (sam_pos - lhsc)
        else:
            return sam_pos
    else:
        match = re.findall(r'(\d+)[D|M|N]', cigar)
        for adj in match:
            A += int(adj)

        if cigar.endswith('S'):
            s = re.findall(r'(\d+)S$', cigar)               #Note $ means end of string
            #print(f'{s=}')
            for smatch in s:
                rhsc = int(smatch)
            PRIMEPOS = (sam_pos + rhsc + A)
            return PRIMEPOS
        else:
            PRIMEPOS = (sam_pos + A)
            return PRIMEPOS
    
with open (umifile,'r') as knownumis:
    for line in knownumis:
        knownumilist.add(line.strip())

#open input SAM file as read, open output SAM file as write
with open (samfile_in, "r") as input, open(samfile_out, 'w') as output, open(dupesfile, 'w') as dupes:
    for line in input:
        if line == "":
            break
        if line.startswith('@'):
            output.write(line)
        else:
            read_being_parsed = line.strip().split()
            CHROM = read_being_parsed[2]                        #capture chromosome number here
            if CHROM != currentchrom:                           #checks to see if the sorted SAM read is a new chromosome
                UMIdict.clear()                                 #dict.clear command takes no arguments
                currentchrom = CHROM                            #sets currentchrom variable to new CHROM
            UMI = read_being_parsed[0].split(':')[7]            #capture UMI here
            if UMI in knownumilist:                             #check that umi is known (vs error)
                cigar = read_being_parsed[5]                    #capture cigar here
                sam_pos = int(read_being_parsed[4])             #capture SAM file start position here
                flag = read_being_parsed[1]                     #capture bitwise flag here
                STRAND = which_strand(int(flag))
                PRIMEPOS = position_correct(sam_pos, STRAND, cigar)
                if (UMI, PRIMEPOS, CHROM, STRAND) in UMIdict:   #check if read is a duplicate
                    UMIdict[(UMI, PRIMEPOS, CHROM, STRAND)] += 1
                    dupes.write(line)
                    duplicatereads += 1
                else:                                           #check if read is unique
                    UMIdict[(UMI, PRIMEPOS, CHROM, STRAND)] = 1
                    uniquereads += 1
                    output.write(line)
   
            else:                                           #umi is an error so skip the read
                continue
                unknownumis += 1
with open(summaryfile, 'w') as summary:
    summary.write(f"the number of unique reads was {uniquereads}\n")
    summary.write(f"the number of duplicate reads was {duplicatereads}\n")
    summary.write(f"the number of unknown umis was {unknownumis}\n")
