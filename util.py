import json
import csv
import networkx as nx
from pyvis.network import Network


def parseData(input_csv_path: str) -> list[dict[str, str]]:
    """
    Parse a CSV file
    """
    clean_data: list[dict[str, str]] = []
    tv_show_counter: int = 0

    with open(input_csv_path, newline='') as csvfile:
        # DictReader converts each row into a dict using header values as keys
        csvreader = csv.DictReader(csvfile)

        fields_to_delete: list = ['show_id', 'type', 'country', 'description']

        for row in csvreader:
            # Skip TV Shows
            if row['type'] == 'TV Show':
                tv_show_counter += 1
                continue

            # Delete unnecessary fields
            for key in fields_to_delete:
                del row[key]

            clean_data.append(row)

    print('TV Shows: ' + str(tv_show_counter))
    print('Movies: ' + str(len(clean_data)))
    print('Total: ' + str(tv_show_counter + len(clean_data)))

    return clean_data


def outputDataAsJSON(output_path: str, data: list) -> None:
    """
    Creating a JSON file as an intermediate step makes it easier to understand and
    manipulate the data rather than directly creating the network from the CSV file.
    """
    with open(output_path, 'w') as jsonfile:
        jsonfile.write('[\n')

        for i, entry in enumerate(data):
            # Convert dictionary to JSON string
            json_string: str = json.dumps(entry, indent=4)
            jsonfile.write(json_string)

            # Commas between dictionaries, don't add a comma after last one
            jsonfile.write(',' if i < len(data) - 1 else '')

        jsonfile.write('\n]')


def createHTMLGraph(G: nx.Graph, graph_name: str) -> None:
    """
    Creates an HTML file for the graph, better for smaller networks
    Time taken to render in browser:
    1000 nodes ~3:30 mins -- 2000 nodes ~9:20 mins
    """
    # Create Pyvis graph from NetworkX graph
    nt = Network(height='100%', width='100%')
    nt.from_nx(G)

    # Color nodes
    color_map: dict = { 'movie': 'gold', 'director': 'lightgreen', 'cast': 'lightblue' }
    for node in nt.nodes:
        # node (dict) preserves node attributes created in NX
        nt.get_node(node['id'])['color'] = color_map[node['type']]

    nt.show(graph_name, notebook=False)
