import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### reading files (!!! all the files which are ended with extention ".msa" are reding !!!)
unsorted_files = (glob.glob('*.msa'))
files = sorted(unsorted_files, key=lambda x: float(x.split('.')[0]))

### helper function to read data file and return first two columns as lists
def read(file_name):
    df = pd.read_csv(file_name,sep=',',skiprows=20,skipfooter=1, header=None, engine='python')
    xdata=np.asarray(df[0])    
    ydata=np.asarray(df[1])
    return xdata, ydata

#!finding the closest value of a list to a certain value
def closest(list, k):
    lst = np.asanyarray(list)
    idx = (np.abs(lst - k)).argmin()
    return idx

### helper function to get normal value to normalized all ydatas
def normal_value(norm_file):
    xdata, ydata = read(norm_file)
    i_ave=closest(xdata, 1.5)
    f_ave=closest(xdata, 2)
    arr_ave = ydata[i_ave:f_ave]
    return np.average(arr_ave)


def get_maxid():
    max_list = []; id_list = []
    for f in files:
        x,y = read(f)
        itimes = closest(x,1.65)
        ftimes = closest(x,1.95)
        max_range = np.max(y[itimes:ftimes])
        maxyid = closest(y,max_range)
        max_list.append(max_range)
        id_list.append(maxyid)
    maxyid = np.argmax(max_list)
    return maxyid, id_list

def get_xlabels():
    xid,_ = read(files[maxyid])
    x = [0, 0.5, 1.0, 1.5, 2.0]
    label_id = []
    for d in x:
        lab = closest(xid,d)
        label_id.append(lab)
    xlabels = []
    for i in range(len(x)):
        k = xid[label_id[i]]
        xlabels.append(k)
    formatedx = ["%.1f" % member for member in xlabels]
    return label_id,formatedx


nfiles = int(len(files))
maxyid,id_list = get_maxid()
nor_value =normal_value(files[maxyid])
for i in range(nfiles):
    labeler = files[i].split('.')
    x,y = read(files[i])
    j = id_list[maxyid] - id_list[i] 
    plt.plot(range(j,j+len(x)), y/nor_value, label=labeler[0])


ylimi = 2950/nor_value; ylimf = 4000/nor_value
plt.ylim([ylimi,ylimf])

label_id, xlabels = get_xlabels()
plt.vlines(id_list[maxyid],ylimi,ylimf,ls = '--',colors='r')
plt.xticks(label_id, xlabels)
plt.title("normelized to {}".format(files[maxyid]))
plt.xlabel("Distance [nm]")
plt.ylabel("Intesity [a.u.]")
plt.legend()
plt.show()
#plt.savefig("fig.png")