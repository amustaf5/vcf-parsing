import sys
import numpy as np
import scipy.cluster.hierarchy as sch


def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step


def cluster_indices(cluster_assignments):
    n = cluster_assignments.max()
    indices = []
    for cluster_number in range(1, n + 1):
        indices.append(np.where(cluster_assignments == cluster_number)[0])
    return indices


def compute_clustering(data, method, criterion, cutoff):
    X = np.fromiter(map(lambda t: float(t.split()[2]), data), np.float)

    Y = sch.linkage(X, method)

    cluster_assignments = sch.fcluster(Y, cutoff, criterion)

    n_clusters = cluster_assignments.max()

    # assining labels
    pz_list = []
    for line in data:
        e = line.split()
        if e[0] not in pz_list:
            pz_list.append(e[0])

        if e[1] not in pz_list:
            pz_list.append(e[1])

    indices = cluster_indices(cluster_assignments)
    d = {}
    for k, ind in enumerate(indices):
        # print(k, ind)
        d[k] = list(map(lambda t: pz_list[t], ind))

    print("cutoff=", cutoff, "n_clusters=", n_clusters)
    h = {}
    for k in d.keys():
        #print("> cluster", k, "n_elements=", len(d[k]))
        h[len(d[k])] = h.get(len(d[k]), 0) + 1

    for k in h.keys():
        print("n elements per cluster=", k, "count=", h[k])


# reading all the lines of the input file
# made of three columns space separated
# id_1 id_2 distance
data = open(sys.argv[1], 'r').readlines()

# read the method of linkage algoritm to use
method = str(sys.argv[2])
criterion = str(sys.argv[3])
# cutoff = float(sys.argv[4])

print("method=", method, "criterion=", criterion)
for cutoff in frange(0, 2, 0.1):
    print()
    compute_clustering(data, method, criterion, cutoff)
