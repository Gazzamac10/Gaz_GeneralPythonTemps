import os


path  = "C:\\Users\\mccarthyg\\Documents\\Batchplot\\"

list1 = []
list2 = []
for item in os.listdir(path):
    list1.append(path+item)
    list2.append(path+"MFSIII-ACM-00-XX-DR-SE-"+item)


"""for i in range(len(list1)):
    os.renames(list1[i],list2[i])"""