import matplotlib.pyplot as plt
import matplotlib
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from deap import gp
import pandas as pd
import csv
###########################################################################
def plot_trees(best):
    """ create tree plots from best array """
    for i in range(len(best)):
        nodes, edges, labels = gp.graph(best[i])
#       print(best)
        matplotlib.rcParams['figure.figsize'] = (10.0, 10.0)

        g = nx.Graph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        pos = graphviz_layout(g, prog="dot")
    
        f = plt.figure()
        nx.draw_networkx_nodes(g, pos, node_size=1500, 
                               font_size=8, node_color='lightblue')
        nx.draw_networkx_edges(g, pos)
        nx.draw_networkx_labels(g, pos, labels, font_size=8)
        if (i < 10):
            plotfile = "tree_0" + str(i) + ".pdf"
        else:    
            plotfile = "tree_" + str(i) + ".pdf"
        f.savefig(plotfile)
###########################################################################
def plot_stats(df):
    matplotlib.rcParams['figure.figsize'] = (10.0, 10.0)
    ax = df.plot()
    fig = ax.get_figure()
    fig.savefig('stats.pdf')
###########################################################################
def plot_fitness(fit):
    fitdf = pd.DataFrame(fit, columns=['Fitness', 'Value'])
    ax = fitdf.plot(x='Value', y='Fitness', kind='scatter')
    fig = ax.get_figure()
    fig.savefig('fitness.pdf')
###########################################################################
def create_file(data,label):
    """ append label as column to data then write out file with header """
    for i in range(len(data)):
        data[i].append(label[i])
        
    # create header
    header = list()
    for i in range(len(data[0])-1):
        header.append('X' + str(i))
    header.append('Class')
        
    # print data to results.tsv
    datadf = pd.DataFrame(data,columns=header) # convert to DF
    datadf.to_csv('results.tsv', sep='\t', index=False)
###########################################################################
def read_file(fname):
    """ return both data and x
        data = rows of instances
        x is data tranposed to rows of features """
    with open(fname) as data:
        dataReader = csv.reader(data, delimiter='\t')
        data = list(list(int(elem) for elem in row) for row in dataReader)
    #transpose into x
    inst_length = len(data[0])
    x = []
    for i in range(inst_length):
        y = [col[i] for col in data]
        x.append(y)
    del y
    return data, x