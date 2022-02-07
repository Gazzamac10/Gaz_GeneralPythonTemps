import rhinoscriptsyntax as rs
import Rhino as rh
import ghpythonlib as ghp
import scriptcontext
import clr

clr.AddReference("Grasshopper")
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree


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


def datatolist(aTree):
    theList = []
    for i in range(aTree.BranchCount):
        thisListPart = []
        thisBranch = aTree.Branch(i)
        for j in range(len(thisBranch)):
            thisListPart.append(thisBranch[j])
        theList.append(thisListPart)
    return theList


def shift(seq, n):
    a = n % len(seq)
    return seq[-a:] + seq[:-a]


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


def sortbykey(key, list):
    return [j for k, j in sorted(zip(key, list))]


def planeNewOrigin(plane, point):
    return rs.PlaneFromNormal(point, plane.ZAxis, plane.XAxis)


def makeabs(vec):
    return [abs(item) for item in vec]


def matchPointTypes(pointlist):
    k = [str(round(float(item), 1)) for item in pointlist]
    out = []
    for item in k:
        if "." in item:
            if len(item.split(".")[-1]) == 3:
                out.append(item)
            elif len(item.split(".")[-1]) == 2:
                out.append(item + "0")
            else:
                out.append(item + "00")
        else:
            out.append(item + ".000")
    # return "("+", ".join(out)+")"
    return out


def splitline(pointA, points):
    out = []
    for item in points:
        out.append(rs.AddLine(pointA, item))
    return out


def getlength(points):
    d = []
    p = []
    p1 = points[0]
    ps = points[1:]
    for item in ps:
        d.append(rs.Distance(p1, item))
        p.append(points)
    return sum(d), p, d


def orderpoints(point, points):
    out = []
    dist = []
    for item in points:
        if point != item:
            out.append(item)
    for item in out:
        dist.append(rs.Distance(item, point))
    return [point] + sortbykey(dist, out), sorted(dist)


def reorderlist(distances, list):
    return [list[0]] + sortbykey(distances, list[1:])


Accuracy = 2


def createVectors(node, curves, names, sizes):
    sphere = rs.AddSphere(node, 0.05)
    centroid = rs.SurfaceAreaCentroid(sphere)[0]
    c = []
    d = []
    test = []
    j = []
    j2 = []
    k = []
    k2 = []
    l = []
    for i in range(len(curves)):
        if rs.CurveBrepIntersect(curves[i], sphere):
            c.append(curves[i])
            j.append(names[i])
            j2.append(sizes[i])
    pts = [rs.CurveBrepIntersect(item, sphere)[1] for item in c]
    for i in range(len(pts)):
        if len(pts[i]) > 1:
            d.append(splitline(centroid, pts[i]))
            k.append([j[i]] + [j[i]])
            k2.append([j2[i]] + [j2[i]])
        else:
            d.append([c[i]])
            k.append([j[i]])
            k2.append([j2[i]])
    e = flattenlist(d)
    ks = flattenlist(k)
    ks2 = flattenlist(k2)
    sp = []
    ep = []
    distsp = []
    distep = []
    curveout = []
    sizeout = []
    nameout = []
    outindex = []
    for item in e:
        sp.append(rs.CurveStartPoint(item))
        ep.append(rs.CurveEndPoint(item))
    for item in sp:
        distsp.append(rs.Distance(node, item))
    for item in ep:
        distep.append(rs.Distance(node, item))
    for i in range(len(sp)):
        if distsp[i] < distep[i]:
            curveout.append(e[i])
            sizeout.append(ks[i])
            nameout.append(ks2[i] + "_start")
            outindex.append(i)
        else:
            # curveout.append(rs.AddLine(rs.CurveEndPoint(e[i]),rs.CurveStartPoint
            # (e[i])))
            curveout.append(e[i])
            sizeout.append(ks[i])
            nameout.append(ks2[i] + "_end")
            outindex.append(i)
    if len(pts) > 1:
        shifpoint = [shift(flattenlist(pts), i) for i in range(len(flattenlist(pts)))]
        distlistsum = [getlength(item)[0] for item in shifpoint]
        distlist = [getlength(item)[2] for item in shifpoint]
        distlistsort = sortbykey(distlistsum, distlist)
        pointslist = sortbykey(distlistsum, [getlength(item)[1][0] for item in shifpoint])
        plist1 = pointslist[-1]
        p1 = plist1[0]
        return curveout, [round(sum(distlistsum), Accuracy)], [sphere], sizeout, p1, flattenlist(pts), centroid, len(
            plist1), nameout, distlistsum
    else:
        return curveout, ["Not Connected"], [sphere], sizeout, rs.AddPoint(centroid), [
            rs.AddPoint(centroid)] + pts, centroid, 1, nameout, 0


def matchpointcures(point, curves, sizes, names):
    outcurves = []
    outsizes = []
    outnames = []
    for i in range(len(curves)):
        if rs.IsPointOnCurve(curves[i], point) is True:
            outcurves.append(curves[i])
            outsizes.append(sizes[i])
            outnames.append(names[i])
    return outcurves, outsizes, outnames


