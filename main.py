# Some other ideas that would take longer to implement but would be more efficient:
#   a) Break some operations out into functions to pass parameters into.
#   b) When writing xml template, instead of repeating writing of the same data in different sections,
#      create a function to do this instead which will some redundancy in code.


import csv
import os
from os import path
from datetime import datetime
import pandas as pd  # pandas module for ease of use to navigate individual column data in csv files
import base64

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
########################################################################################################
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

    # Using the headers previously extracted from question #3
    out_file.write("\t\t<columns>" + delimiter.join(header_row_from_csv) + "</columns>\n")

    out_file.write("\t\t<skip_first_line>true</skip_first_line>\n")
    out_file.write("\t\t<field_separator>comma</field_separator>\n")
    out_file.write("\t\t<data>\n")

    # Using the headers previously extracted from question #3
    out_file.write("\t\t\t" + delimiter.join(header_row_from_csv) + "\n")

    # Write data to master_XML_filename ('master.xml') from csv_readfile ('poppulu_techtask.csv')
    with open(poppulo_csv_file, 'r') as readonly_poppulu_data:
        csv_reader = csv.reader(readonly_poppulu_data)
        header = next(readonly_poppulu_data)  # Skip the header
        for each_row in csv_reader:
            out_file.write("\t\t\t" + delimiter.join(each_row) + "\n")

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

# cycle through each dept col and write to that file the template data:

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
        csv_readfile = pd.read_csv(str(each_dept) + ".csv")
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
#   8. Generate a separate 'Child' XML file per 'Department' value, using the created CSV             #
#   files (see point 5 above), named 'departmentValue.xml', using the XML template                    #
#   seen below.                                                                                       #
#######################################################################################################

