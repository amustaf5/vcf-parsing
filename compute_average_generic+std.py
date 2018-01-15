import sys
import numpy as np


def computeAverage(argv):
    '''computing average of values over a list of file
    given the index of a key value
    and a comma separated string of index values columns
    '''
    path_list = argv[0]
    key_index = int(argv[1])
    # list of the columns on which compute the average
    value_index_list = list(map(int, argv[2].split(",")))

    # index of the column to compute dev standard
    std_index = int(argv[3])

    # conta sempre, aggiungi al dizionario lista di valori pari all'interavllo di colonne in input
    # conta il numero di bootstrap per il quale dividere
    # array variabile o lista?
    # indice lista in cui scrivere= for i in range(value_index)
    d = {}
    d_std = {}
    bootstrap_paths = list(map(lambda t: t.strip(), open(path_list, 'r').readlines()))
    n = len(bootstrap_paths)
    for p in bootstrap_paths:
        with open(p, 'r') as f:
            for line in f:
                # get the key of the dictionary
                k = line.split()[key_index]

                # reading all the values in a numpy array
                # by the chosen columns given in input
                values = np.fromiter(
                    map(lambda i: line.split()[i], value_index_list),
                    np.float)

                # read the value to use for computing standard dev
                value_std = float(line.split()[std_index])

                if k in d.keys():
                    # summing the existing array values with the current
                    # np.array values (sum by position)
                    d[k] = d[k] + values

                    # dictionary of the standard deviations
                    d_std[k].append(value_std)
                else:
                    d[k] = values
                    d_std[k] = [value_std]
            f.close()

    for k in d.keys():
        mean_values = d[k]/n
        std_value = np.std(d_std[k])
        print('{:s}\t{:s}\t{:f}'
              .format(k, "\t".join(map(str, mean_values)), std_value))


if __name__ == "__main__":
    computeAverage(sys.argv[1:])
