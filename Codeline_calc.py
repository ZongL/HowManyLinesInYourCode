#coding: UTF-8
import matplotlib.pyplot as plt
import os

def plot_X_Y(XX,YY):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.bar(range(1,len(XX)+1),YY,0.6,color="red")
    ax.set_xticks(range(1,len(XX)+1))
    ax.set_xticklabels(XX)
    plt.xticks(rotation=90)#Set the ticks on x-axis
    plt.xlabel("X-axis")
    plt.ylabel("Y-Frequency")
    plt.show()


def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # if you want to ignore some files, add below if-condition
            if ((s == "_doc")or(s == "Release") or (s == "Output") or (s=='_tools')or(s=='Model')):
                continue
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList

def GetFileLineNUM(file_path):
    myfile_f = open(file_path)
    lines = len(myfile_f.readlines())
    myfile_f.close()
    return lines

def cut_to_words(str_input):
    str_input_temp = str_input.split('\\')
    return str_input_temp[-1]

if __name__ == "__main__":
    list = GetFileList('your path eg. C:\Program Files', [])
    file_name = []
    file_NUM  = []
    for i in range(0,len(list)):
            if ('.c' == list[i][-2:]):
                file_name.append(cut_to_words(list[i]))
                file_NUM.append(GetFileLineNUM(list[i]))
                #print(file_name)
                #print(file_NUM)

    #plot_X_Y(file_name,file_NUM)
    dic = dict(zip(file_name, file_NUM))
    for item in dic.items():
        print(item)
    #sort dic by value.
    dict= sorted(dic.items(), key=lambda x:x[1], reverse = True)
    for i in dict:
        print(i)


