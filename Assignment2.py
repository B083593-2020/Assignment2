#! /usr/bin/python3

import os,sys,subprocess,shutil
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

taxonomyID="txid8782" #Enter query taxonomy ID in quotes
protein="glucose-6-phosphatase" #Enter query protein in quotes 
subprocess.call("esearch -db Protein -query '" + taxonomyID + "[Organism:exp] AND " + protein + "[Protein])' | efetch -format fasta > esearch.output",shell=True)

subprocess.call("cons -sequence esearch.output -outseq cons.output", shell=True) #Command outputs a sequence that best represents the input sequences

subprocess.call("makeblastdb -in esearch.output -dbtype prot -out blastdb.output", shell=True) #Bash database created in preparation of blastp

num_alignments="250" #value set to 250 but user can change 
subprocess.call("blastp -db blastdb.output -query cons.output -num_alignments " + num_alignments + " -outfmt '6 sseqid' > blastp.output", shell=True)

#plotcon reads a sequence alignment and draws a plot of the sequence conservation within windows over the alignment.
window_size="6" #Number of columns to average alignment quality over. The larger this value is, the smoother the plot will be. (4 minimum) 
plotcon_output="plot.output" #Option for user to name output plot  
subprocess.call("plotcon -sequences blastp.output -graph cps -winsize " + window_size +" > " + plotcon_output ,shell=True) 

#Command pulls sequences from original list of protein sequences against for the accession numbers of interest
subprocess.call("/localdisk/data/BPSM/Assignment2/pullseq -i esearch.output -n blastp.output > pullseq.output", shell=True)

#Motif directory created for patmatmotifs outputs
dir = "motifs"
if os.path.exists(dir):
	shutil.rmtree(dir)
os.makedirs(dir)   

AccID = open("blastp.output") 
for ID in AccID:
	subprocess.call("patmatmotifs -auto -sequence pullseq.output -rdirectory_outfile " + dir + " -sid1 " + ID,shell=True)
