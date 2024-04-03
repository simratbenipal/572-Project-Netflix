import pandas as pd
import networkx as nx

# Read the CSV data into a pandas DataFrame
# HRef: https://www.w3schools.com/python/pandas/pandas_csv.asp
df = pd.read_csv('netflix_titles.csv')

# Things to note: Cast and Directors have multiple CSV values
# Some cast and directors have missing values (null), ignore those
# Only include Movies
# Filter rows where type is 'Movie' and director and cast are not empty
# Href: https://www.geeksforgeeks.org/ways-to-apply-an-if-condition-in-pandas-dataframe/
movies_df = df[(df['type'] == 'Movie') & (df['director'].notnull()) & (df['cast'].notnull())]

# Create an undirected graph
G = nx.Graph()

# Iterate over all the rows in CVS, split the director, split the cast
# add the nodes as movies, and director and cast (if not added before)   
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

# Iterate over the rows in CSV, for every movie split the director and cast, and for each director, add an edge from movie to each director
# add an edge from movie to each actor
# add an edge from each actor to each director
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
# Href: https://stackoverflow.com/questions/31450090/writing-a-networkx-graph-with-position-color-ect-to-gexf
nx.write_gexf(G, 'movie_network_undirected.gexf')

# This will make the graph tripartite
# Edge set #1 : Movie to Director(s)
# Edge set #2 : Movie to Cast Member(s)
# Edge set #3 : Cast to Director, if they have worked together
