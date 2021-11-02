from lisa import FromGenes
import os
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='DeepMAPS - Run LISA2')
 
parser.add_argument("--path", help="Gene module path", default="")
args = parser.parse_args()

def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.txt':
                L.append(os.path.join(root, file))
    return L


#batch1_file = file_name('/home/wan268/deepmaps/data/lymph_14k')
batch1_file = file_name(args.path)


lisa_test = FromGenes('hg38', rp_map='enhanced_10K',
                      assays=['Direct', 'DNase', 'H3K27ac'], isd_method='chipseq', verbose=1)
for i in batch1_file:
    f = open(i)
    linesList = f.readlines()
    a = []
    for line in linesList:
        a.append(line.strip())

    up_results, up_metadata = lisa_test.predict(
        a, num_background_genes=3000, background_strategy='regulatory')
    up_results = pd.DataFrame(up_results.to_dict())
    up_results.to_csv(i+'.csv', index=False, header=True)
