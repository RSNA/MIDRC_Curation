# Script that locates all X-ray images (DX and CR) in a given directory
# and copies them over to new directory
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
print("Starting transfer...\n")

savePath = inputDirectory + "Copied X-RAYS\\"

try:
    os.mkdir(savePath)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

dcm_files = glob.glob(inputDirectory + "**/*.dcm", recursive=True)
print(str(len(dcm_files)) + " DICOM files found in batch \n")
modality_counts = []
count = 0
for i in tqdm(range(len(dcm_files))):
    complete_f_path = os.fsdecode(dcm_files[i])
    ds = pydicom.dcmread(complete_f_path)
    tag = pydicom.read_file(complete_f_path)
    modality = str(tag[0x0008, 0x0060].value)
    modality_counts.append(modality)
    if modality != 'DX' and modality != 'CR':
        continue
    saveFile = savePath + os.path.basename(complete_f_path)
    try:
        ds.save_as(saveFile)
    except OSError as e:
        if e.errno != errno.ENOENT:
            print("ERROR: No such file or directory named " + saveFile)
            raise
    newFilePath = savePath + "\\"
    shutil.move(saveFile, newFilePath + 'Xray' + str(count) + '_' + os.path.basename(complete_f_path))  # renaming file
    count += 1

print('\nTransfer complete. Modality counts: ')
unique_values = dict(zip(modality_counts, [modality_counts.count(i) for i in modality_counts]))
print(unique_values)
