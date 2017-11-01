import os


directory = "C:\\temp\Gazza\MFS\\"

d = []
for i in range(41):
    d.append(directory + "Con_" + str(i+1))


for item in d:
    if not os.path.exists(item):
        os.makedirs(item)
