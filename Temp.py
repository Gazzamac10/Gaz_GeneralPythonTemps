import os


#directory = "C:\\temp\Gazza\MFS\\"

#d = []
#for i in range(42):
    #d.append(directory + "Con_" + str(i+1))


#for item in d:
    #if not os.path.exists(item):
        #os.makedirs(item)



path = "P:\UKLON06-BE-Structural\Projects\Structures - Kapps\BIM" \


folders = os.listdir(path)



list1 = []
for root, dirs, files in os.walk(path):
    for name in files:
        if ".rte" in  name:
            list1.append(name)

list2 = [item for item in set(list1)]

for item in list2:
    print item

