# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from statsmodels.sandbox.stats.multicomp import multipletests
from itertools import combinations


# My hypothesis
# H0: There is no difference in the Click-Through-Rate (CTR) of the various versions of the website
# HA: There is a difference in the CTR between the various versions of the website


help_source = '/content/drive/MyDrive/Colab Notebooks/CrazyEgg/all_versions/Help.csv'
connect_source ='/content/drive/MyDrive/Colab Notebooks/CrazyEgg/all_versions/Connect.csv'
interact_source = '/content/drive/MyDrive/Colab Notebooks/CrazyEgg/all_versions/Interact.csv'
learn_source = '/content/drive/MyDrive/Colab Notebooks/CrazyEgg/all_versions/Learn.csv'
services_source = '/content/drive/MyDrive/Colab Notebooks/CrazyEgg/all_versions/Services.csv'

# read in my data
help_df = pd.read_csv(help_source, sep =',')
connect_df = pd.read_csv(connect_source, sep =',')
learn_df = pd.read_csv(learn_source, sep =',')
interact_df = pd.read_csv(interact_source, sep =',')
services_df = pd.read_csv(services_source, sep =',')

help_no = int(help_df[help_df['Name']=='HELP']['No. clicks'])
connect_no =int(connect_df[connect_df['Name']=='CONNECT']['No. clicks'])
learn_no = int(learn_df[learn_df['Name']=='LEARN']['No. clicks'])
interact_no = int(interact_df[interact_df['Name']=='INTERACT']['No. clicks'])
services_no = int(services_df[services_df['Name']=='SERVICES']['No. clicks'])

# i save the number of clicks for the button for each version in a list
clicks = [help_no, connect_no, learn_no, interact_no, services_no]
help_visit = 3180
connect_visit = 2742
learn_visit = 2747
interact_visit = 10283
service_visit = 2064

# i store the total number of site visit for each version in a list
visits = [help_visit, connect_visit, learn_visit, interact_visit, service_visit]

# creating a dataframe to store the click-through-rate (CTR) for each version
click_rate = pd.DataFrame([['Help', 'Connect', 'Learn', 'Interact', 'Services'],[round(i/j,4) for i,j in zip(clicks, visits)]],
                          index = ['Variable', 'CTR']).T

# creating a data frame to store the number of clicks, and non-clicks for each version so that i can run the chi-squared test
records = pd.DataFrame([clicks, [j - i for i,j in zip(clicks, visits)]],
                       columns =['Help', 'Connect', 'Learn', 'Interact', 'Services'],
                       index = ['clicks', 'No_clicks'])


# created a function to manually calculate for chi-squared and check for significance 
def chi_square_values(observations, alpha=0.05):
  '''
  observations is the table that i am inspecting
  alpha is is my significance level, default at 0.05
  '''
  expected = []
  for row in range(len(observations)):
    expected.append([observations.iloc[row].mean()] * len(observations.columns))

  chi_squared = 0
  degrees_of_freedom = (observations.shape[0] - 1) * (observations.shape[1] - 1)

  for row1, (_, row2) in zip(expected, observations.iterrows()):
    for i,j in zip(row1, row2):
      output = (j - i)**2/i
      chi_squared += output

  table_num = float(input(f'What is your chi_squared statistic number from the table?\nCheck at alpha {alpha} and DOF at {degrees_of_freedom}: '))

  if chi_squared > table_num:
    return 'Null Hypothesis rejected'
  else:
    return 'Insufficient evidence to reject Null Hypothesis'


# to calculate using scipy
alpha = 0.05
chisq, pvalue, df, expected = chi2_contingency(records)

if pvalue < alpha:
  print('Null Hypothesis rejected')
else:
  print('Insufficient evidence to reject Null Hypothesis')


def get_asterisks_for_pval(pvalue, alpha=0.05):
    """Receives the p-value and returns asterisks string
    to do it like other coding languges (R).
    i set the alpha to 0.01 as default for my posthoc"""

    if pvalue > alpha:  # bigger than alpha
        p_text = "ns" # ns - not significant
    # following the standards in scientifc publications for the asterisk.
    # i understood it as the more the asterisk, the more its significance
    elif pvalue < 1e-4:
        p_text = '****'
    elif pvalue < 1e-3:
        p_text = '***'
    elif pvalue < 1e-2:
        p_text = '**'
    else:
        p_text = '*'
    return p_text

# to do a post hoc
# i did a pairwise test 

pvalue_list =[] # to create a list to store my pvalues
print("Significance results:")
for comb in all_combinations:
    # subset records table into a dataframe containing only the pair "comb"
    new_df = records[list(comb)]
    # running chi-square test
    chi2, p, dof, ex = chi2_contingency(new_df, correction=False)
    print(f"Chi2 result for pair {comb}: {chi2}, p-value: {p}, {get_asterisks_for_pval(p)}")
    pvalue_list.append(p)


# bonferroni test to correct for multiple-comparison 
reject_list, corrected_p_vals = multipletests(pvalue_list, alpha=0.01, method='bonferroni')[:2]

# to print out the result of my post hoc test
print("original p-value\tcorrected p-value\treject H0?")
for p_val, corr_p_val, reject in zip(pvalue_list, corrected_p_vals, reject_list):
    print(p_val, "\t", corr_p_val, "\t", reject)


# i merged my code to create a function using all the code and structured the code a bit to to have a nice outlook

def chisq_and_posthoc_corrected(df, correction_method='bonferroni', alpha=0.05):
  '''correction method is set to bonferroni as default
  alpha is set to 0.05 as my default'''
  chisq, pvalue, dff, expected = chi2_contingency(df)
  hypothesis = 'Null Hypothesis rejected' if pvalue < alpha else 'Insufficient evidence to reject Null Hypothesis'
  print(f'{hypothesis}\n')
  all_combinations = list(combinations(df.columns, 2))

  pvalue_list =[] # to create a list to store my pvalues

  for comb in all_combinations:
      # subset records table into a dataframe containing only the pair "comb"
      new_df = records[list(comb)]
      # running chi-square test
      chi2, p, dof, ex = chi2_contingency(new_df, correction=False)
      print(f"Result for pair {str(comb).ljust(25)} ---| chi-square: {str(chi2).ljust(20)} | p-value: {p}, {get_asterisks_for_pval(p)}") 
      pvalue_list.append(p)

  reject_list, corrected_p_vals = multipletests(pvalue_list, alpha=alpha/(len(all_combinations)), method=correction_method)[:2]

  print('\nPOST-HOC TEST RESULTS')
  print(f'{str("original p-value").ljust(24)} | {str("corrected p-value").ljust(24)} | {"reject H0?"}')
  for p_val, corr_p_val, reject in zip(pvalue_list, corrected_p_vals, reject_list):
      print(f'{str(p_val).ljust(24)} | {str(corr_p_val).ljust(24)} | {str(reject)}')





