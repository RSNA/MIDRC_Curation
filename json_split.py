
# Splitting JSON file into JSON file for each annotation
# Author: Maryam Vazirabad
# Last updated: 5/3/23
import json

with open(r'E:\1c_mdai_rsna_project_MwBeK3Nr_annotations_labelgroup_all_2021-01-08-164102.json') as f:
    data = json.load(f)

label_info = {}
for label_group in data['labelGroups']:
    for label in label_group['labels']:
        label_info[label['id']] = {
            'name': label['name'],
            'description': label['description'],
            'scope': label['scope']
        }

for annotation in data['datasets'][0]['annotations']:
    label_id = annotation['labelId']
    label_name = label_info[label_id]['name']
    label_description = label_info[label_id]['description']
    label_scope = label_info[label_id]['scope']

    new_data = {
        'id': annotation.get('id'),
        'parentId': annotation.get('parentId'),
        'isImported': annotation.get('isImported', False),
        #'isInterpolated': annotation.get('isInterpolated', False),
        'createdAt': annotation.get('createdAt'),
        'createdById': annotation.get('createdById'),
        'updatedAt': annotation.get('updatedAt'),
        'updatedById': annotation.get('updatedById'),
        'updateHistory': annotation.get('updateHistory'),
        'StudyInstanceUID': annotation.get('StudyInstanceUID'),
        #'SeriesInstanceUID': annotation.get('SeriesInstanceUID'),
        #'SOPInstanceUID': annotation.get('SOPInstanceUID'),
        #'frameNumber': annotation.get('frameNumber'),
        'labelId': label_id,
        'labelName': label_name,
        'labelDescription': label_description,
        'labelScope': label_scope,
        #'annotationNumber': annotation.get('annotationNumber'),
        'height': annotation.get('height'),
        'width': annotation.get('width'),
        'data': annotation.get('data'),
        'note': annotation.get('note'),
        'radlexTagIds': annotation.get('radlexTagIds'),
        'reviews': annotation.get('reviews'),
        'reviewsPositiveCount': annotation.get('reviewsPositiveCount'),
        'reviewsNegativeCount': annotation.get('reviewsNegativeCount'),
        'groupId': annotation.get('groupId')
    }

    with open(f"{annotation.get('id')}_{annotation.get('StudyInstanceUID')}.json", 'w') as f:
        json.dump(new_data, f)
