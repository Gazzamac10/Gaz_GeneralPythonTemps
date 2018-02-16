import os


path  = "C:\\Users\\mccarthyg\\Documents\\Batchplot\\"


list1 = []
for item in os.listdir(path):
    list1.append(item)

def split1(item):
    return item.split("Sheet - ")[1]

def split2(item):
    return item.split(" - ")[0]


f = [split1(list1[i])for i in range(len(list1))]

g = [split2(f[i])for i in range(len(f))]

new = []
for item in g:
    new.append(path+"P-HS1001-CS-"+item+".pdf")


list1 = []
list2 = []
for item in os.listdir(path):
    list1.append(path+item)

for i in range(len(list1)):
    os.renames(list1[i],new[i])

