#script creates case level directories for nesting associated studies
#initial by jsho updated 20230308

import os
import shutil
import pydicom
import sys

# Set the root directory containing the subdirectories to move
root_directory = sys.argv[1]

# Define a function to recursively search for DICOM images
def find_dicom_file(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.dcm'):
                dicom_file = os.path.join(dirpath, filename)
                return dicom_file
    return None

# Iterate through the subdirectories in the root directory
for subdirectory in os.listdir(root_directory):
    subdirectory_path = os.path.join(root_directory, subdirectory)

    # Check if the subdirectory is a directory
    if os.path.isdir(subdirectory_path):

        # Find the DICOM image in the subdirectory
        dicom_file = find_dicom_file(subdirectory_path)

        # Check if a DICOM file was found in the subdirectory
        if dicom_file:

            # Read the DICOM image to get the patient name
            ds = pydicom.dcmread(dicom_file)
            patient_name = str(ds[0x0010, 0x0010].value)

            # Create a parent directory with the patient name if it doesn't exist
            parent_directory = os.path.join(root_directory, patient_name)
            if not os.path.exists(parent_directory):
                os.makedirs(parent_directory)

            # Move the subdirectory to the parent directory
            new_directory_path = os.path.join(parent_directory, subdirectory)
            shutil.move(subdirectory_path, new_directory_path)
