from Plotting import Owner_VS_Status
from Plotting import Category_VS_Status
from Plotting import Week_VS_Status
from Plotting import Selected_Category_VS_Week
from Plotting import Selected_Owner_VS_Work_week
from Data_path import directory_path
from matplotlib.ticker import PercentFormatter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re


sam_path = directory_path.regression_data_path()
reg_path = sam_path.directory_path_regression_file()

# Initialize an empty DataFrame to store the results
result_df = pd.DataFrame()

def extract_date(log):
    match = re.search(r'(\d{2}_\d{2}_\d{2})', log)
    if match:
        date = match.group()
        formatted_date = date.replace('_', '-')
        return formatted_date
    else:
        return None

sam_path = reg_path

for filename in os.listdir(sam_path):
    file_path = os.path.join(sam_path, filename)
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        #print(filename)
        df = pd.read_csv(sam_path + "\\" + filename, on_bad_lines='skip')
        df['DateTime'] = extract_date(df.iloc[0]['Log'])
        #print(df.iloc[0]['DateTime'])
        df['Status'] = df['Status'].replace(['make_error', 'timeout', 'tool_failure', 'expected_failure'], 'failed')
        short = df.groupby('Category')['Status'].value_counts().unstack(fill_value=0).reset_index()
        owners = df.groupby('Category')['Owner'].first().reset_index(name='Owner')
        short = pd.merge(short, owners, on='Category')
        short["DateTime"] = df.iloc[0]['DateTime']
        #print(short)
        result_df = pd.concat([result_df, short], ignore_index=True)
    else:
        print(f"File '{filename}' is empty")

#pa=pd.DataFrame()


class perito():
    def __init__(self):
        pass
    def perito(self):
        pa = pd.DataFrame()
        pa['Category'] = result_df['Category']
        pa['passed'] = result_df['passed']
        pa['failed'] = result_df['failed']
        pa = pa.groupby(['Category'], as_index=False)[["passed", "failed"]].sum()

        pa = pa.sort_values('failed', ascending=False).reset_index()

        tf = pa['failed'].sum()

        pa["fail_percent"] = (pa['failed'] / tf) * 100

        plot = pa[(pa.fail_percent > 1.0)]

        #plt.bar(plot['Category'], plot['fail_percent'])
        #plt.xticks(rotation=90)

        pa["cumsum"] = pa['failed'].cumsum()

        pa = pa[(pa.failed > 100)]

        pa['pareto'] = 100 * pa.failed.cumsum() / pa.failed.sum()

        ca = pa['Category']
        l = pa['fail_percent']

        ca = ca.tolist()
        l = l.tolist()

        fig, ax = plt.subplots()
        ax.bar(pa.index, pa['fail_percent'])

        # add cumulative percentage line to plot
        ax2 = ax.twinx()
        ax2.plot(pa['Category'], pa['pareto'], color='orange', marker="D", ms=4)
        ax2.yaxis.set_major_formatter(PercentFormatter())
        ax2.axhline(y=20, color='r', linestyle='--')
        # arr=pd['Category']
        # ax.xaxis.set_ticks(l)
        # ax.set_xticks(l)
        # ax.set_xticklabels(ca, rotation=90)
        ax.xaxis.set_ticklabels(ca, rotation=90)
        # ax2.set_xticks(ticks, minor=False)
        # ax2.xticks(rotation = 90)
        
        # specify axis colors
        ax.tick_params(axis='y')
        ax2.tick_params(axis='y')
        ax.set_title('Perito Analysis')
        # display Pareto chart
        plt.show()







