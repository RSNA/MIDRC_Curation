import torch
from radgraph import RadGraph

# Load the model onto CPU
model_state_path = "path/to/model_state_file"  # Replace with the actual path to your model state file
model_state = torch.load(model_state_path, map_location=torch.device('cpu'))

# Create a RadGraph object with the desired model type
radgraph = RadGraph(model_state=model_state)

# Perform inference on a sample text
annotations = radgraph(["no acute cardiopulmonary abnormality"])

# Print the annotations
print(annotations)