gc = [createVectors(item, beams, sizes, marks)[0] for item in nodes]
UniqueCode = listtodata([createVectors(item, beams, sizes, marks)[1] for item in nodes])
Spheres = listtodata([createVectors(item, beams, sizes, marks)[2] for item in nodes])
se = [createVectors(item, beams, sizes, marks)[3] for item in nodes]
firstPoint = [createVectors(item, beams, sizes, marks)[4] for item in nodes]
ps = [createVectors(item, beams, sizes, marks)[5] for item in nodes]
cen = [createVectors(item, beams, sizes, marks)[6] for item in nodes]
lencurve = [createVectors(item, beams, sizes, marks)[7] for item in nodes]
mk = [createVectors(item, beams, sizes, marks)[8] for item in nodes]


def createcoords(pointlist):
    return [rs.PointCoordinates(item) for
            item in pointlist]


pcoords = [createcoords(item) for item in ps]
firstpointcoords = createcoords(firstPoint)


def reorder(fp, po, gcurves, secs, mks):
    # op = orderpoints(fp,po)[0]
    op1 = rs.SortPointList(po)
    op2 = rs.SortPointList(po)[::-1]
    if rs.Distance(op1[0], op1[1]) > rs.Distance(op2[0], op2[1]):
        op = op1
    else:
        op = op2
    # op = shift(op,len(op)-op.index(fp))
    mp1 = [matchpointcures(item, gcurves, secs, mks)[0][0] for item in op]
    mp2 = [matchpointcures(item, gcurves, secs, mks)[1][0] for item in op]
    mp3 = [matchpointcures(item, gcurves, secs, mks)[2][0] for item in op]
    return op, mp1, mp2, mp3


Points1 = [reorder(firstpointcoords[i], pcoords[i], gc[i], se[i], mk[i])[0] for i in range(len(gc))]
GroupedCurves1 = [reorder(firstpointcoords[i], pcoords[i], gc[i], se[i], mk[i])[1] for i in range(len(gc))]
Sections1 = [reorder(firstpointcoords[i], pcoords[i], gc[i], se[i], mk[i])[2] for i in range(len(gc))]
Marks1 = [reorder(firstpointcoords[i], pcoords[i], gc[i], se[i], mk[i])[3] for i in range(len(gc))]


def sortcorner(cornercurves, cornerpoints, cornersections):
    d1 = [rs.VectorCreate(rs.CurveEndPoint(item), rs.CurveStartPoint(item)) for item in cornercurves]
    d = sortbykey([rs.VectorUnitize(item) for item in d1], cornercurves)
    e = sortbykey([rs.VectorUnitize(item) for item in d1], cornerpoints)
    f = sortbykey([rs.VectorUnitize(item) for item in d1], cornersections)
    return d, e, f


GroupedCurves = []
Points = []
Sections = []
Marks = []
for i in range(len(GroupedCurves1)):
    if len(GroupedCurves1[i]) == 2:
        GroupedCurves.append(sortcorner(GroupedCurves1[i], Points1[i], Sections1[i])[0])
        Points.append(sortcorner(GroupedCurves1[i], Points1[i], Sections1[i])[1])
        Sections.append(sortcorner(GroupedCurves1[i], Points1[i], Sections1[i])[2])
        Marks.append(sortcorner(GroupedCurves1[i], Points1[i], Marks1[i])[2])
    else:
        GroupedCurves.append(GroupedCurves1[i])
        Points.append(Points1[i])
        Sections.append(Sections1[i])
        Marks.append(Marks1[i])

GroupedCurves = listtodata(GroupedCurves1)
Points = listtodata(Points1)
Sections = listtodata(Sections1)
Marks = listtodata(Marks1)

"""
se = [reorder(firstpointcoords[i],pcoords[i],gc[i],se[i])[2]for i in range(len(gc))]
ps = [reorder(firstpointcoords[i],pcoords[i],gc[i],se[i])[0]for i in range(len(gc))]

def findchord(centroid,points,sizes):

    oz = centroid.Z

    px = [item.X for item in points]
    py = [item.Y for item in points]

    pp = [rs.AddPoint(px[i],py[i],oz)for i in range(len(px))]

    dist = [rs.Distance(centroid,item)for item in pp]

    return sortbykey(dist,sizes)[0]
    return oz


def checkangle(centroid,points,sizes):
    l = [rs.AddLine(centroid,item)for item in [ps[1][0],ps[1][-1]]]
    if sorted(rs.Angle2(l[0],l[-1]))[0] < 100:
        return findchord(centroid,points,sizes),sizes[1]
    else:
        return sizes[0][1]

def checkangle2(centroid,points,sizes):
    pnts = [points[0],points[-1]]
    l = [rs.AddLine(centroid,item)for item in pnts]
    if sorted(rs.Angle2(l[0],l[-1]))[0] < 100:
        return findchord(centroid,points,sizes),sizes[1]
    else:
        return sizes[1]   

out= []
for i in range(len(se)):
    if len(se[i]) > 3:
        out.append(se[i][1:-1])
    elif len(se[i]) == 3:
        out.append([checkangle2(cen[i],ps[i],se[i])])
    elif len(se[i]) == 2:
        out.append([findchord(cen[i],ps[i],se[i])])
    else:
        out.append(se[i])



UniqueSecs = listtodata(out)
"""