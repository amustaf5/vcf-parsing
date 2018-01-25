import sys
import argparse
import numpy as np
from sklearn import metrics
from sklearn.metrics import matthews_corrcoef as mcc
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


def classificator(argv):
    '''takes in input a generic file with a column of class and a column of
    scores associated to that class, the two positions of class column and
    score column, and optional imput threshold at wich get the scores, if not
    provided get the one that maximize the mcc
    '''
    parser = argparse.ArgumentParser(usage='%(prog)s [options] arg1 arg2',
                                     description='create a classificator')
    parser.add_argument('file_data',
                        type=str,
                        help='input file')
    parser.add_argument('-c',
                        '--classind',
                        type=int,
                        dest='classind',
                        action='store',
                        default=0,
                        help=('index of the column containing the classes'))
    parser.add_argument('-s',
                        '--scoreind',
                        type=int,
                        dest='scoreind',
                        action='store',
                        default=1,
                        help=('index of the column containing the score 
                              associated to the class'))
    parser.add_argument('-t',
                        '--threshold',
                        type=float,
                        dest='threshold',
                        action='store',
                        help=('threshold value at wich compute the evaluation
                              scores'))

    args = parser.parse_args()

    data = open(args.file_data, 'r').readlines()

    y = np.fromiter(map(lambda t: t.rstrip().split()[args.classind], data),
                    np.int)
    scores = np.fromiter(map(lambda t: t.rstrip().split()[args.scoreind], data),
                         np.float)
    n = len(scores)

    if args.threshold:
        pred_list = []
        for s in scores:
            if s > args.threshold:
                pred_list.append(1)
            else:
                pred_list.append(0)
        # compute confusion matrix
        tn, fp, fn, tp = confusion_matrix(y, pred_list)
        # false positive rate 
        fpr = fp / (fp + tn)
        # true positive rate / recall / sensitivity
        tpr = tp / (tp + fn)
        # compute accuracy / ACC
        acc_t = accuracy_score(y, pred_list)
        # compute matthews correlation coefficent
        mcc_t = mcc(y, pred_list)
        # print fpr, tpr, thresholds
        print('threshold= {:4f} {:4f} {:4f} {:4f} {:4f} {:4f} ')
        
        "threshold=", mcc_max[1], "acc=", mcc_max[4], "AUC=", metrics.roc_auc_score(y, scores), "mcc_max=", mcc_max[0], "fpr=", mcc_max[2], "tpr=", mcc_max[3]

    else:
        fpr, tpr, thresholds = metrics.roc_curve(y, scores)

        # maximixe MCC
        prediction = {}
        mcc_max = (0, 0, 0, 0, 0)
        for i in range(len(thresholds)):
            t = thresholds[i]
            prediction[t] = []
            for s in scores:
                if s > t:
                    prediction[t].append(1)
                else:
                    prediction[t].append(0)
            # compute matthews correlation coefficent
            acc_t = accuracy_score(y, prediction[t])
            mcc_t = (mcc(y, prediction[t]), t, fpr[i], tpr[i], acc_t)
            if mcc_t[0] > mcc_max[0]:
                mcc_max = mcc_t

        # print fpr, tpr, thresholds
        print "threshold=", mcc_max[1], "acc=", mcc_max[4], "AUC=", metrics.roc_auc_score(y, scores), "mcc_max=", mcc_max[0], "fpr=", mcc_max[2], "tpr=", mcc_max[3]


if __name__ == "__main__":
    classificator(sys.argv[1:])
