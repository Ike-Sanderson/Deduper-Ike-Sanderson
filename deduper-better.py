#!Usr/bin/env python

#I think I like this version better

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
def true_leftPOS(POS: int) -> int:

    '''This function will iterate through input SAM reads and fix all starting left (5') positions, 
        accounting for soft clip where needed. Will return a corrected 5' POS'''

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
                        #return true_leftPOS
                    #else
                        #true_leftPOS = POS
                        #return true_leftPOS    

                #else, i.e. if((flag&16) == 16) --> strand is revcomp
                    #if soft clip, extract countback from cigar, adjust POS
                    #if re.match('$6~/^(([1-9]|[1-9][0-9])[S]$/', readline) <- maybe this will work? 
                        #countback = the same regex used above
                        #true_leftPOS = readline[$4] - countback
                        #return true_leftPOS
                    #else
                    #true_leftPOS = POS
                    #return true_leftPOS
            #else:
                #continue
        
    #close input SAM file   

'''Main'''

'''iterate through temp SAM file and build dictionary of RNAME=key: POS = value
for each dict entry, write line to new SAM file
as build dict, check to see if key:value already exists, if so => do not write'''

#Store UMIs as a list
#with open STL96.txt as u:
    #umilist = u.read()

#open input SAM file as read, open output SAM file as write
    #for loop line in tempSAM file
        #if readline != ('^N') <- trying to say "does not start with N"
            #write line to output SAM file --> Copying all the header lines into the new file
        
        #else 
            #readline and store UMI from $1,POS from $4, RNAME from $3
            #check if UMI is in the list
                #if search(umilist,UMI):  (i.e. if TRUE, UMI is in list and we can move on checking read)
                    #call true_leftPOS function
                    #if RNAME, true_leftPOS, and UMI already in RNAMEdict (i.e. readline[$3] RNAME==key and 
                    #                                      readline[4]==RNAMEdict 1st value and
                    #                                      readline[1]==RNAMEdict 2nd value)
                        # continue i.e. skip, do NOT write from input to output
                    
                    #else 
                        #RNAMEdict[RNAME] += [true_leftPOS,UMI]  i.e. assign true_leftPOS as 1st value for RNAME key, add UMI to 2nd value
                        #write readline to output SAM file
                #else:
                    #continue (UMI must be bad so throw out the read)
    #close input and output SAM files







