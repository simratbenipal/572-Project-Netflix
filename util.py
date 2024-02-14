import json
import csv
import random
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


def createGraph(data: list[dict[str, str]], weights: list[list[int]]) -> list[nx.Graph]:
    """
    Create a GEXF file for each of the given probability distributions

    NOTE: edges between directors and cast would make network tripartite
    NOTE: nodes are unique only by name, someone that's been cast and director
      keeps last role to be processed
    """
    outcomes: list = ['IN', 'OUT']
    created_graphs: list = []

    for prob in weights:
        G = nx.Graph()

        for entry in data:
            G.add_node(entry['title'], type='movie')

            # Add director nodes and movie-director edges
            for director in entry['director'].split(', '):
                if director != '' and random.choices(outcomes, prob, k=1)[0] == 'IN':
                    G.add_node(director, type='director')
                    G.add_edge(entry['title'], director)

            # Add cast nodes and movie-cast edges
            for cast_member in entry['cast'].split(', '):
                if cast_member != '' and random.choices(outcomes, prob, k=1)[0] == 'IN':
                    G.add_node(cast_member, type='cast')
                    G.add_edge(entry['title'], cast_member)

        # GEXF keeps all attributes, render file in Gephi
        nx.write_gexf(G, f'output/network_{prob[0]}%.gexf')
        created_graphs.append(G)

    return created_graphs


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
