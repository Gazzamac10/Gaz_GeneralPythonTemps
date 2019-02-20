def UnrollSurface(surface_id, explode=False, following_geometry=x, absolute_tolerance=None, relative_tolerance=None):
    brep = rs.coercebrep(surface_id, True)
    unroll = rh.Geometry.Unroller(brep)
    unroll.ExplodeOutput = explode
    if relative_tolerance is None: relative_tolerance = scriptcontext.doc.ModelRelativeTolerance
    if absolute_tolerance is None: absolute_tolerance = scriptcontext.doc.ModelAbsoluteTolerance
    unroll.AbsoluteTolerance = absolute_tolerance
    unroll.RelativeTolerance = relative_tolerance
    if following_geometry:
        for id in following_geometry:
            geom = rs.coercegeometry(id)
            unroll.AddFollowingGeometry(geom)
    breps, curves, points, dots = unroll.PerformUnroll()
    if not breps: return None
    rc = [scriptcontext.doc.Objects.AddBrep(brep) for brep in breps]
    new_following = []
    for curve in curves:
        id = scriptcontext.doc.Objects.AddCurve(curve)
        new_following.append(id)
    for point in points:
        id = scriptcontext.doc.Objects.AddPoint(point)
        new_following.append(id)
    for dot in dots:
        id = scriptcontext.doc.Objects.AddTextDot(dot)
        new_following.append(id)
    scriptcontext.doc.Views.Redraw()
    if following_geometry: return rc, new_following
    return rc