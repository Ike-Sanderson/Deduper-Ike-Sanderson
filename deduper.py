#!Usr/bin/env python




'''The problem:
PCR can amplify copies of some DNA molecules more than others. This inequality 
can give an inaccurate picure of a cell's activity

In addition, soft clipping can affect the accurate ID of the 5' starting position, 
and if a read is from the reverse strand, a couple of extra steps must be taken to correct the soft clipping'''


'''This solution A) corrects the POS, B) makes a dictionary with RNAME:POS:UMI and C) uses the dictionary 
to direct which reads are writtent to the output SAM file'''

import re

RNAMEdict = {}


#Position_correct 

'''I started out trying to write this as a high level function but kept coming back to just wanting to have this set of code run 
to completion and then run the next set. I dont ask the code to manipulate and then return values, 
rather I ask it to rewrite the file. It seems safer than rewriting the original SAM.

    This block will iterate through input SAM reads and fix all starting left (5') positions, 
    accounting for soft clip where needed. Write all lines (including any corrected POS) to a temp SAM file (so I don't corrupt original)'''

#open input SAM file as read, open tempSAM file as write
    #for loop iterates through
        #readline
            #if line begins with "N":
                #if forward strand, i.e. if((flag&16) != 16)
                    #if soft clip, extract countback from cigar, adjust POS
                    #if re.match('$6~/^(([1-9]|[1-9][0-9])[S]$/', readline) <- maybe this will work?
                                                        ## (starts w any single or dble digit number followed by S)
                        #countback = the same regex used above
                        #true_leftPOS = readline[$4] + countback
                        #write readline with true_leftPOS into tempSAM file

                #else, i.e. if((flag&16) == 16) --> strand is revcomp
                    #if soft clip, extract countback from cigar, adjust POS
                    #if re.match('$6~/^(([1-9]|[1-9][0-9])[S]$/', readline) <- maybe this will work? 
                        #countback = the same regex used above
                        #true_leftPOS = readline[$4] - countback
                        #write readline with true_leftPOS into tempSAM file
            #else:
                #write readline to tempSAM file
    #close input SAM file, close tempSAM file    

#Write output SAM file

'''iterate through temp SAM file and build dictionary of RNAME=key: POS = value
for each dict entry, write line to new SAM file
as build dict, check to see if key:value already exists, if so => do not write'''

#open tempSAM file as read, open output SAM file as write
    #for loop line in tempSAM file
        #readline
            #if readline != ('^N') <- trying to say "does not start with N"
                #write line to output SAM file --> Copying all the header lines into the new file
            
            #else 
                #if RNAME, POS, and UMI already in RNAMEdict (i.e. readline[$3] RNAME==key and 
                #                                      readline[4]==RNAMEdict 1st value and
                #                                      readline[1]==RNAMEdict 2nd value)
                    # continue i.e. skip, do NOT write from input to output
                
                #else 
                    #RNAME = readline[$3]
                    #RNAMEdict[RNAME] = [readline[$4]]  assign POS as 1st value for RNAME key, add QNAME (from $1) to 2nd value
                    #write readline to output SAM file
    #close input and output SAM files






