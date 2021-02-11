import pandas as pd
import os
import sys
sys.path.append('space_analyser')
from lib.database import Database
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger("logger_name")

# d = Database(
#   os.environ.get("URL"),
#   os.environ.get("USR"),
#   os.environ.get("PW"),
#   os.environ.get("DB"),
#   logger
# )

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

# def get_du_table(root_folder="'/Users/cheshic/dev/repos/arshamg-scrnaseq-wgan'"):
#   df = d.get_size_summary(root_folder)
#   return_dict = {}
#   for row_idx in range(len(df)):
#     return_dict[df.iloc[row_idx]["file_name"]] = df.iloc[row_idx]["size"]
#   return(return_dict)

def get_top_n_dup_md5(n=1):
  data_table = read_data_frame()
  count_dict = {}
  size_dict = {}
  for index, row in data_table.iterrows():
    if pd.notna(row["md5"]):
      count_dict.setdefault(row["md5"], 0)
      count_dict[row["md5"]] += 1
      size_dict.setdefault(row["md5"], row["size"])
  count_table = pd.DataFrame({
    "md5": count_dict.keys(),
    "count": count_dict.values(),
    "size": [size_dict[md5] for md5 in count_dict.keys()]
  })
  # Assumes deleting all but one copy of the file
  count_table["potential_saving"] = count_table["size"] * (count_table["count"] - 1)
  top_n_count_table = count_table.sort_values("potential_saving", ascending=False)[0:n]
  return_list = []
  for index, row in top_n_count_table.iterrows():
    row_dict = row.to_dict()
    data_table_subset = data_table.loc[data_table["md5"] == row["md5"]]
    row_dict["paths"] = list(data_table_subset["path"])
    row_dict["names"] = list(set(data_table_subset["name"] + "." + data_table_subset["extension"]))
    return_list.append(row_dict)
  return(return_list)

def get_pretty_recommentations(n=1):
  info = get_top_n_dup_md5(n)
  blocks = []
  for idx, rec_dict in enumerate(info):
    blurb_str = ""
    blurb_str += (
      "*Top {rank} Recommendation*\n"
      "A file with the name(s) {names} "
      "is present {count} times and takes up {size} disk space each.\n"
      "Using a single, shared resource would save {potential_saving}.\n"
      "The paths to these files are:\n"
    ).format(
      rank=idx+1,
      names='/'.join(["`{name}`".format(name=name) for name in rec_dict["names"]]),
      count=rec_dict["count"],
      size=sizeof_fmt(rec_dict["size"]),
      potential_saving=sizeof_fmt(rec_dict["potential_saving"])
    )
    path_str = "```#paths to {names}\n".format(
      names='/'.join(["{name}".format(name=name) for name in rec_dict["names"]])
    )
    for path in rec_dict["paths"]:
      path_str += "{path}\n".format(path=path)
    path_str += "```"
    blocks.append({"blurb_str": blurb_str, "path_str": path_str})
  return(blocks)

#OLD / TEMPORARY FUNCTIONS
def read_data_frame():
  return(pd.read_csv("slack_app/test_data/test-set-2.csv"))

# def get_du_table():
#   return_dict = {}
#   with open("test_data/du.out", "r") as du_in:
#     for line in du_in:
#       row = line.strip().split()
#       return_dict[row[-1].replace("./", "")] = float(row[0])
#   return(return_dict)

def get_du_table():
  depth = 1
  all_data = read_data_frame()
  depth_folder_subset = all_data.loc[all_data.folder].loc[all_data.depth==depth]
  return_dict = {}
  for row_idx in range(len(depth_folder_subset)):
    return_dict[depth_folder_subset.iloc[row_idx]["name"]] = depth_folder_subset.iloc[row_idx]["size"]
  return(return_dict)
