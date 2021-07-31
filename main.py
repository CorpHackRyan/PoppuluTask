# Some other ideas that would take longer to implement could prove useful:
#   a) Break some operations out into functions to pass parameters into.
#   b) When writing xml template, instead of repeating writing of the same data in different sections,
#      create a function to do this instead which will some redundancy in code.
#   c) Check to see if files exist in case and handle accordingly


import csv
import os
from os import path
from datetime import datetime
import pandas as pd            # pandas module for ease of use to navigate individual column data in csv files
import base64                  # base64 module to encode department csv files and embed into their respective xml files

poppulo_csv_file = "poppulo_techtask.csv"
delimiter = ","

if not path.exists(poppulo_csv_file):
    print(os.getcwd() + "/" + poppulo_csv_file + " does not exist and program cannot proceed.")
    exit()


####################################################################################################################
# 2. Programmatically create a subdirectory named year-month-date where YMD is specific to the day program is run #
####################################################################################################################
dir_name = datetime.today().strftime('%Y-%m-%d')

try:
    os.mkdir(dir_name)
    print("\nQUESTION #2:  " + os.getcwd() + "/" + dir_name + " directory was created.")

except OSError as folder_error:
    print(folder_error)


##################################################################################################
# 3. Generate a text file, named "headers.txt", containing a string of the provided headers only #
##################################################################################################
headers_txt_file = "headers.txt"

# Using the built in csv_reader for python for experimentation versus pandas csv module
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

            print("\nQUESTION #3:  Header information gathered from: " + poppulo_csv_file + " file was:",
                  header_row_from_csv)

except OSError as file_error:
    print(file_error)


#######################################################################################################
# 4. Generate a separate CSV file per 'Department' value found within the provided CSV file, name     #
#    the CSV file 'departmentValue.csv', where departmentValue is the actual Department value itself. #
#######################################################################################################

try:
    csv_readfile = pd.read_csv(poppulo_csv_file)
    dept_column = csv_readfile.Department

    for idx, each_row in csv_readfile.iterrows():
        with open(each_row.Department + ".csv", "+a") as out_file:
            out_file.write(delimiter.join(each_row) + "\n")

    dept_column = csv_readfile.Department
    dept_column = set(dept_column)  # Remove all duplicates
    print("\nQUESTION #4: The following .csv files were created with their corresponding values: " + str(dept_column))

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

    # index=False required to eliminate prepending a ',' to the data set
    country_omitted.to_csv(country_omitted_filename, sep=',', index=False)

    print("\nQUESTION #5: " + country_omitted_filename + " has been created with the following data")
    print(country_omitted)

except OSError as file_error:
    print(file_error)


#######################################################################################################
#  6. Generate a 'Master' XML file named 'master.xml', containing all of the data found               #
#     within the provided CSV file, using the XML template seen below.                                #
#######################################################################################################

