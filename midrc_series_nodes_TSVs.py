"""
Generating CT Series, DX Series, and CR series for submission to MIDRC
Run the script as follows: python midrc_series_nodes_TSVs.py PATH_TO_POWERTOOLS_CSV
Author: Maryam Vazirabad
Updated: 2/9/2022
"""
import sys
import os
import pandas as pd


def print_info(df1):  # print general info about batch of imaging data
    print('\nNumber of cases in batch: {0}'.format(len(df1.drop_duplicates(subset=['case_ids']))))
    print('Number of studies in batch: {0}'.format(len(df1.drop_duplicates(subset=['study_uid']))))
    print('Number of series in batch: {0}'.format(len(df1.drop_duplicates(subset=['series_uid']))))
    print('Number of imaging files in batch: {0}'.format(len(df1)))


def gather_TSV_info(df1, date):  # getting ready to create Series TSVs
    df = df1.drop_duplicates(
        subset=['series_uid'])  # Grab all series information by finding unique Series UIDS in DICOM data
    result_CT = df.loc[df['modality'] == 'CT']  # Locate all the rows for CT series
    print('\nNumber of CT series in batch: {0}'.format(len(result_CT)))
    result_DX = df.loc[df['modality'] == 'DX']  # Locate all the rows for DX series
    print('Number of DX series in batch: {0}'.format(len(result_DX)))
    result_CR = df.loc[df['modality'] == 'CR']  # Locate all the rows for CR series
    print('Number of CR series in batch: {0}'.format(len(result_CR)))
    # Properties in the Series Nodes (differs depending on modality type)
    # Grab the columns that are needed:
    result_CT = result_CT.loc[:, ['study_uid', 'case_ids', 'acquisition_type', 'contrast_bolus_agent',
                                  'convolution_kernel', 'exposure_modulation_type', 'image_type',
                                  'lossy_image_compression', 'manufacturer',
                                  'manufacturer_model_name', 'modality', 'patient_position', 'pixel_spacing',
                                  'series_description', 'series_uid', 'slice_thickness',
                                  'spacing_between_slices']]
    result_CR = result_CR.loc[:,
                ['study_uid', 'case_ids', 'contrast_bolus_agent',
                 'detector_type', 'image_type', 'imager_pixel_spacing', 'lossy_image_compression',
                 'manufacturer', 'manufacturer_model_name', 'modality', 'pixel_spacing',
                 'series_description', 'series_uid', 'spatial_resolution', 'view_position']]
    result_DX = result_DX.loc[:,
                ['study_uid', 'case_ids', 'contrast_bolus_agent',
                 'detector_type', 'image_type', 'imager_pixel_spacing', 'lossy_image_compression',
                 'manufacturer', 'manufacturer_model_name', 'modality', 'pixel_spacing', 'series_description',
                 'series_uid', 'spatial_resolution', 'view_position']]
    create_TSVs(result_CT, date, modality_type='CT')
    create_TSVs(result_CR, date, modality_type='CR')
    create_TSVs(result_DX, date, modality_type='DX')


def create_TSVs(result_mod, date, modality_type):  # creating the series TSVs according to modality type
    dict_rename = {'study_uid': 'imaging_studies.submitter_id'}
    result_mod.rename(columns=dict_rename,
                      inplace=True)
    result_mod['type'] = modality_type.lower() + '_series_file'
    result_mod['data_type'] = 'DICOM'
    result_mod['data_format'] = 'DCM'
    result_mod['data_category'] = modality_type
    result_mod['submitter_id'] = result_mod[
        "series_uid"]  # The submitter id of each series node will also be the Series UID
    result_mod.to_csv(modality_type.lower() + '_series_RSNA_' + date + '.tsv', sep='\t',
                      index=False)  # write to TSV file in default directory
    print('\n{0} Series TSV created'.format(modality_type))


if __name__ == "__main__":
    try:
        powertools_path = sys.argv[1]  # path to powertools file (.csv)
        assert powertools_path.endswith('.csv'), 'Invalid file type'
        df1 = pd.read_csv(powertools_path, low_memory=False)
        csv_filename = str(os.path.basename(powertools_path)).replace('.csv', '')
        x = csv_filename.split("_")
        date = x[2]
        csv_filename = csv_filename + '.csv'
        print_info(df1)
        gather_TSV_info(df1, date)
    except IndexError:
        print("You did not specify a file")
        sys.exit(1)  # abort due to error
