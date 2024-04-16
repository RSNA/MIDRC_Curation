from radgraph import RadGraph
radgraph = RadGraph(model_type="radgraph-xl")
annotations = radgraph(["no acute cardiopulmonary abnormality"])
annotations
{'0': {'text': 'no acute cardiopulmonary abnormality', 'entities': {
    '1': {'tokens': 'acute', 'label': 'Observation::definitely absent', 'start_ix': 1, 'end_ix': 1, 'relations': []},
    '2': {'tokens': 'cardiopulmonary', 'label': 'Anatomy::definitely present', 'start_ix': 2, 'end_ix': 2,
          'relations': []},
    '3': {'tokens': 'abnormality', 'label': 'Observation::definitely absent', 'start_ix': 3, 'end_ix': 3,
          'relations': [['located_at', '2']]}}, 'data_source': None, 'data_split': 'inference'}}

print(annotations)
