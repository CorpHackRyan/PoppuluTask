import csv
import os
from os import path
from datetime import datetime
import pandas as pd  # pandas module for ease of use to navigate individual column data in csv files

poppulo_csv_file = "poppulo_techtask.csv"

if not path.exists(poppulo_csv_file):
    print(os.getcwd() + "/" + poppulo_csv_file + " does not exist and program cannot proceed.")
    exit()


####################################################################################################################
# 2. Programmatically create a subdirectory named year-month-date where YMD is specific to the day program is run #
####################################################################################################################
dir_name = datetime.today().strftime('%Y-%m-%d')

try:
    os.mkdir(dir_name)
    print("QUESTION #2:  " + os.getcwd() + "/" + dir_name + " directory was created.")
except OSError as folder_error:
    print(folder_error)


##################################################################################################
# 3. Generate a text file, named "headers.txt", containing a string of the provided headers only #
##################################################################################################
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

            print("QUESTION #3:  Header information gathered from: " + poppulo_csv_file + " file was:", header_row_from_csv)

except OSError as file_error:
    print(file_error)


#######################################################################################################
# 4. Generate a separate CSV file per 'Department' value found within the provided CSV file, name     #
#    the CSV file 'departmentValue.csv', where departmentValue is the actual Department value itself. #
########################################################################################################

try:
    csv_readfile = pd.read_csv(poppulo_csv_file)
    dept_column = csv_readfile.Department
    dept_column = set(dept_column)  # Remove all duplicates

    for each_dept in dept_column:
        out_file = open(each_dept + ".csv", "w+")

    print("QUESTION #4:  The following .csv files were created: ", dept_column)

except OSError as file_error:
    print(file_error)


#######################################################################################################
#  5. Generate a separate CSV file named 'no_countries.csv', where the 'Country' field is             #
#     omitted from the file entirely.                                                                 #
#######################################################################################################

try:
    country_omitted_filename = "no_countries.csv"
    cols_to_use = ["Email", "Surname", "FirstName", "Department"]
    country_omitted = pd.read_csv(poppulo_csv_file, usecols=cols_to_use)
    country_omitted.to_csv(country_omitted_filename, sep=',', index=False)  # index=False req'd to eliminate prepending a ',' to data set

    print("QUESTION #5:  " + country_omitted_filename + " has been created with the following data")
    print(country_omitted)

except OSError as file_error:
    print(file_error)
