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
    for i in range(aTree.BranchCount):
        thisListPart = []
        thisBranch = aTree.Branch(i)
        for j in range(len(thisBranch)):
            thisListPart.append(thisBranch[j])
        theList.append(thisListPart)
    return theList


def listtodata(input, none_and_holes=True, source=[0]):
    """Transforms nestings of lists or tuples to a Grasshopper DataTree"""
    from Grasshopper import DataTree as Tree
    from Grasshopper.Kernel.Data import GH_Path as Path
    from System import Array
    def proc(input, tree, track):
        path = Path(Array[int](track))
        if len(input) == 0 and none_and_holes: tree.EnsurePath(path); return
        for i, item in enumerate(input):
            if hasattr(item, '__iter__'):  # if list or tuple
                track.append(i);
                proc(item, tree, track);
                track.pop()
            else:
                if none_and_holes:
                    tree.Insert(item, path, i)
                elif item is not None:
                    tree.Add(item, path)

    if input is not None: t = Tree[object]();proc(input, t, source[:]);return t


def ifequal(b, a):
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


def duplist(listA, listB):
    return [listA for i in range(len(listB))]


def getEndinSRF(curve, brep):
    curvepoints = rs.CurveStartPoint(curve), rs.CurveEndPoint(curve)
    centroid = rs.SurfaceAreaCentroid(brep)[0]
    j = []
    for item in curvepoints:
        if rs.IsPointInSurface(brep, item) is True:
            j.append(item)
    if len(j) > 0:
        return j[0]
    else:
        return centroid


def findintpoints(curves, sphere, names, sizes):
    curve = []
    linepoints = []
    namesout = []
    sizeout = []
    centroid = rs.SurfaceAreaCentroid(sphere)[0]
    for i in range(len(curves)):
        if rs.CurveBrepIntersect(curves[i], sphere):
            curve.append(curves[i])
            linepoints.append(rs.CurveBrepIntersect(curves[i], sphere)[1])
            namesout.append(names[i])
            sizeout.append(sizes[i])
    test = flattenlist([duplist(curve[i], linepoints[i]) for i in range(len(linepoints))])
    ps = [getEndinSRF(item, sphere) for item in test]
    h = flattenlist([duplist(namesout[i], linepoints[i]) for i in range(len(linepoints))])
    so = flattenlist([duplist(sizeout[i], linepoints[i]) for i in range(len(linepoints))])
    g = flattenlist(linepoints)
    cl = [rs.AddLine(centroid, item) for item in g]
    l = [rs.AddLine(ps[i], g[i]) for i in range(len(g))]
    if CentroidBool is False:
        return l, h, curve, so, ps, g
    else:
        return cl, h, curve, so, ps, g


def makevectors(listoflines):
    v = [rs.VectorCreate(rs.CurveEndPoint(item), rs.CurveStartPoint(item)) for item in listoflines]
    return [rs.VectorUnitize(item) for item in v]


def sortbykey(key, list):
    return [j for k, j in sorted(zip(key, list))]


def rounditems(list):
    return [round(item, 7) for item in list]


def trimstring(string):
    outlist = []
    for item in string:
        outlist.append(str(item)[:str(item).find(".") + 5])
    return outlist


def sumnumber(numberlist):
    return sum([float(item) for item in numberlist])


def sort(listA, listB):
    s = [sumnumber(item) for item in listA]

    j = sortbykey(s, listA)
    k = sortbykey(s, listB)
    t = [rounditems(item) for item in j]

    numbers = [trimstring(item) for item in t]
    STnumbers = [sorted(item) for item in numbers]

    return [",".join(item) for item in STnumbers], k


def sumandsortbyVec(vectors, list):
    s = [sumnumber(item) for item in vectors]
    j = sortbykey(s, list)
    return j


if CentroidBool is None:
    CentroidBool = False

newlist = []
for item in Beams:
    if item is not None:
        newlist.append(item)

spheres = []
for item in Nodes:
    spheres.append(rs.AddSphere(item, 0.15))

ele = [findintpoints(newlist, item, Names, Sizes)[0] for item in spheres]
ele2 = [findintpoints(newlist, item, Names, Sizes)[2] for item in spheres]
n = [findintpoints(newlist, item, Names, Sizes)[1] for item in spheres]
s = [findintpoints(newlist, item, Names, Sizes)[3] for item in spheres]
pss = [findintpoints(newlist, item, Names, Sizes)[4] for item in spheres]
tss = [findintpoints(newlist, item, Names, Sizes)[5] for item in spheres]


def VecAbsolute(listofvecs):
    x = []
    y = []
    z = []
    for item in listofvecs:
        x.append(abs(item[0]))
        y.append(abs(item[1]))
        z.append(abs(item[2]))
    return zip(x, y, z)


vec = [makevectors(j) for j in ele]
vecAbs = [VecAbsolute(item) for item in vec]

trimvec = [sort(vec[i], s[i])[0] for i in range(len(vec))]
trimvecS = [sort(vec[i], s[i])[1] for i in range(len(vec))]

trimvecAbs = [sort(vecAbs[i], s[i])[0] for i in range(len(vecAbs))]
trimvecAbsS = [sort(vecAbs[i], s[i])[1] for i in range(len(vecAbs))]

j1 = [flattenlist(item) for item in (zip(trimvec, trimvecS))]
j2 = [flattenlist(item) for item in (zip(trimvecAbs, trimvecAbsS))]
j3 = trimvec
j4 = trimvecAbs

breps = spheres
vecjoin = [",".join(item) for item in j4]


def groupbyindex(list, indexlist):
    return [list[item] for item in indexlist]


def sortUniquebyList(Key, list):
    sortvecs = sorted([item for item in set(Key)])
    uniqueindexes = [ifequal(Key, [item]) for item in sortvecs]
    return [groupbyindex(list, item) for item in uniqueindexes]


sortvecs = sorted([item for item in set(vecjoin)])
uniqueindexes = [ifequal(vecjoin, [item]) for item in sortvecs]

g_breps = sortUniquebyList(vecjoin, breps)
g_beams = sortUniquebyList(vecjoin, ele2)
g_vecs = sortUniquebyList(vecjoin, ele)
g_names = sortUniquebyList(vecjoin, n)
g_sizes = sortUniquebyList(vecjoin, s)


def stringjoin(list):
    return [",".join([str(item) for item in list])]


groupedmembers = listtodata([stringjoin(item) for item in g_names])

g_brepsOUT = listtodata(g_breps)


def FlatSizelist(list):
    return flattenlist([stringjoin(item) for item in list])


fs = [FlatSizelist(item) for item in g_sizes]

brepsSortbySizeOUT = listtodata([sortUniquebyList(fs[i], g_breps[i]) for i in range(len(g_breps))])
SizesOUT = listtodata([sortUniquebyList(fs[i], g_sizes[i]) for i in range(len(g_names))])

