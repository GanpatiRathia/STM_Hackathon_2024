from Plotting import Owner_VS_Status
from Plotting import Category_VS_Status
from Plotting import Week_VS_Status
from Plotting import Selected_Category_VS_Week
from Plotting import Selected_Owner_VS_Work_week
from Data_path import directory_path
from Plotting import Perito
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


## plotting Owner_vs_Status

object_owner_vs_status = Owner_VS_Status.Owner_VS_Status()
object_owner_vs_status.Owner_VS_Status_plot()

## plotting Category_VS_Status

object_category_vs_status = Category_VS_Status.Category_VS_Status()
object_category_vs_status.Category_VS_Status_plot()


## plotting Week_Vs_Status

object_week_vs_status = Week_VS_Status.Week_VS_Status()
object_week_vs_status.Week_VS_Status_plot()

## plotting Selected Category_VS_Week

selected_category = "reference"
# Assuming you have imported the necessary libraries and defined the `Selected_Category_VS_Week` class

# Create an instance of Selected_Category_VS_Week with the selected category
object_Selected_Category_VS_Week = Selected_Category_VS_Week.Selected_Category_VS_Week(selected_category)

# Call the Selected_Category_VS_Week_plot method
object_Selected_Category_VS_Week.Selected_Category_VS_Week_plot()


## plotting Selected Owner_VS_work_Week

selected_owner = "Sachin S1"
# Assuming you have imported the necessary libraries and defined the `Selected_Category_VS_Week` class

# Create an instance of Selected Owner_VS_work_Week with the selected owner
object_Selected_Owner_VS_Work_Week = Selected_Owner_VS_Work_week.Selected_Owner_VS_Work_week(selected_owner)

# Call the elected Owner_VS_work_Week_plot method
object_Selected_Owner_VS_Work_Week.Selected_Owner_VS_Week_plot()



##-------------------------------------------------------------------------------------------------##

sam_path_cov = directory_path.regression_data_path()
reg_path_cov = sam_path_cov.directory_path_coverage_file()

outc = pd.DataFrame()


month_dict = {
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
    'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
}



# Function to extract date from log column
def extract_date_cov(REPORT_PATH):
    match = re.search(r'\w{3}\d{6}', REPORT_PATH)
    if match:
        date = match.group()
        month = month_dict[date[:3]]  # Get month abbreviation and convert to month number
        day = date[3:5]  # Get day
        year = date[5:]  # Get year
        formatted_date = f"{year[2:]}-{month}-{day}"
        return formatted_date
    else:
        return None

samc_path = reg_path_cov

for filename in os.listdir(samc_path):
    print(filename)
    dfc = pd.read_csv(samc_path+"/"+filename,on_bad_lines='skip')
    dfc['REPORT PATH'] = dfc['REPORT PATH'].replace('-', np.nan)
    dfc=dfc.dropna()
    short=pd.DataFrame()
    dfc['DateTime'] = dfc['REPORT PATH'].apply(extract_date_cov)
    dfc['DateTime'] = pd.to_datetime(dfc['DateTime'] )
    dfc['Week_Number'] = dfc['DateTime'].dt.isocalendar().week
    short = dfc[["NAME","OWNER","SCORE","DateTime","Week_Number"]]
    outc = pd.concat([outc, short], ignore_index=True)
    #print(outc)

outc['SCORE'] = outc['SCORE'].str.replace(r'[^0-9.]', '').astype(float)
plot=outc.groupby('Week_Number')['SCORE'].mean().reset_index()
plot.set_index('Week_Number').plot(kind='line', stacked=True, color=['steelblue', 'red'])
plt.show()




## plotting Coverage_Score_VS_Work_week


## plotting Perito

object_perito = Perito.perito()
object_perito.perito()



























