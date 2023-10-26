import os
import pydicom
from faker import Faker
import random
import string
import datetime
import argparse

fake = Faker()

patient_data_cache = {}


def synthetic_patient_data(patient_id):
    if patient_id in patient_data_cache:
        return patient_data_cache[patient_id]
    else:
        synthetic_data = {
            'PatientName': fake.name(),
            'PatientBirthDate': fake.date_between_dates(
                date_start=datetime.date.today() - datetime.timedelta(days=80 * 365),
                date_end=datetime.date.today() - datetime.timedelta(days=18 * 365)).strftime("%Y%m%d"),
            'PatientAge': str(random.randint(18, 95)).zfill(3),
            'PatientMotherBirthName': fake.name(),
            'MilitaryRank': fake.job(),
            'PatientAddress': fake.address().replace('\n', ' '),
            'BranchOfService': random.choice(['Army', 'Navy', 'Air Force', 'Marine Corps', 'Coast Guard']),
        }
        patient_data_cache[patient_id] = synthetic_data
        return synthetic_data


def update_dicom_file(file_path):
    ds = pydicom.dcmread(file_path)

    patient_id = ds.PatientID
    synthetic_data = synthetic_patient_data(patient_id)

    for tag, value in synthetic_data.items():
        if tag in ds:
            ds.data_element(tag).value = value

    synthetic_data_varying = {
        'StudyDate': fake.date_between_dates(date_start=datetime.date(2020, 1, 1),
                                             date_end=datetime.date.today()).strftime("%Y%m%d"),
        'SeriesDate': fake.date_between_dates(date_start=datetime.date(2020, 1, 1),
                                              date_end=datetime.date.today()).strftime("%Y%m%d"),
        'AcquisitionDate': fake.date_between_dates(date_start=datetime.date(2020, 1, 1),
                                                   date_end=datetime.date.today()).strftime("%Y%m%d"),
        'ContentDate': fake.date_between_dates(date_start=datetime.date(2020, 1, 1),
                                               date_end=datetime.date.today()).strftime("%Y%m%d"),
        'StudyTime': fake.time(pattern="%H%M%S"),
        'SeriesTime': fake.time(pattern="%H%M%S"),
        'AcquisitionTime': fake.time(pattern="%H%M%S"),
        'ContentTime': fake.time(pattern="%H%M%S"),
        'ReferringPhysicianName': fake.name(),
        'PerformingPhysicianName': fake.name(),
        'InstitutionName': fake.company(),
        'InstitutionAddress': fake.address().replace('\n', ' '),
        'InsurancePlanIdentificationRetired': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        'MedicalRecordLocator': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        'MedicalAlerts': fake.sentence(nb_words=6),
        'ContrastAllergies': fake.sentence(nb_words=6),
        'PatientTelephoneNumber': fake.phone_number(),
        'AdditionalPatientHistory': fake.text(max_nb_chars=200),
        'PatientComments': fake.text(max_nb_chars=200),
    }

    for tag, value in synthetic_data_varying.items():
        if tag in ds:
            ds.data_element(tag).value = value

    for element in ds.iterall():
        if element.tag.group == 0x0013:
            del ds[element.tag]

    ds.PatientIdentityRemoved = "NO"
    ds.DeIdentificationMethod = ""
    if "DeIdentificationMethodCodeSequence" in ds:
        ds.DeIdentificationMethodCodeSequence = [item for item in ds.DeIdentificationMethodCodeSequence if
                                                 item.CodeValue != "113100"]

    private_block = ds.private_block(0x0049, "FakeBlock", create=True)
    private_block.add_new(0x10, 'LO', fake.word())
    private_block.add_new(0x20, 'LO', fake.sentence())

    ds.save_as(file_path)


def update_dicom_files_in_dir(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".dcm"):
                update_dicom_file(os.path.join(root, file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path', type=str, help='directory containing the DICOM files')

    args = parser.parse_args()

    update_dicom_files_in_dir(args.dir_path)
