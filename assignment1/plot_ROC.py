

import matplotlib.pyplot as plt
from sklearn.metrics import auc

def addpoints(fpr, tpr):
    w = 2*(len(fpr) - 1) + 1
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

    res[0][w - 1] = 1
    res[1][w - 1] = 1
    return res


fpr = [0, 0]
tpr = [0, 1]
#fpr = [0, 0.1, 0.3, 0.5, 0.7, 0.8, 0.9];
#tpr = [0.3, 0.5, 0.7, 0.75, 0.8, 0.95, 1];
res = addpoints(fpr, tpr)
fpr = res[0]
tpr = res[1]
roc_auc = auc(fpr, tpr)

plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()