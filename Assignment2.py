#! /usr/bin/python3

import os,sys,subprocess,shutil
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

taxonomyID="txid8782" #Enter query taxonomy ID in quotes
protein="glucose-6-phosphatase" #Enter query protein in quotes
esearch_output="esearch_output" 
subprocess.call("esearch -db Protein -query '" + taxonomyID + "[Organism:exp] AND " + protein + "[Protein])' | efetch -format fasta > " + esearch_output, shell=True)

cons_output="cons_output"
subprocess.call("cons -sequence " + esearch_output + " -outseq " + cons_output, shell=True) #Command outputs a sequence that best represents the input sequences

blastdb_output="blastdb_output"
subprocess.call("makeblastdb -in " + esearch_output + " -dbtype prot -out " + blastdb_output, shell=True) #Bash database created in preparation of blastp

num_alignments="250" #value set to 250 but user can change 
blastpAccID_output="blastp_output"
subprocess.call("blastp -db " + blastdb_output + " -query " + cons_output + " -num_alignments " + num_alignments + " -outfmt '6 sseqid' > " + blastpAccID_output, shell=True)

#Command pulls sequences from original list of protein sequences against for the accession numbers of interest
pullseq_output="pullseq_output"
subprocess.call("/localdisk/data/BPSM/Assignment2/pullseq -i " + esearch_output + " -n " +  blastpAccID_output + " > " + pullseq_output, shell=True)

#plotcon reads a sequence alignment and draws a plot of the sequence conservation within windows over the alignment.
window_size="6" #Number of columns to average alignment quality over. The larger this value is, the smoother the plot will be. (4 minimum) 
plotcon_output="plot_output" #Option for user to name output plot  
subprocess.call("plotcon -sequences " +  pullseq_output + " -graph svg -winsize " + window_size + " > " + plotcon_output ,shell=True) 

#Motif directory created for patmatmotifs outputs
dir = "motifs"
if os.path.exists(dir):
	shutil.rmtree(dir)
os.makedirs(dir)   

AccID = open(blastpAccID_output) 
for ID in AccID:
	subprocess.call("patmatmotifs -auto -sequence " + pullseq_output + " -rdirectory_outfile " + dir + " -sid1 " + ID,shell=True)
