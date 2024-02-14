from util import *


# CSV --> JSON --> nx.Graph --> GEXF file

INPUT_CSV_PATH = 'data/netflix_titles.csv'
JSON_OUTPUT_PATH = 'output/clean_data.json'


# Parse input CSV and output clean data to JSON file (CSV --> JSON)
clean_data: list[dict[str, str]] = parseData(INPUT_CSV_PATH)
outputDataAsJSON(JSON_OUTPUT_PATH, clean_data)

# Probability of adding a person. Expressed as: [p(include), p(don't include)]
weights: list[list[int]] = [[50, 50], [60, 40], [70, 30], [80, 20], [100, 0]]

# JSON --> nx.Graph --> GEXF file
graphs: list = createGraph(clean_data, weights)