from radgraph import RadGraph

# Create a RadGraph object with the desired model type
radgraph = RadGraph(model_type="radgraph-xl")

# Perform inference on a sample text
annotations = radgraph(["no acute cardiopulmonary abnormality"])

# Print the annotations
print(annotations)
