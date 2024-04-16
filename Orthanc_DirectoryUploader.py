import os
import requests

def upload_dicom_files(directory, url):
    """Recursively uploads DICOM files from a given directory to an Orthanc server."""
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith('.dcm'):  # Check if the file is a DICOM file
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'rb') as file:
                        dicom_data = file.read()
                    headers = {'Content-Type': 'application/dicom'}
                    response = requests.post(url, data=dicom_data, headers=headers)
                    if response.status_code == 200:
                        print(f"Successfully uploaded {filename}")
                    else:
                        print(f"Failed to upload {filename}: {response.text}")
                except Exception as e:
                    print(f"Error uploading {filename}: {e}")

# URL to the Orthanc server's REST API for uploading instances
orthanc_url = 'http://localhost:8042/instances'

# Path to the directory containing DICOM files
directory_path = 'E:\HFH_Anon_test\MIDRC-RICORD'

# Start uploading process
upload_dicom_files(directory_path, orthanc_url)
