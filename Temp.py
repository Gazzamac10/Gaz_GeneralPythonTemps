import os


#directory = "C:\\temp\Gazza\MFS\\"

#d = []
#for i in range(42):
    #d.append(directory + "Con_" + str(i+1))


#for item in d:
    #if not os.path.exists(item):
        #os.makedirs(item)



path = "C:\\temp\Gazza\MFS\DWG"

folders = os.listdir(path)

"""for item in folders:
    print len(os.listdir(path +"\\"+item))
    print os.listdir(path +"\\"+item)"""


list = ["12","6","2"]

for item in list:
    print list.index("6")