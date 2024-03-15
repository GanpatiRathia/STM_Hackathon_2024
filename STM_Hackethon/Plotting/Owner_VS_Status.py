from Data_path import directory_path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

from application_logging.logger import App_Logger

log_file = open("Owner_VS_Status log.txt","a+")

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
        pass
        #print(f"File '{filename}' is empty or doesn't exist.")



class Owner_VS_Status():
    def __init__(self):
        self.logger = App_Logger()

    def Owner_VS_Status_plot(self):
        self.logger.log(log_file, "Owner_VS_Status plotting has started !!")
        plot = result_df.groupby(['Owner'], as_index=False)[["passed", "failed"]].sum()

        # Set seaborn style
        sns.set(style='white')
        self.logger.log(log_file, "Works Fine , The flow is Good to Go into next step")

        # Plot the data
        plot.set_index('Owner').plot(kind='bar', stacked=True, color=['steelblue', 'red'])

        self.logger.log(log_file, "Great !! The beginning of the graph plotting has started")

        # Show the plot
        plt.show()

        self.logger.log(log_file, "Category_VS_Status plotting ended!!")


