import shutil
import subprocess
import sys
import pandas as pd
from pathlib import Path
import os
import glob
import numpy as np
import tqdm
from tqdm import tqdm
import hashlib
import boto3
import pydicom
import math


def ask_user(directory_path):
    user_date = int(input("Enter the intended date for the manifest (ex: 20220101): "))
    user_select = int(input("Does the inputted directory have images or submission TSVs? Enter 0 for images, "
                            "1 for submission TSVs: "))
    try:
        if user_select == 0:
            s_url = 's3://storage.ir.rsna.ai/replicated-data-rsna/RSNA_' + str(user_date) + '/data/'
            file_type = 'dcm'
            create_data_manifest(s_url, directory_path, file_type, 'imaging', str(user_date), user_select)
        elif user_select == 1:
            s_url = 's3://storage.ir.rsna.ai/replicated-data-rsna/RSNA_' + str(user_date) + '/'
            # file_type = 'tsv'
            create_clinical_manifest(s_url, directory_path, 'clinical', str(user_date))
        else:
            return ask_user(directory_path)
    except Exception as error:
        print("Unexpected error")
        print(error)
        return ask_user(directory_path)


def create_clinical_manifest(s_url, directory_path, title, date):
    text_files = glob.glob(directory_path)
    images_path = os.listdir(str(directory_path))
    numpy_array = np.array(images_path)
    df = pd.DataFrame(numpy_array, columns=['file_name'])
    hashes = []
    file_size = []
    acl = []
    url = []
    for i in tqdm(range(len(images_path))):
        # upload_to_bucket(s3, text_files[i], date, user_select)  # upload to s3 bucket
        md5_hash = hashlib.md5()
        a_file = open(text_files[i], "rb")
        content = a_file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        hashes.append(digest)
        acl.append('Open-R1')
        file_size.append(os.path.getsize(text_files[i]))
        url.append(s_url + images_path[i])

    df['md5sum'] = np.array(hashes)
    df['acl'] = np.array(acl)
    df['storage_urls'] = np.array(url)
    df['file_size'] = np.array(file_size)
    new_manifest = 'clinical_manifest_RSNA_' + date + '.tsv'
    df.to_csv(new_manifest, sep='\t', index=False)


def create_data_manifest(s_url, directory_path, file_type, title, date, user_select):
    images_path = glob.glob(str(directory_path) + "/**/*.dcm", recursive=True)
    df = pd.DataFrame()
    hashes = []
    file_size = []
    acl = []
    url = []
    case_ids = []
    study_uids = []
    series_uids = []
    instance_uids = []
    modality = []
    file_names = []

    for i in tqdm(range(len(images_path))):
        md5_hash = hashlib.md5()
        a_file = open(images_path[i], "rb")
        content = a_file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        hashes.append(digest)
        acl.append('Open-R1')
        file_size.append(os.path.getsize(images_path[i]))
        instance_uids.append(str(os.path.basename(images_path[i])).replace('.dcm', ''))
        # Get relevant DICOM tags:
        tag = pydicom.read_file(images_path[i])
        case_ids.append(str(tag[0x0010, 0x0020].value))
        study_uids.append(str(tag[0x0020, 0x000D].value))
        series_uids.append(str(tag[0x0020, 0x000E].value))
        modality.append(str(tag[0x0008, 0x0060].value))
        file_name = str(tag[0x0010, 0x0020].value) + '/' + str(tag[0x0020, 0x000D].value) + '/' + str(
            tag[0x0020, 0x000E].value) + '/' + str(os.path.basename(images_path[i]))
        file_names.append(file_name)
        url.append(s_url + file_name)

    df['md5sum'] = np.array(hashes)
    df['acl'] = np.array(acl)
    df['storage_urls'] = np.array(url)
    df['file_size'] = np.array(file_size)
    df['case_ids'] = np.array(case_ids)
    df['study_uid'] = np.array(study_uids)
    df['series_uid'] = np.array(series_uids)
    df['modality'] = np.array(modality)
    df['file_name'] = np.array(file_names)

    new_manifest = 'image_manifest_RSNA_' + date + '.tsv'
    df.to_csv(new_manifest, sep='\t', index=False)


def chunks(lst: list, n: int) -> list:
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == "__main__":
    data_root_path = Path(sys.argv[1])  # path to folder holding the batch/submission TSVs
    ask_user(data_root_path)
