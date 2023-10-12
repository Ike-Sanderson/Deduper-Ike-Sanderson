# Test file for deduper

## cases covered in test.sam
-line 25 unique [will be written]
-line 26 unique [will be written]
-line 27 unique [will be written]
-line 28 2 base soft clip duplicate of line 25, adjusted POS +2 [will not be written]
-line 29 exact duplicate of line 25 [will not be written]
-line 30 not a duplicate; bitwise flag 16 tells us reverse complement [will be written]
-line 31 2 base soft clip duplicate of line 103 -strand, adjusted POS -2 [will not be written]
-insertion of leftmost bases, affecting POS, not yet tested in this file; not sure how to account for error that should be skipped
-UMI error, not sure how to capture this unless I accept all UMIs 
-deletion of leftmost bases, affecting POS, not yet tested in this file; not sure how to account for error that should be skipped
