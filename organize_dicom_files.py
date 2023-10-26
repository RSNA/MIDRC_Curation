import pydicom as py
import os
import argparse
from pathlib import Path
from tqdm import tqdm
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("inputDirectory", type=str, help="input DICOM directory")
args = parser.parse_args()

data_root_path = Path(args.inputDirectory)
filenames = list(data_root_path.glob('**/*.dcm'))

input_dir_name = os.path.basename(args.inputDirectory)
destination_dir_name = f"organized_{input_dir_name}"
destination_dir = data_root_path.parent / destination_dir_name
os.makedirs(destination_dir, exist_ok=True)

print("Organizing...\n")


def organize_files(image_fn, destination):
    d = py.dcmread(image_fn)
    destination_fn = f'{destination}/{d.PatientID}/{d.StudyInstanceUID}/{d.SeriesInstanceUID}/{d.SOPInstanceUID}.dcm'
    os.makedirs(destination + '/' + d.PatientID, exist_ok=True)
    os.makedirs(destination + '/' + d.PatientID + '/' + d.StudyInstanceUID, exist_ok=True)
    os.makedirs(destination + '/' + d.PatientID + '/' + d.StudyInstanceUID + '/' + d.SeriesInstanceUID, exist_ok=True)
    shutil.copyfile(image_fn, destination_fn)


for filename in tqdm(filenames, total=len(filenames)):
    organize_files(str(filename), str(destination_dir))

print(f'\nOrganization of files complete. Organized files saved in {destination_dir}.')
