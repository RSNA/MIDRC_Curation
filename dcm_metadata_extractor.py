
# Extracting a list of DICOM metadata from a directory of DICOM files (PowerTools Indexer dupe!)
# Author: Maryam Vazirabad
# Last updated: 1/20/23
import os
import csv
import pydicom
import sys
from tqdm import tqdm


def get_dicom_metadata(file):
    dcm = pydicom.dcmread(file)
    pixel_spacing = dcm.get("PixelSpacing", "")
    if pixel_spacing != "":
        pixel_spacing = pixel_spacing[0].original_string
    imager_pixel_spacing = dcm.get("ImagerPixelSpacing", "")
    if imager_pixel_spacing != "":
        imager_pixel_spacing = imager_pixel_spacing[0].original_string
    image_type = dcm.get("ImageType", "")
    if type(image_type) != str:
        image_type = "_".join(dcm.get("ImageType", ""))
    convolution_kernel = dcm.get("ConvolutionKernel", "")
    if type(convolution_kernel) != str:
        convolution_kernel = "_".join(dcm.get("ConvolutionKernel", ""))
    exposure_modulation_type = dcm.get("ExposureModulationType", "")
    if type(exposure_modulation_type) != str:
        exposure_modulation_type = "_".join(dcm.get("ExposureModulationType", ""))

    data = {
        'file_name': os.path.basename(file),
        'accession_number': dcm.get("AccessionNumber", ""),
        'acquisition_type': dcm.get("AcquisitionType", ""),
        'body_part_examined': dcm.get("BodyPartExamined", ""),
        'case_ids': dcm.get("PatientID", ""),
        'contrast_bolus_agent': dcm.get("ContrastBolusAgent", ""),
        'patient_position': dcm.get("PatientPosition", ""),
        'convolution_kernel': convolution_kernel,
        'detector_type': dcm.get("DetectorType", ""),
        'exposure_modulation_type': exposure_modulation_type,
        'image_type': image_type,
        'imager_pixel_spacing': imager_pixel_spacing,
        'lossy_image_compression': dcm.get("LossyImageCompression", ""),
        'manufacturer': dcm.get("Manufacturer", ""),
        'manufacturer_model_name': dcm.get("ManufacturerModelName", ""),
        'modality': dcm.get("Modality", ""),
        'sop_instance_uid': dcm.get("SOPInstanceUID", ""),
        'pixel_spacing': pixel_spacing,
        'series_description': dcm.get("SeriesDescription", ""),
        'series_uid': dcm.get("SeriesInstanceUID", ""),
        'slice_thickness': dcm.get("SliceThickness", ""),
        'spacing_between_slices': dcm.get("SpacingBetweenSlices", ""),
        'spatial_resolution': dcm.get("SpatialResolution", ""),
        'study_description': dcm.get("StudyDescription", ""),
        'study_uid': dcm.get("StudyInstanceUID", ""),
        'view_position': dcm.get("ViewPosition", ""),
        'study_date': dcm.get("StudyDate", "")
    }
    return data


def write_csv(data, filename):
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def loc_dicom_files(directory):
    dicom_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".dcm"):
                dicom_files.append(os.path.join(root, file))
    return dicom_files


def main(directory):
    dicom_files = loc_dicom_files(directory)
    data = [get_dicom_metadata(file) for file in tqdm(dicom_files, desc='Progress')]
    output_file = os.path.basename(os.path.normpath(directory)) + "_dcm_metadata" + ".csv"
    write_csv(data, output_file)
    print()
    print('DICOM metadata exported to ' + output_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python dcm_metadata_extractor.py directory")
    else:
        main(sys.argv[1])
