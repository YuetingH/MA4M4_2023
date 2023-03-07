import numpy as np
import networkx as nx

# This will filter warnings, which can be lengthy but sometimes useful. You may comment it out if you want to see them.
import warnings
warnings.filterwarnings('ignore')

# Check https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.louvain.louvain_communities.html
import networkx.algorithms.community as nx_comm



def rearrange_graph(G, comm):
    '''
    Input: 
        G: (un)directed (un)weighted graph
        comm: a list of sets, each of which comprises nodes belonging to the same community        
    Output: 
        G_perm: it maintains the coherence of the input graph G, wherein nodes are rearranged to represent clusters of nodes within the corresponding community
    '''
    # Initialise an empty new graph with the same type as G
    G_perm = G.copy(); G_perm.clear() 
    
    # Arrange the sets in the comm list in a descending order based on the size of each set
    comm_copy = comm.copy(); # retain the input "comm"
    comm_copy.sort(key=len, reverse = True) 
    
    # Add nodes
    for comm_set in comm_copy:
        G_perm.add_nodes_from(list(comm_set))
    
    # Add edges
    for edge in G.edges.data():
        G_perm.add_edges_from([edge])
        
    return G_perm


def compute_perm_adj(G, comm):
    '''
    Input:
        G: (un)directed (un)weighted graph
        comm: a list of sets, each of which comprises nodes belonging to the same community
    Output:
        A_perm: permuted adjacency matrix
    '''
    G_perm = rearrange_graph(G, comm)
    A_perm = nx.adjacency_matrix(G_perm).todense()
    
    return A_perm


def compute_asso_one_run(G, perm_comm, weight, resolution, threshold, seed):
    '''
    We create an unweighted dummy graph. An edge is generated if two nodes are assigned to the same community when performing community detection in graph G. 
    
    Input:
        G: (un)directed (un)weighted graph
        perm_comm: a list of sets, each of which comprises nodes belonging to the same community
        weight, resolution, threshold: prescribed parameters for community detection
        seed: random seed
    Output:
        A_dummy: a matrix indicates whether two nodes are assigned to the same community
    '''
    
    # community detection results
    G_comm = nx_comm.louvain_communities(G, weight = weight, resolution = resolution, threshold = threshold, seed = seed) 
    # get a graph with permuted nodes but no edges
    G_dummy = rearrange_graph(G, perm_comm); G_dummy.remove_edges_from(list(G_dummy.edges))
    
    for comm in G_comm:
        comm = list(comm)
        G_dummy_edges = [(a, b) for idx, a in enumerate(comm) for b in comm[idx + 0:]]
        G_dummy.add_edges_from(G_dummy_edges)
    A_dummy = nx.adjacency_matrix(G_dummy).todense()
    
    return A_dummy


def compute_asso(G, comm, n_runs, weight, resolution, threshold, perm = True):
    '''
    Input:
        G: (un)directed (un)weighted graph
        comm: a list of sets, each of which comprises nodes belonging to the same community
        n_runs: the number of community detection runs
        weight, resolution, threshold: prescribed parameters for community detection
        perm: whether to permute association matrix according to comm
    Output:
        A_asso: a matrix indicates the proportion of times two nodes are assigned to the same community
    '''
    
    A_asso = np.zeros((len(G.nodes), len(G.nodes)))
    
    if perm:
        for i in range(n_runs):
            A_asso += compute_asso_one_run(G, comm, seed = i, weight = weight, resolution = resolution, threshold = threshold)
    else:
        for i in range(n_runs):
            A_asso += compute_asso_one_run(G, [set(G.nodes)], seed = i, weight = weight, resolution = resolution, threshold = threshold)
    A_asso /= n_runs
    
    return A_asso


def comm_detection_dict(G, seed, weight, resolution, threshold):
    '''
    Input:
        G: (un)directed (un)weighted graph
        seed: random seed
        weight, resolution, threshold: prescribed parameters for community detection.
    Output:
        G_comm_dict: a dictionary format of {node: label}, where each label is an integer, and nodes with the same label are assigned to the same community.
    '''
    
    G_comm = nx_comm.louvain_communities(G, seed = seed, weight = weight, resolution = resolution, threshold = threshold)
    G_comm_dict = {node: 0 for node in G.nodes}
    
    index = 0
    for comm in G_comm:
        for node in comm:
            G_comm_dict[node] = index
        index += 1
        
    return G_comm_dict


import sklearn
from sklearn import metrics

def compute_nMI(G, n_runs, weight, resolution, threshold):
    '''
    Input:
        G: (un)directed (un)weighted graph
        n_runs: the number of community detection runs
        weight, resolution, threshold: prescribed parameters for community detection. 
    Output:
        nMI_matrix: a matrix indicates the similarity between different partitions
    '''
    
    # Obtain community results using different random seeds. Convert results to labels and save them in a numpy array.
    n_runs_labels = []
    for i in range(n_runs):
        label = np.array(list(comm_detection_dict(G, seed = i, weight = weight, resolution = resolution, threshold = threshold).values()))
        n_runs_labels.append(label)
    n_runs_labels = np.array(n_runs_labels)
    
    # Calculate the level of dissimilarity between each pair of partition results using NMI
    nMI_matrix = np.zeros((n_runs, n_runs))
    for i in range(n_runs):
        for j in range(n_runs):
            nMI_matrix[i, j] = sklearn.metrics.normalized_mutual_info_score(n_runs_labels[i], n_runs_labels[j])
    
    return nMI_matrix


def aggregated_results(G, n_runs, weight = 'weight', resolution = 1, threshold = 1e-07, seed = None):
    '''
    Input: 
        G: (un)directed (un)weighted graph
        n_runs: the number of community detection runs
        weight, resolution, threshold, seed: prescribed parameters for community detection. 
    Output:
        A: adjacency matrix of G
        A_perm: the permutated adjacency matrix of G according to community detection results
        A_asso: the association matrix for checking the stochasticity of community detection in G
        A_perm_asso: the permutated association matrix according to community detection results
    '''
    
    # Original adajency matrix
    A = nx.adjacency_matrix(G).todense()
    
    # Permutated adjacency matrix
    G_comm = nx_comm.louvain_communities(G, weight = weight, resolution = resolution, threshold = threshold, seed = seed)
    A_perm = compute_perm_adj(G, G_comm)
    
    # Unpermutated association matrix
    A_asso = compute_asso(G, G_comm, n_runs = n_runs, weight = weight, resolution = resolution, threshold = threshold, perm = False)
    
    # Permutated association matrix
    A_perm_asso = compute_asso(G, G_comm, n_runs = n_runs, weight = weight, resolution = resolution, threshold = threshold)
    
    # nMI matrix
    nMI_matrix = compute_nMI(G, n_runs = n_runs, weight = weight, resolution = resolution, threshold = threshold)
    
    return A, A_perm, A_asso, A_perm_asso, nMI_matrix