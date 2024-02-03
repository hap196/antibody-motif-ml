import pandas as pd
import numpy as np
import seaborn as sns

igg = pd.read_excel("/n/groups/marks/projects/public_epitope/data/elledge/Shrock_2020/igg_aaa_scanning_s11.xlsx")

"""
For the IgG data, it adds a new column num_patients_igg that counts how many patients have a value less than or equal to 0.5 for each mutant (across all columns starting from the third column). This is done using the le() method (less than or equal to) and sum() method along the axis=1, which refers to the rows.
"""
igg['num_patients_igg'] = igg[igg.columns[2:]].le(0.5,axis=0).sum(axis=1)
igg["pos"] = igg["Unnamed: 0"]

iga = pd.read_excel("/n/groups/marks/projects/public_epitope/data/elledge/Shrock_2020/iga_aaa_scanning_s12.xlsx")
iga['num_patients_iga'] = iga[iga.columns[2:]].le(0.5,axis=0).sum(axis=1)

"""
It extracts the position data from an unnamed column (presumably the first column) and renames it as pos for both IgG and IgA datasets.
"""
iga["pos"] = iga["Unnamed: 0"]

"""
The script merges the two datasets on the pos column to combine the number of patients' data for both IgG and IgA.
"""
ig = iga[["num_patients_iga","pos"]].merge(igg[["num_patients_igg","pos"]], on ="pos")

"""
It creates a new column num_patients that contains the maximum value between num_patients_igg and num_patients_iga for each position. This is likely used to find the highest number of patients with a response to either IgG or IgA for each mutant.
"""
ig["num_patients"] = ig[["num_patients_iga","num_patients_igg"]].max(axis="columns")

sns.lineplot(x='pos', y='num_patients', data=ig)

ig.to_csv("../../../../data/elledge/Shrock_2020/aaa_scanning_processed.csv")