import os


#directory = "C:\\temp\Gazza\MFS\\"

#d = []
#for i in range(42):
    #d.append(directory + "Con_" + str(i+1))


#for item in d:
    #if not os.path.exists(item):
        #os.makedirs(item)



path = "P:\UKLON06-BE-Structural\Projects\_all\!Annual Leave"

folders = os.listdir(path)

"""for item in folders:
    print len(os.listdir(path +"\\"+item))
    print os.listdir(path +"\\"+item)"""


test = [folders[0]]


for dirs in os.walk(path):
    print dirs





"""for root, dirs, files in os.walk(path):
    for name in files:
        if "TestingGazGazgaz.txt" ==  name:
            print name"""