import sys
import numpy as np
from sklearn.cluster import KMeans


# reading all the lines of the input file
# made of three columns space separated
# id_1 id_2 distance
data = open(sys.argv[1], 'r').readlines()

# read the number of cluster desired
n = int(sys.argv[2])

X = np.fromiter(map(lambda t: float(t.split()[2]), data), np.float)

# need to reshape for one feature array
X_ = X.reshape(-1, 1)

kmeans = KMeans(n_clusters=n).fit(X_)

labels = kmeans.labels_
centroids = kmeans.cluster_centers_
centroids_distances = kmeans.transform(X_)

print '#ID1\tID2\tDIST_IDS\tLABEL\tCENTROID\tDIST_FROM_CENTROID'
for i in range(len(data)):
    print('{:s}\t{:d}\t{:4f}\t{:4f}'.format(
        data[i].strip(),
        labels[i],
        centroids[labels[i]][0],
        centroids_distances[i][labels[i]]))
