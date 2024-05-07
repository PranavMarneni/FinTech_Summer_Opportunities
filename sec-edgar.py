# Importing all necessary libraries
from sec_edgar_downloader import Downloader
#Imports to open, access, and edit files
import os
import re

#Initialize downloader
dl = Downloader('pmarnGT', 'pranavmarneni321@gmail.com')

#User's ticker of choice
ticker = "AAPL"

# Download 10-K filings for respective ticker from 1995 to 2023
num_files_downloaded = dl.get("10-K", ticker, after="1995-01-01", before="2023-03-25",download_details=True)

#Providing folder path to download
folder_path = f"/Users/pranavmarneni/sec-edgar-filings/{ticker}/10-K"

#Method to rename files to make it easy to access
renamed_files = []
def rename_files_in_folder(folder_path):
    # Get a list of files in the folder
    files = os.listdir(folder_path)
    for file in files:
        # Access the area where the dates are stored in file name
        date = file[11:13]
        if date.isdigit() and len(date) == 2:  # Check if date is a valid two-digit number
            # Conditional to check if before or after 1999
            if(int(date)<=24):
                print("20" + date)
                new_file_name = f"20{date}.txt"  # For example, renaming to "file_<date>.txt"
            else:
                print("19" + date)
                new_file_name = f"19{date}.txt"
        # Update file names
        old_file_path = os.path.join(folder_path, file)
        new_file_path = os.path.join(folder_path, new_file_name)

        os.rename(old_file_path, new_file_path)
            
            # Append the renamed file name to the list
        renamed_files.append(new_file_name)

        print(f"Renamed '{file}' to '{new_file_name}'")
    
    return renamed_files

#Calling method
rename_files_in_folder(folder_path)
