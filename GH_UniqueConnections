import rhinoscriptsyntax as rs
import Rhino as rh
import ghpythonlib as ghp
import scriptcontext
import clr
clr.AddReference("Grasshopper")
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree
from System import Object

import ghpythonlib.components as ghc

def datatolist(aTree):
    theList = []
    for i in range(aTree.BranchCount ):
        thisListPart = []
        thisBranch = aTree.Branch(i)
        for j in range(len(thisBranch)):
            thisListPart.append( thisBranch[j] )
        theList.append(thisListPart)
    return theList

def listtodata(raggedList):
    rl = raggedList
    result = DataTree[object]()
    for i in range(len(rl)):
        temp = []
        for j in range(len(rl[i])):
            temp.append(rl[i][j])
        #print i, " - ",temp
        path = GH_Path(i)
        result.AddRange(temp, path)
    return result


def ifequal(b,a):
	indiceslist = []
	for lA in a:
		counter = 0
		for lB in b:
			if (lA == lB):
				indiceslist.append(counter)
			counter += 1
	return indiceslist


def flattenlist(list):
    return [item for sublist in list for item in sublist]

def duplist(listA,listB):
    return [listA for i in range(len(listB))]

def findintpoints(curves,sphere,names):
    curve = []
    linepoints = []
    namesout = []
    centroid = rs.SurfaceAreaCentroid(sphere)[0]
    for i in range(len(curves)):
        if rs.CurveBrepIntersect(curves[i],sphere):
            curve.append(curves[i])
            linepoints.append(rs.CurveBrepIntersect(curves[i],sphere)[1])
            namesout.append(names[i])
    h = flattenlist([duplist(namesout[i],linepoints[i])for i in range(len(linepoints))])
    g = flattenlist(linepoints)
    return [rs.AddLine(centroid,item)for item in g],h,curve

def makevectors(listoflines):
    return [rs.VectorCreate(rs.CurveEndPoint(item),rs.CurveStartPoint(item))for item in listoflines]

def sortbykey(key, list):
    return [j for k, j in sorted(zip(key, list))]

def rounditems(list):
    return [round(item,6) for item in list]

def trimstring(string):
    outlist = []
    for item in string:
        outlist.append(str(item)[:str(item).find(".")+6])
    return outlist

def sumnumber(numberlist):
    return sum([float(item)for item in numberlist])

def sort(list):

    s = [sumnumber(item)for item in list]

    j = sortbykey(s,list)

    t = [rounditems(item)for item in j]

    numbers = [trimstring(item) for item in t]

    return [",".join(item)for item in [sorted(item)for item in numbers]]

def sumandsortbyVec(vectors,list):
    s = [sumnumber(item)for item in vectors]
    j = sortbykey(s,list)
    return j


newlist = []
for item in Beams:
    if item is not None:
        newlist.append(item)

spheres = []
for item in Nodes:
    spheres.append(rs.AddSphere(item,0.25))

ele = [findintpoints(newlist,item,Names)[0]for item in spheres]
ele2 = [findintpoints(newlist,item,Names)[2]for item in spheres]
n = [findintpoints(newlist,item,Names)[1]for item in spheres]

def VecAbsolute(listofvecs):
    x = []
    y = []
    z = []
    for item in listofvecs:
        x.append(abs(item[0]))
        y.append(abs(item[1]))
        z.append(abs(item[2]))
    return zip(x,y,z)


vec = [makevectors(j)for j in ele]
vecAbs = [VecAbsolute(item)for item in vec]

trimvec = [sort(item)for item in vec]
trimvecAbs = [sort(item)for item in vecAbs]

breps = spheres
vecjoin = [",".join(item)for item in trimvec]

sortvecs = sorted([item for item in set(vecjoin)])
uniqueindexes = [ifequal(vecjoin,[item])for item in sortvecs]

def groupbyindex(list,indexlist):
    return [list[item]for item in indexlist]

g_breps = listtodata([groupbyindex(breps,item)for item in uniqueindexes])
g_beams = [groupbyindex(ele2,item)for item in uniqueindexes]
g_vecs = [groupbyindex(ele,item)for item in uniqueindexes]
g_names = [groupbyindex(n,item)for item in uniqueindexes]

def stringjoin(list):
    return [",".join([str(item)for item in list])]

groupedmembers = listtodata([stringjoin(item)for item in g_names])