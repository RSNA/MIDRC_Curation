import os
import shutil
import pandas as pd
from tqdm import tqdm
import argparse
import time

def main(source_dir, quarantine_dir, csv_path):
    df = pd.read_csv(csv_path)

    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        patient_id = str(row['patient_id'])
        study_uid = str(row['study_uid'])

        for root, dirs, files in os.walk(source_dir):
            if patient_id in dirs:
                patient_folder = os.path.join(root, patient_id)
                quarantine_patient_dir = os.path.join(quarantine_dir, patient_id)

                os.makedirs(quarantine_patient_dir, exist_ok=True)

                if pd.isnull(study_uid):
                    dst_dir = os.path.join(quarantine_patient_dir, patient_id)
                    if os.path.exists(dst_dir):
                        dst_dir = dst_dir + '_' + str(time.time())
                    shutil.move(patient_folder, dst_dir)
                else:
                    for subroot, subdirs, subfiles in os.walk(patient_folder):
                        if study_uid in subdirs:
                            study_folder = os.path.join(subroot, study_uid)
                            dst_dir = os.path.join(quarantine_patient_dir, study_uid)
                            if os.path.exists(dst_dir):
                                dst_dir = dst_dir + '_' + str(time.time())
                            shutil.move(study_folder, dst_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('source_dir', help='The DICOM source directory in jumpbox')
    parser.add_argument('quarantine_dir', help='The quarantined directory in jumpbox')
    parser.add_argument('csv_path', help='The CSV file path')
    args = parser.parse_args()

    main(args.source_dir, args.quarantine_dir, args.csv_path)