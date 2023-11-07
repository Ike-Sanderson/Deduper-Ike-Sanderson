#!/bin/bash
#SBATCH --account=bgmp              ### This is my actual account for charging
#SBATCH --partition=bgmp            ### queue to submit to (backup option = compute)
#SBATCH --job-name=deduper          ### job name
#SBATCH --output=deduper_%j.out       ### file in which to store job stdout
#SBATCH --error=deduper_%j.err        ### file in which to store job stderr
#SBATCH --time=4:00:00              ### wall-clock time limit, in minutes
#SBATCH --mem=32G                   ### memory limit per node, in MB
#SBATCH --nodes=1                   ### number of nodes to use
#SBATCH --cpus-per-task=8           ### number of cores for each task

conda activate bgmp_deduper

#sort SAM file
/usr/bin/time -v samtools sort /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam -O sam -o C1_SE_uniqAlign-sorted.sam  

#run python script
/usr/bin/time -v ./deduper.py -f /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam -o dedup-output.sam -d dup-reads.txt -u STL96.txt -s dedup-summary.txt