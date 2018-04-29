

import matplotlib.pyplot as plt
from sklearn.metrics import auc

def addpoints(fpr, tpr):
    w = 2*len(fpr)
    h = 2
    res = [[0 for x in range(w)] for y in range(h)]
    res_index = 0
    for i in range(0, len(fpr) - 1):
        res[0][res_index] = fpr[i]
        res[1][res_index] = tpr[i]
        res_index = res_index + 1
        res[0][res_index] = fpr[i]
        res[1][res_index] = tpr[i + 1]
        res_index = res_index + 1

    res[0][w - 2] = res[0][w - 3]
    res[1][w - 2] = 1

    res[0][w - 1] = 1
    res[1][w - 1] = 1
    return res

def preparedata(fpr, tpr):
    res = addpoints(fpr1, tpr1)
    fprres = res[0]
    tprres = res[1]
    roc_auc_res = auc(fprres, tprres)
    return fprres, tprres, roc_auc_res

# No SMOTE data.
# 5-NN
fpr1 = [0.0001, 0.0002, 0.0002, 0.0003, 0.0005, 0.0006]
tpr1 = [0, 0, 0, 0.125, 0.2, 0.25]
fpr1, tpr1, auc1 = preparedata(fpr1, tpr1)

# Random forest
fpr2 = [0, 0, 0.0001, 0.0002, 0.0002, 0.0003, 0.0007, 0.0008, 0.0009]
tpr2 = [1, 1, 0.8, 0.4286, 0.1667, 0.8571, 0.875, 0.6667]
fpr2, tpr2, auc2 = preparedata(fpr2, tpr2)

# Logistic regression
fpr3 = [0.0001, 0.0001, 0.0002, 0.0004, 0.0004, 0.0004, 0.0005, 0.0005, 0.0006, 0.0007]
tpr3 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
fpr3, tpr3, auc3 = preparedata(fpr3, tpr3)

plt.figure()
lw = 2
plt.plot(fpr1, tpr1, color='cyan', ls='-',
         lw=lw, label='ROC curve (area = %0.2f)' % auc1)
plt.plot(fpr2, tpr2, color='red', ls='--',
         lw=lw, label='ROC curve (area = %0.2f)' % auc2)
plt.plot(fpr3, tpr3, color='green', ls='-.',
         lw=lw, label='ROC curve (area = %0.2f)' % auc3)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='-')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()