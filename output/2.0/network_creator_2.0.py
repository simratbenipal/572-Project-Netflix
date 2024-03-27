import pandas as pd
import networkx as nx

# Read the CSV data into a pandas DataFrame
df = pd.read_csv('netflix_titles.csv')

# Filter rows where type is 'Movie' and director and cast are not empty
movies_df = df[(df['type'] == 'Movie') & (df['director'].notnull()) & (df['cast'].notnull())]

# Create an undirected graph
G = nx.Graph()

# Add nodes for movies, directors, and cast
for index, row in movies_df.iterrows():
    movie = row['title']
    directors = row['director'].split(', ')
    cast = row['cast'].split(', ')
    G.add_node(movie, type='movie')
    for director in directors:
        G.add_node(director, type='director')
    for actor in cast:
        G.add_node(actor, type='cast')

# Add edges between movies and directors/cast
for index, row in movies_df.iterrows():
    movie = row['title']
    directors = row['director'].split(', ')
    cast = row['cast'].split(', ')
    for director in directors:
        G.add_edge(movie, director)
    for actor in cast:
        G.add_edge(movie, actor)
        for director in directors:
            G.add_edge(director, actor)

# Export the graph to a GEXF file
nx.write_gexf(G, 'movie_network_undirected.gexf')
