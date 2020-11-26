import pandas as pd

#TEMPORARY FUNCTION
def get_du_table_old():
  return_dict = {}
  with open("test_data/du.out", "r") as du_in:
    for line in du_in:
      row = line.strip().split()
      return_dict[row[-1].replace("./", "")] = float(row[0])
  return(return_dict)

# https://stackoverflow.com/a/1094933
def sizeof_fmt(num, suffix='B'):
  for unit in ['K','M','G','T','P','E','Z']:
    if abs(num) < 1024.0:
      return "%3.1f%s%s" % (num, unit, suffix)
    num /= 1024.0
  return "%.1f%s%s" % (num, 'Y', suffix)

def read_data_frame():
  return(pd.read_csv("test_data/test-set-2.csv"))

def get_du_table():
  depth = 1
  all_data = read_data_frame()
  depth_folder_subset = all_data.loc[all_data.folder].loc[all_data.depth==depth]
  return_dict = {}
  for row_idx in range(len(depth_folder_subset)):
    return_dict[depth_folder_subset.iloc[row_idx]["name"]] = depth_folder_subset.iloc[row_idx]["size"]
  return(return_dict)
