# Script that renames DICOM files according to their SOP Instance UID and empties Age tag if age > 89
# Maryam Vazirabad

import pydicom
import os
import argparse
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

    if (0x0010, 0x1010) in ds:
        age = str(ds.PatientAge) #get age from dicom tag and convert to string
        if age: #check if age is real value
            scale = age[-1:]
            if scale.isalpha(): #if last char is Y, M, D, etc. (it should be)
                age = age[:-1] #delete last char
            if len(age) > 1:
                if age[0] == '0':
                    age = int(age[1:])
                else:
                    age = int(age)
            elif len(age) <= 1:
                age = int(age)
            if age > 89:
                print('age is greater than 89')
                print(ds.PatientAge)
                ds.PatientAge = None #setting patient age to None

    folder = os.path.dirname(complete_f_path)
    # Adding the SOP Instance UID to file name
    destination = folder + '/' + sop_instance_uid + ".dcm"
    # Renaming the file
    os.rename(complete_f_path, destination)
    ds.save_as(destination)

print('\nProcessing complete.')
