#script to edit DICOM imaging data within AWS S3 bucket


import urllib.parse
import argparse
import pydicom
import boto3
import time
from pydicom.tag import Tag
from pydicom.dataelem import DataElement
from tqdm import tqdm
from io import BytesIO

def main(s3_uri, chunk_size, sleep_time, start, end):
    s3 = boto3.resource('s3')
    client = boto3.client('s3')


    parsed_uri = urllib.parse.urlparse(s3_uri)
    bucket_name = parsed_uri.netloc
    prefix = parsed_uri.path.lstrip('/')

    paginator = client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    tags_to_add = {
        (0x0013, 0x1010): 'MIDRC-RICORD',
        (0x0013, 0x1011): 'MIDRC-RICORD',
        (0x0013, 0x1012): '702389',
        (0x0013, 0x1013): '702389',
    }

    obj_counter = 0
    for page in pages:
        for obj in tqdm(page['Contents'][start:end], total=end-start):
            if obj_counter < start:
                obj_counter += 1
                continue
            if obj_counter >= end:
                break

            if obj['Key'].endswith('.dcm'):
                dicom_content = s3.Object(bucket_name, obj['Key']).get()['Body'].read()
                dicom_file = pydicom.dcmread(BytesIO(dicom_content))

                dicom_file.add(DataElement(Tag(0x0013, 0x0010), 'LO', 'CTP'))
                for tag, value in tags_to_add.items():
                    dicom_file.add(DataElement(tag, 'LO', value))

                dicom_io = BytesIO()
                dicom_file.save_as(dicom_io)

                s3.Object(bucket_name, obj['Key']).put(Body=dicom_io.getvalue())

            if obj_counter % chunk_size ==0:
                print(f'Processed {chunk_size} objects, sleeping for {sleep_time} seconds')
                time.sleep(sleep_time)

            obj_counter += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('s3_uri', help='The S3 URI of the DICOM directory')
    parser.add_argument('chunk_size', type=int, help='Number of objects')
    parser.add_argument('sleep_time', type=int, help='Seconds between process')
    parser.add_argument('start', type=int, help='The starting index of objects')
    parser.add_argument('end', type=int, help='The ending index of objects')
    args = parser.parse_args()

    main(args.s3_uri, args.chunk_size, args.sleep_time, args.start, args.end)