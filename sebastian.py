import csv
import os
import re

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data.extend(row)
    return data

def create_mermaid_edge(up_node, down_node):
    #, connection):
    #return f"{up_node} -->|{connection}| {down_node}"
    return f"{up_node} --> {down_node}"

def create_mermaid_node(node_id, node_path, node_name):
    return f"{node_id}[<u><a href='{node_path}'>{node_name}</a></u>]"

def find_sql_file(file_name):
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == file_name and file.endswith('.sql'):
                return os.path.abspath(os.path.join(root, file))
    return None

def read_sql_file(file_path):
    abs_path = os.path.abspath(file_path)
    with open(abs_path, 'r') as sql_file:
        sql_text = sql_file.read()
    return sql_text

def find_jinja_macros(text):
    macro_pattern = r"{{\s*[^{}]+?\s*}}"
    return re.findall(macro_pattern, text)

def extract_model_ref_names(macros):
    model_names = []
    for macro in macros:
        if 'ref' in macro:
            model_name = macro.split('\'')[1]
            model_names.append(model_name)
    return model_names

def find_string_positions(text, lst):
    return [
        index
        for index, item in enumerate(lst, start=1)
        if text.lower() == item.lower()
    ]

def create_mermaid_diagram(first_line, nodes, edges):
    diagram_text = f"{first_line}\n"
    
    # Add nodes
    for node in nodes:
        diagram_text += f"  {node}\n"
    
    # Add edges
    for edge in edges:
        diagram_text += f"  {edge}\n"
    
    return diagram_text

def point_to_github_model(model_path, current_path, new_path_prefix):
    if model_path.startswith(current_path):
        model_path = new_path_prefix + model_path[len(current_path):]
    return model_path

def write_diagram_to_file(file_path, diagram):
    with open(file_path, 'w') as file:
        file.write(diagram)

ariel = [] #edges
flounder=[] #nodes

csv_file_path = 'sebastian_models.csv'  # Replace with the path to your CSV file
new_path_prefix = "https://github.com/mattwhiteley/little-mermaid" #replace with the Github prefix to deep-link to the files
current_path = os.getcwd()
print(current_path)

model_list = read_csv_file(csv_file_path)
print(f"Base models - finding dependencies: {model_list}")

for node_num, model in enumerate(model_list, start=1):
    #first find the path for the file
    print(f"---- Scanning model: {model}")
    model_path = find_sql_file(model)
    github_path = point_to_github_model(model_path, current_path, new_path_prefix)
    flounder.append(create_mermaid_node(node_num, github_path, model))
    #open the file get the sql text
    
    model_text = read_sql_file(model_path)

    #extract dbt references into a list, with types
    jinja_refs = find_jinja_macros(model_text)
    print(f"Found Model refs: {jinja_refs}")
    new_models = extract_model_ref_names(jinja_refs)
    print(f"Parsed Model: {new_models}")

    # loop through new models:
    for item in new_models:
        # if a model already exists in the list, do nothing, but if it is new, append it to model list
        item_file = (f"{item}.sql")
        if item_file not in model_list:
            print(f'Adding new model to list: {item_file}')
            model_list.append(item_file)

        # for each model, create an edge
        print(model_list)
        up_node_id = find_string_positions(item_file,model_list)[0]
        down_node_id = node_num
        ariel.append(create_mermaid_edge(up_node_id, down_node_id))
    #jinja_refs
    #loop through the list, and for each source/ref append an entry to the model list, and create an edge

#pass node list and edge list to create the Mermaid file
first_line = "flowchart LR" #defaults to left to right flowchart

#write out the little mermaid file
diagram = create_mermaid_diagram(first_line, flounder, ariel)
output_path = 'little_mermaid.mmd'

print(diagram)
write_diagram_to_file(output_path, diagram)