message = "RW1haWwsU3VybmFtZSxGaXJzdE5hbWUsRGVwYXJ0bWVudCxDb3VudHJ5CmVtYWlsMSxTdXJuYW1lMSxGaXJzdG5hbWUxLFNhbGVzLElyZWxhbmQKZW1haWwyLFN1cm5hbWUyLEZpcnN0bmFtZTIsRmluYW5jZSxVSwplbWFpbDMsU3VybmFtZTMsRmlyc3RuYW1lMyxTYWxlcyxGcmFuY2UKZW1haWw0LFN1cm5hbWU0LEZpcnN0bmFtZTQsRW5naW5lZXJpbmcsR2VybWFueQplbWFpbDUsU3VybmFtZTUsRmlyc3RuYW1lNSxNYXJrZXRpbmcsVVNBCmVtYWlsNixTdXJuYW1lNixGaXJzdG5hbWU2LEZpbmFuY2UsSXJlbGFuZAplbWFpbDcsU3VybmFtZTcsRmlyc3RuYW1lNyxTYWxlcyxVSwplbWFpbDgsU3VybmFtZTgsRmlyc3RuYW1lOCxFbmdpbmVlcmluZyxGcmFuY2UKZW1haWw5LFN1cm5hbWU5LEZpcnN0bmFtZTksTWFya2V0aW5nLEdlcm1hbnkKZW1haWwxMCxTdXJuYW1lMTAsRmlyc3RuYW1lMTAsRmluYW5jZSxVU0EKZW1haWwxMSxTdXJuYW1lMTEsRmlyc3RuYW1lMTEsTWFya2V0aW5nLElyZWxhbmQKZW1haWwxMixTdXJuYW1lMTIsRmlyc3RuYW1lMTIsRW5naW5lZXJpbmcsVUsKZW1haWwxMyxTdXJuYW1lMTMsRmlyc3RuYW1lMTMsTWFya2V0aW5nLEZyYW5jZQplbWFpbDE0LFN1cm5hbWUxNCxGaXJzdG5hbWUxNCxNYXJrZXRpbmcsR2VybWFueQplbWFpbDE1LFN1cm5hbWUxNSxGaXJzdG5hbWUxNSxGaW5hbmNlLFVTQQplbWFpbDE2LFN1cm5hbWUxNixGaXJzdG5hbWUxNixTYWxlcyxJcmVsYW5kCmVtYWlsMTcsU3VybmFtZTE3LEZpcnN0bmFtZTE3LEVuZ2luZWVyaW5nLFVLCmVtYWlsMTgsU3VybmFtZTE4LEZpcnN0bmFtZTE4LE1hcmtldGluZyxGcmFuY2UKZW1haWwxOSxTdXJuYW1lMTksRmlyc3RuYW1lMTksRmluYW5jZSxHZXJtYW55CmVtYWlsMjAsU3VybmFtZTIwLEZpcnN0bmFtZTIwLFNhbGVzLFVTQQplbWFpbDIxLFN1cm5hbWUyMSxGaXJzdG5hbWUyMSxFbmdpbmVlcmluZyxJcmVsYW5kCmVtYWlsMjIsU3VybmFtZTIyLEZpcnN0bmFtZTIyLE1hcmtldGluZyxVSwplbWFpbDIzLFN1cm5hbWUyMyxGaXJzdG5hbWUyMyxGaW5hbmNlLEZyYW5jZQplbWFpbDI0LFN1cm5hbWUyNCxGaXJzdG5hbWUyNCxTYWxlcyxHZXJtYW55CmVtYWlsMjUsU3VybmFtZTI1LEZpcnN0bmFtZTI1LEVuZ2luZWVyaW5nLFVTQQplbWFpbDI2LFN1cm5hbWUyNixGaXJzdG5hbWUyNixNYXJrZXRpbmcsSXJlbGFuZAplbWFpbDI3LFN1cm5hbWUyNyxGaXJzdG5hbWUyNyxNYXJrZXRpbmcsVUsKZW1haWwyOCxTdXJuYW1lMjgsRmlyc3RuYW1lMjgsRmluYW5jZSxGcmFuY2UKZW1haWwyOSxTdXJuYW1lMjksRmlyc3RuYW1lMjksU2FsZXMsR2VybWFueQplbWFpbDMwLFN1cm5hbWUzMCxGaXJzdG5hbWUzMCxFbmdpbmVlcmluZyxVU0EKZW1haWwzMSxTdXJuYW1lMzEsRmlyc3RuYW1lMzEsTWFya2V0aW5nLElyZWxhbmQKZW1haWwzMixTdXJuYW1lMzIsRmlyc3RuYW1lMzIsRmluYW5jZSxVSwplbWFpbDMzLFN1cm5hbWUzMyxGaXJzdG5hbWUzMyxTYWxlcyxGcmFuY2UKZW1haWwzNCxTdXJuYW1lMzQsRmlyc3RuYW1lMzQsRW5naW5lZXJpbmcsR2VybWFueQplbWFpbDM1LFN1cm5hbWUzNSxGaXJzdG5hbWUzNSxNYXJrZXRpbmcsVVNBCmVtYWlsMzYsU3VybmFtZTM2LEZpcnN0bmFtZTM2LEZpbmFuY2UsSXJlbGFuZAplbWFpbDM3LFN1cm5hbWUzNyxGaXJzdG5hbWUzNyxTYWxlcyxVSwplbWFpbDM4LFN1cm5hbWUzOCxGaXJzdG5hbWUzOCxFbmdpbmVlcmluZyxGcmFuY2UKZW1haWwzOSxTdXJuYW1lMzksRmlyc3RuYW1lMzksTWFya2V0aW5nLEdlcm1hbnkKZW1haWw0MCxTdXJuYW1lNDAsRmlyc3RuYW1lNDAsVGVjaG5pY2FsIFNlcnZpY2VzLFVTQQplbWFpbDQxLFN1cm5hbWU0MSxGaXJzdG5hbWU0MSxGaW5hbmNlLElyZWxhbmQKZW1haWw0MixTdXJuYW1lNDIsRmlyc3RuYW1lNDIsRmluYW5jZSxVSwplbWFpbDQzLFN1cm5hbWU0MyxGaXJzdG5hbWU0MyxFbmdpbmVlcmluZyxGcmFuY2UKZW1haWw0NCxTdXJuYW1lNDQsRmlyc3RuYW1lNDQsTWFya2V0aW5nLEdlcm1hbnkKZW1haWw0NSxTdXJuYW1lNDUsRmlyc3RuYW1lNDUsRmluYW5jZSxVU0EKZW1haWw0NixTdXJuYW1lNDYsRmlyc3RuYW1lNDYsU2FsZXMsSXJlbGFuZAplbWFpbDQ3LFN1cm5hbWU0NyxGaXJzdG5hbWU0NyxFbmdpbmVlcmluZyxVSwplbWFpbDQ4LFN1cm5hbWU0OCxGaXJzdG5hbWU0OCxNYXJrZXRpbmcsRnJhbmNlCmVtYWlsNDksU3VybmFtZTQ5LEZpcnN0bmFtZTQ5LEZpbmFuY2UsR2VybWFueQplbWFpbDUwLFN1cm5hbWU1MCxGaXJzdG5hbWU1MCxTYWxlcyxVU0EK"
#base64.encode(message)
message_bytes = base64.b64decode(message)
print("\n" + str(message_bytes))





