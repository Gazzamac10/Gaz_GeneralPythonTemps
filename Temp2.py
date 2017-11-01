import os

path = "C:\\temp\Gazza\MFS\DWG"

folders = os.listdir(path)

lista = []
for item in folders:
    lista.append(os.listdir(path + "\\" + item))


pathandfolder = []
for item in folders:
    pathandfolder.append(path + "\\" + item + "\\")


def createlist(path,lista):
    test = []
    for i in range(len(lista)):
        test.append(path+lista[i])
    return test



test = [createlist(pathandfolder[i],lista[i])for i in range(len(lista))]

listofdrawings = [item for sublist in test for item in sublist]

for item in lista:
    print item