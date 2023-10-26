#script to rename existing DICOM directory with DICOM element value as string.
#intial by jsho and update 20230308

import os
import sys
import shutil
import pydicom
from tqdm import tqdm

root_directory = sys.argv[1]

# Rename subdirectories to temporary incremented string value
subdirectories = os.listdir(root_directory)
for i, subdirectory in enumerate(subdirectories):
    if os.path.isdir(os.path.join(root_directory, subdirectory)):
        new_name = f'case_{i+1}'
        os.rename(os.path.join(root_directory, subdirectory), os.path.join(root_directory, new_name))

# Iterate through root subdirectories and nested directories for DICOM images
for subdirectory in tqdm(os.listdir(root_directory)):
    if os.path.isdir(os.path.join(root_directory, subdirectory)):
        dicom_file = None
        for dirpath, dirnames, filenames in os.walk(os.path.join(root_directory, subdirectory)):
            for filename in filenames:
                if filename.endswith('.dcm'):
                    dicom_file = os.path.join(dirpath, filename)
                    break
            if dicom_file:
                break

        # Get DICOM element value (0010,0010) as a string
        if dicom_file:
            ds = pydicom.dcmread(dicom_file)
            element_value = str(ds[0x0010, 0x0010].value)

            # Rename subdirectory to element value
            os.rename(os.path.join(root_directory, subdirectory), os.path.join(root_directory, element_value))
