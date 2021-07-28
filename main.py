import csv
import os
from datetime import datetime
import pandas as pd  # Using pandas module for ease of use to  navigate certain columns in csv files

poppulo_csv_file = "poppulo_techtask.csv"

####################################################################################################################
#  2. Programmatically create a subdirectory named year-month-date where YMD is specific to the day program is run #
####################################################################################################################
dir_name = datetime.today().strftime('%Y-%m-%d')

try:
    os.mkdir(dir_name)
except OSError as folder_error:
    print(folder_error)


# #################################################################################################
#  3. Generate a text file, named "headers.txt", containing a string of the provided headers only #
# #################################################################################################
headers_txt_file = "headers.txt"

try:
    with open(headers_txt_file, "w+") as headers_outfile:
        with open(poppulo_csv_file, 'r') as csv_readfile:
            csv_reader = csv.reader(csv_readfile, delimiter=",")
            header_row_from_csv = next(csv_reader)
            for idx, value in enumerate(header_row_from_csv):
                if idx == len(header_row_from_csv) - 1:
                    headers_outfile.write(value)
                else:
                    headers_outfile.write(value + ",")

            print("Header information gathered from: " + poppulo_csv_file + " file was:", header_row_from_csv)

except OSError as file_error:
    print(file_error)


# ######################################################################################################
#  4. Generate a separate CSV file per 'Department' value found within the provided CSV file, name     #
#     the CSV file 'departmentValue.csv', where departmentValue is the actual Department value itself. #
########################################################################################################

# Since there is a lot of files, I decided to move them into their own directory.
dept_dir_name = "Department"

try:
    os.mkdir(dept_dir_name)

except OSError as folder_error:
    print(folder_error)

csv_readfile = pd.read_csv(poppulo_csv_file)
dept_column = csv_readfile.Department
dept_column = set(dept_column)  # Remove all duplicates
print(dept_column)
