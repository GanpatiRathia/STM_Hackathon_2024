import pandas as pd
import os
from Read_Coverage_Data import read_coverage_data
from Read_Regression_Data import read_regression_data
from Data_path import directory_path


def ingest_data(directory_path):
  """
  Ingests data from all CSV files in the specified directory.

  Args:
    directory_path: Path to the directory containing the CSV files.

  Returns:
    A dictionary containing separate DataFrames for regression and coverage data.
  """
  data = {}
  for filename in os.listdir(directory_path):
    if filename.startswith("REGR_STATUS"):
      filepath = os.path.join(directory_path, filename)
      data["regression"] = read_regression_data(filepath)
    elif filename.startswith("COVERAGE"):
      filepath = os.path.join(directory_path, filename)
      data["coverage"] = read_coverage_data(filepath)
  return data