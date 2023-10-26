import os
import shutil
import pandas as pd


def find_studies_and_move(source_folder, target_folder, csv_file):
    df = pd.read_csv(csv_file)

    study_uids = set(df['study_uid'])

    for root, dirs, _ in os.walk(source_folder, topdown=True):
        studyUID = os.path.basename(os.path.dirname(root))

        if studyUID not in study_uids:
            dirs[:] = [d for d in dirs if d != studyUID]

            relative_path = os.path.relpath(root, source_folder)
            target_path = os.path.join(target_folder, relative_path)

            os.makedirs(target_path, exist_ok=True)

            try:
                shutil.move(root, target_path)
            except Exception as e:
                print(f"Error moving directory {root} to {target_path}: {e}")


find_studies_and_move(r'E:\ucsf_long_covid_submission_1', r'E:\ucsf_long_covid_submission_no_mr',
                     r'E:\study_uids_to_move.csv')
