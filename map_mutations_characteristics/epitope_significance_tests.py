import pandas as pd
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('C:\\Users\\haile\\OneDrive\\Desktop\\MIT\\urop\\week 2\\all_epitopes.csv')

# Convert 'seen_date' to datetime and 'is_public' to a binary variable
df['seen_date'] = pd.to_datetime(df['seen_date'], errors='coerce')
df['is_public'] = df['is_public'].map({'yes': 1, 'no': 0})

# Crate bins for evescape_score as 'high' and 'low' based on the median
evescape_median = df['evescape_score'].median()
df['evescape_score_high_low'] = pd.cut(df['evescape_score'], bins=[-float('inf'), evescape_median, float('inf')], labels=[0, 1])

# Bins for seen_date as 'early' and 'late' based on a cutoff date (here, it's the median date of non-NaT entries)
seen_date_cutoff = df['seen_date'].dropna().median()
df['seen_date_early_late'] = (df['seen_date'] < seen_date_cutoff).astype(int)

# Perform chi-square test for evescape_score and is_public
chi2_score, p_score, dof_score, ex_score = chi2_contingency(pd.crosstab(df['evescape_score_high_low'], df['is_public']))

# Perform chi-square test for seen_date and is_public
chi2_date, p_date, dof_date, ex_date = chi2_contingency(pd.crosstab(df['seen_date_early_late'], df['is_public']))

# Print out the chi-square values and interpretations
print(f"Chi-square test for evescape_score and public epitopes: chi2 = {chi2_score}, p-value = {p_score}")
if p_score < 0.05:
    print("There is a significant association between evescape score and public epitopes.")
else:
    print("There is no significant association between evescape score and public epitopes.")

print(f"\nChi-square test for seen_date and public epitopes: chi2 = {chi2_date}, p-value = {p_date}")
if p_date < 0.05:
    print("There is a significant association between seen date and public epitopes.")
else:
    print("There is no significant association between seen date and public epitopes.")
