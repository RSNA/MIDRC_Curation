# Script that renames DICOM files according to their SOP Instance UID
# Maryam Vazirabad

import pydicom
import os
import argparse
import errno
import shutil
import glob
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("inputDirectory", type=str, help="input DICOM directory")
args = parser.parse_args()

inputDirectory = args.inputDirectory + "\\"
print("Starting renaming...\n")

dcm_files = glob.glob(inputDirectory + "**/*.dcm", recursive=True)
print(str(len(dcm_files)) + " DICOM files found in batch \n")

for i in tqdm(range(len(dcm_files))):
    complete_f_path = os.fsdecode(dcm_files[i])

    ds = pydicom.dcmread(complete_f_path)
    tag = pydicom.read_file(complete_f_path)
    sop_instance_uid = str(tag[0x0008, 0x0018].value)

    folder = os.path.dirname(complete_f_path)

    # Adding the SOP Instance UID to file name
    destination = folder + '/' + sop_instance_uid + ".dcm"
    # Renaming the file
    os.rename(complete_f_path, destination)

print('\nRenaming complete.')
