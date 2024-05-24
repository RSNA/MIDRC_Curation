"""
Generating CT Series, DX Series, CR series, MR series, NM series, US series, RF series, XA series,
and PT series TSVs for submission to MIDRC
Run the script as follows: python midrc_series_nodes_TSVs.py PATH_TO_DCM_METADATA_CSV
Author: Maryam Vazirabad
Updated: 7/5/2022

Updated File handling and debugging
Author: Thomas OSullivan
Updated: 7/24/2024
"""

import sys
import os
import pandas as pd

def print_info(df1):  # print general info about batch of imaging data
    print('\nNumber of cases in batch: {0}'.format(len(df1.drop_duplicates(subset=['case_ids']))))
    print('Number of studies in batch: {0}'.format(len(df1.drop_duplicates(subset=['study_uid']))))
    print('Number of series in batch: {0}'.format(len(df1.drop_duplicates(subset=['series_uid']))))
    print('Number of imaging files in batch: {0}'.format(len(df1)))

def gather_TSV_info(df1, date, output_path):  # getting ready to create Series TSVs
    df = df1.drop_duplicates(subset=['series_uid'])  # Grab all series information by finding unique Series UIDS in DICOM data
    modalities = ['CT', 'DX', 'CR', 'MR', 'NM', 'US', 'RF', 'XA', 'PT']
    for modality in modalities:
        result = df.loc[df['modality'] == modality]
        print('\nNumber of {0} series in batch: {1}'.format(modality, len(result)))
        create_TSVs(result, date, modality_type=modality, output_path=output_path)

def create_TSVs(result_mod, date, modality_type, output_path):  # creating the series TSVs according to modality type
    if result_mod.empty:
        print(f'No {modality_type} data found. Skipping {modality_type} TSV creation.')
        return

    column_map = {
        'CT': ['study_uid', 'case_ids', 'acquisition_type', 'contrast_bolus_agent', 'convolution_kernel',
               'exposure_modulation_type', 'image_type', 'lossy_image_compression', 'manufacturer',
               'manufacturer_model_name', 'modality', 'patient_position', 'pixel_spacing', 'series_description',
               'series_uid', 'slice_thickness', 'spacing_between_slices'],
        'CR': ['study_uid', 'case_ids', 'contrast_bolus_agent', 'detector_type', 'image_type', 'imager_pixel_spacing',
               'lossy_image_compression', 'manufacturer', 'manufacturer_model_name', 'modality', 'pixel_spacing',
               'series_description', 'series_uid', 'spatial_resolution', 'view_position'],
        'DX': ['study_uid', 'case_ids', 'contrast_bolus_agent', 'detector_type', 'image_type', 'imager_pixel_spacing',
               'lossy_image_compression', 'manufacturer', 'manufacturer_model_name', 'modality', 'pixel_spacing',
               'series_description', 'series_uid', 'spatial_resolution', 'view_position'],
        'MR': ['study_uid', 'angio_flag', 'case_ids', 'contrast_bolus_agent', 'diffusion_b_value',
               'diffusion_gradient_orientation', 'echo_number', 'echo_train_length', 'echo_time', 'image_type',
               'imaged_nucleus', 'imager_pixel_spacing', 'lossy_image_compression', 'magnetic_field_strength',
               'mr_acquisition_type', 'number_of_temporal_positions', 'manufacturer', 'manufacturer_model_name',
               'modality', 'pixel_spacing', 'series_description', 'series_uid', 'spatial_resolution', 'view_position',
               'repetition_time', 'scan_options', 'scanning_sequence', 'sequence_name', 'sequence_variant',
               'slice_thickness', 'software_version', 'spacing_between_slices'],
        'NM': ['study_uid', 'case_ids', 'body_part_examined', 'lossy_image_compression', 'radiopharmaceutical',
               'manufacturer', 'manufacturer_model_name', 'modality', 'series_description', 'series_uid'],
        'PT': ['study_uid', 'case_ids', 'body_part_examined', 'lossy_image_compression', 'radiopharmaceutical',
               'manufacturer', 'manufacturer_model_name', 'modality', 'series_description', 'series_uid',
               'slice_thickness'],
        'RF': ['study_uid', 'case_ids', 'contrast_bolus_agent', 'detector_type', 'pixel_spacing', 'manufacturer',
               'manufacturer_model_name', 'modality', 'series_description', 'series_uid'],
        'US': ['study_uid', 'case_ids', 'lossy_image_compression', 'manufacturer', 'manufacturer_model_name',
               'modality', 'series_description', 'series_uid', 'transducer_type'],
        'XA': ['study_uid', 'case_ids', 'image_type', 'lossy_image_compression', 'manufacturer',
               'manufacturer_model_name', 'modality', 'series_description', 'series_uid']
    }

    selected_columns = [col for col in column_map.get(modality_type, []) if col in result_mod.columns]
    result_mod = result_mod.loc[:, selected_columns]

    dict_rename = {'study_uid': 'imaging_studies.submitter_id'}
    result_mod.rename(columns=dict_rename, inplace=True)
    result_mod['type'] = modality_type.lower() + '_series_file'
    result_mod['data_type'] = 'DICOM'
    result_mod['data_format'] = 'DCM'
    result_mod['data_category'] = modality_type
    result_mod['submitter_id'] = result_mod["series_uid"]  # The submitter id of each series node will also be the Series UID
    
    output_file = os.path.join(output_path, modality_type.lower() + '_series_RSNA_' + date + '.tsv')
    result_mod.to_csv(output_file, sep='\t', index=False)  # write to TSV file in specified output directory
    print('\n{0} Series TSV created at {1}'.format(modality_type, output_file))

if __name__ == "__main__":
    try:
        print(f'Arguments received: {sys.argv}')  # Debugging line
        powertools_path = sys.argv[1]  # path to powertools file (.csv)
        assert powertools_path.endswith('.csv'), 'Invalid file type'
        output_path = sys.argv[2] if len(sys.argv) > 2 else '.'  # default to current directory if not provided
        
        df1 = pd.read_csv(powertools_path, low_memory=False)
        
        # Debugging info
        csv_filename = str(os.path.basename(powertools_path)).replace('.csv', '')
        print(f'CSV Filename: {csv_filename}')
        
        x = csv_filename.split("_")
        print(f'Splitted CSV Filename: {x}')
        
        if len(x) < 3:
            print("Filename does not match the expected format. Setting a default date.")
            date = "default_date"  # You can set this to any default date value or logic you prefer
        else:
            date = x[2]
        
        print(f'Date Extracted: {date}')
        
        csv_filename = csv_filename + '.csv'
        print_info(df1)
        gather_TSV_info(df1, date, output_path)
    except IndexError:
        print("You did not specify a file")
        sys.exit(1)  # abort due to error
    except FileNotFoundError:
        print("The specified file was not found")
        sys.exit(1)  # abort due to error
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)  # abort due to error
