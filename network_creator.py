import networkx as nx
from util import outputDataAsJSON, parseData, createHTMLGraph


# CSV --> JSON --> nx.Graph --> visualization

INPUT_CSV_PATH = 'data/netflix_titles.csv'
JSON_OUTPUT_PATH = 'clean_data.json'


# Parse input CSV and output clean data to JSON file (CSV --> JSON)
clean_data: list[dict[str, str]] = parseData(INPUT_CSV_PATH)
outputDataAsJSON(JSON_OUTPUT_PATH, clean_data)

# JSON --> nx.Graph
G = nx.Graph()

for i, entry in enumerate(clean_data):
    # if i == 500:
    #     print('Graph created: ' + str(i) + ' nodes')
    #     break

    # NOTE: edges between directors and cast would make network tripartite
    # NOTE: nodes are unique only by name, someone that's been cast and director
    #   keeps last role to be processed

    G.add_node(entry['title'], type='movie')

    # Add director nodes and movie-director edges
    for director in entry['director'].split(', '):
        if director != '':
            G.add_node(director, type='director')
            G.add_edge(entry['title'], director)

    # Add cast nodes and movie-cast edges
    for cast_member in entry['cast'].split(', '):
        if cast_member != '':
            G.add_node(cast_member, type='cast')
            G.add_edge(entry['title'], cast_member)

# Browser rendered graph
# createHTMLGraph(G, 'network.html')

# GEXF keeps all attributes, render in Gephi
nx.write_gexf(G, 'network.gexf')