try:
    master_XML_filename = "master.xml"
    out_file = open(master_XML_filename, "+w")
    csv_readfile = pd.read_csv(poppulo_csv_file)
    delimiter = ","

    out_file.write("<subscriber_import_job>\n")
    out_file.write("\t<accept_terms>true</accept_terms>\n")
    out_file.write("\t<reactivate_api_removed>false</reactivate_api_removed>\n")
    out_file.write("\t<reactivate_admin_removed>true</reactivate_admin_removed>\n")
    out_file.write("\t<reactivate_bounced_removed>false</reactivate_bounced_removed>\n")
    out_file.write("\t<tags>\n")
    out_file.write('\t\t<tag name="Some Tag" />\n')
    out_file.write("\t</tags>\n")
    out_file.write("\t<subscriber_data>\n")

    # Using the header previously extracted from question #3
    out_file.write("\t\t<columns>" + delimiter.join(header_row_from_csv) + "</columns>\n")

    out_file.write("\t\t<skip_first_line>true</skip_first_line>\n")
    out_file.write("\t\t<field_separator>comma</field_separator>\n")
    out_file.write("\t\t<data>\n")

    # Using the header previously extracted from question #3
    out_file.write("\t\t\t" + delimiter.join(header_row_from_csv) + "\n")

    # Write data to master_XML_filename ('master.xml') from csv_readfile ('poppulu_techtask.csv')
    with open(poppulo_csv_file, 'r') as readonly_poppulu_data:
        csv_reader = csv.reader(readonly_poppulu_data)
        header = next(readonly_poppulu_data)  # Skip the header
        for each_row in csv_reader:
            out_file.write("\t\t\t" + delimiter.join(each_row) + "\n")

    #######################################################################################################
    # FROM QUESTION 8: embed the master csv file in the data section
    #######################################################################################################
    with open(poppulo_csv_file, "rb") as master_csv_data:
        master_csv_encoded = base64.b64encode(master_csv_data.read())

    out_file.write("\t\t\t<embed>" + str(master_csv_encoded.decode('utf-8')) + "</embed>\n")
    out_file.write("\t\t</data>\n")
    out_file.write("\t</subscriber_data>\n")
    out_file.write("</subscriber_import_job>\n")

    print("\nQUESTION #6: " + master_XML_filename + " template has been successfully created and populated from: "
          + poppulo_csv_file)

except OSError as file_error:
    print(file_error)


#######################################################################################################
#   7. Generate a separate 'Child' XML file per 'Department' value, using the created CSV             #
#   files (see point 5 above), named 'departmentValue.xml', using the XML template                    #
#   seen below.                                                                                       #
#######################################################################################################

try:
    # Write out top half of XML template to all department files
    for each_dept in dept_column:
        with open(str(each_dept) + ".xml", "+w") as out_file:
            out_file.write("<subscriber_import_job>\n")
            out_file.write("\t<accept_terms>true</accept_terms>\n")
            out_file.write("\t<reactivate_api_removed>false</reactivate_api_removed>\n")
            out_file.write("\t<reactivate_admin_removed>true</reactivate_admin_removed>\n")
            out_file.write("\t<reactivate_bounced_removed>false</reactivate_bounced_removed>\n")
            out_file.write("\t<tags>\n")
            out_file.write('\t\t<tag name="Some Tag" />\n')
            out_file.write("\t</tags>\n")
            out_file.write("\t<subscriber_data>\n")

            # Using the headers previously extracted from question #3
            out_file.write("\t\t<columns>" + delimiter.join(header_row_from_csv) + "</columns>\n")

            out_file.write("\t\t<skip_first_line>true</skip_first_line>\n")
            out_file.write("\t\t<field_separator>comma</field_separator>\n")
            out_file.write("\t\t<data>\n")

            # Using the headers previously extracted from question #3
            out_file.write("\t\t\t" + delimiter.join(header_row_from_csv) + "\n")

    # Write data to individual 'child' (departmental) xml files from the .csv files generated from question 4
    for each_dept in dept_column:
        csv_readfile = pd.read_csv(str(each_dept) + ".csv", header=None)
        with open(str(each_dept) + ".xml", "+a") as out_file:
            for idx, each_row in csv_readfile.iterrows():
                out_file.write("\t\t\t" + delimiter.join(each_row) + "\n")

    # Bottom half of template that gets written out to every child xml file, might need to load each one in and append
    for each_dept in dept_column:
        with open(str(each_dept) + ".xml", "+a") as out_file:
            out_file.write("\t\t</data>\n")
            out_file.write("\t</subscriber_data>\n")
            out_file.write("</subscriber_import_job>\n")

    print("\nQUESTION #7: The following department xml files were generated from their respective csv files: "
          + str(dept_column))

except OSError as file_error:
    print(file_error)


#######################################################################################################
#  8.  When generating the XML files, within the XML node named "data", embed the                     #
#      'Master' CSV file data or 'Child' CSV file data, as created (see points 7 & 8).                #
#######################################################################################################

# Read in master data in binary, not text; "rb"
master_csv_data = open(poppulo_csv_file, "rb").read()
master_csv_encoded = base64.b64encode(master_csv_data)

