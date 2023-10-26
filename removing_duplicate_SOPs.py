#script that locates duplicate SOP instance images in DICOM directory
#initial by jsho updated 20230309

import os
import pydicom
import hashlib
import sys

# Get the root directory containing the DICOM images from the command line argument
root_directory = sys.argv[1]

# Define a function to compute the MD5 hash of a DICOM file
def compute_md5(dicom_file):
    with open(dicom_file, 'rb') as f:
        data = f.read()
        return hashlib.md5(data).hexdigest()

# Define a function to recursively search for DICOM files
def find_dicom_files(directory):
    dicom_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.dcm'):
                dicom_file = os.path.join(dirpath, filename)
                dicom_files.append(dicom_file)
    return dicom_files

# Define a function to remove duplicate DICOM files
def remove_duplicate_dicom_files(directory):
    # Find all DICOM files in the directory and its subdirectories
    dicom_files = find_dicom_files(directory)

    # Create a dictionary to store the MD5 hash values of DICOM files
    md5_dict = {}

    # Iterate through the DICOM files
    for dicom_file in dicom_files:
        # Read the DICOM file to get the SOP Instance UID
        ds = pydicom.dcmread(dicom_file)
        sop_instance_uid = ds[0x0008, 0x0018].value

        # Compute the MD5 hash of the DICOM file
        md5 = compute_md5(dicom_file)

        # Check if the SOP Instance UID already exists in the dictionary
        if sop_instance_uid in md5_dict:
            # Check if the MD5 hash of the DICOM file is the same as the one in the dictionary
            if md5 == md5_dict[sop_instance_uid]:
                # If the MD5 hash is the same, the DICOM file is a duplicate
                print(f"Removing duplicate DICOM file: {dicom_file}")
                os.remove(dicom_file)
            else:
                # If the MD5 hash is different, there is a hash collision
                print(f"Hash collision detected for DICOM file: {dicom_file}")
                # Get the MD5 hash value that is already in the dictionary
                old_md5 = md5_dict[sop_instance_uid]
                # Find the path of the DICOM file with the old MD5 hash value
                old_dicom_file = next(filter(lambda x: compute_md5(x) == old_md5, dicom_files), None)
                if old_dicom_file:
                    # If the DICOM file with the old MD5 hash value is found, delete it
                    print(f"Deleting DICOM file with old MD5 hash value: {old_dicom_file}")
                    os.remove(old_dicom_file)
                else:
                    # If the DICOM file with the old MD5 hash value is not found (unlikely), print a warning message
                    print("Warning: DICOM file with old MD5 hash value not found.")
        else:
            # If the SOP Instance UID doesn't exist in the dictionary, add it
            md5_dict[sop_instance_uid] = md5

    # Recursively remove empty directories
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        if not os.listdir(dirpath):
            os.rmdir(dirpath)

# Call the function to remove duplicate DICOM files
remove_duplicate_dicom_files(root_directory)
