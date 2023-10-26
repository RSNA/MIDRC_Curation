#script modifies DICOM tag values within a DICOM image directory
#initial by jsho updated 20220308

import os
import pydicom
from tqdm import tqdm

# Define function to modify DICOM metadata
def modify_dicom_metadata(file_path, element_value, tag_code):
    # Load DICOM file
    dcm = pydicom.dcmread(file_path)

    # Get current tag value
    tag_value = dcm[tag_code].value

    if isinstance(tag_value, pydicom.valuerep.PersonName):
        tag_value = str(tag_value)

    # Check if tag value contains a hyphen
    if "-" in tag_value:
        # Split tag value by hyphen
        split_value = tag_value.split("-")
        # Replace left side of hyphen with element_value
        new_value = f"{element_value}-{split_value[1]}"
    else:
        # Replace entire tag value
        new_value = element_value

    # Modify tag value
    dcm[tag_code].value = new_value

    # Save modified DICOM file
    dcm.save_as(file_path)

# Get user input
element_value = input("Enter DICOM element value to modify: ")

# Define list of DICOM tags to modify
tags_to_modify = [(0x0010,0x0010), (0x0010,0x0020), (0x0013,0x1012), (0x0013,0x1013)]

# Get list of DICOM files in directory tree
directory = input("Enter DICOM directory path: ")
dicom_files = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".dcm"):
            dicom_files.append(os.path.join(root, file))

# Loop through DICOM files and modify metadata
for file_path in tqdm(dicom_files, desc="Processing DICOM files"):
    for tag_code in tags_to_modify:
        modify_dicom_metadata(file_path, element_value, tag_code)
