import pandas as pd
import os
import sys
sys.path.append('space_analyser')
from lib.database import Database
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger("logger_name")

d = Database(
  os.environ.get("URL"),
  os.environ.get("USR"),
  os.environ.get("PW"),
  os.environ.get("DB"),
  logger
)

# https://stackoverflow.com/a/1094933
def sizeof_fmt(num, suffix='B'):
  for unit in ['', 'K','M','G','T','P','E','Z']:
    if abs(num) < 1024.0:
      return "%3.1f%s%s" % (num, unit, suffix)
    num /= 1024.0
  return "%.1f%s%s" % (num, 'Y', suffix)

def align_first_col(du_message):
  max_len = 0
  du_message_rows = du_message.split("\n")
  for line in du_message_rows:
    current_len = len(line.split("\t")[0])
    if current_len > max_len:
      max_len = current_len
  aligned_row_list = []
  for line in du_message_rows:
    first_col = line.split("\t")[0]
    second_col = line.split("\t")[1]
    new_firs_col = " " * (max_len - len(first_col)) + first_col
    aligned_row_list.append(new_firs_col + "\t" + second_col)
  aligned_du_message = "\n".join(aligned_row_list)
  return(aligned_du_message)

def get_du_table(root_folder="'/Users/cheshic/dev/repos/TOBIAS'"):
  df = d.get_size_summary(root_folder)
  return_dict = {}
  for row_idx in range(len(df)):
    return_dict[df.iloc[row_idx]["file_name"]] = df.iloc[row_idx]["size"]
  return(return_dict)

#OLD / TEMPORARY FUNCTIONS
# def read_data_frame():
#   return(pd.read_csv("test_data/test-set-2.csv"))

# def get_du_table():
#   return_dict = {}
#   with open("test_data/du.out", "r") as du_in:
#     for line in du_in:
#       row = line.strip().split()
#       return_dict[row[-1].replace("./", "")] = float(row[0])
#   return(return_dict)

# def get_du_table():
#   depth = 1
#   all_data = read_data_frame()
#   depth_folder_subset = all_data.loc[all_data.folder].loc[all_data.depth==depth]
#   return_dict = {}
#   for row_idx in range(len(depth_folder_subset)):
#     return_dict[depth_folder_subset.iloc[row_idx]["name"]] = depth_folder_subset.iloc[row_idx]["size"]
#   return(return_dict)
