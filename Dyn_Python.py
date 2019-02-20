Revit
Python

# imports#
import clr

clr.AddReference('ProtoGeometry')
clr.AddReference('ProtoGeometry')
clr.AddReference("RevitNodes")
clr.AddReference("RevitServices")
clr.AddReference("RevitAPI")
import Revit
import System
import RevitServices
import Autodesk
from Revit.Elements import *
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
from Autodesk.DesignScript.Geometry import *

doc = DocumentManager.Instance.CurrentDBDocument
app = DocumentManager.Instance.CurrentUIApplication.Application

# all elements of category
userCategories = doc.Settings.Categories
cat = IN[0]
names, ids, builtInNames = [], [], []
for i in userCategories:
    names.append(i.Name)
    ids.append(i.Id.IntegerValue)
    tempID = i.Id.IntegerValue
    builtInNames.append(System.Enum.ToObject(BuiltInCategory, tempID))

cat = []
for item in builtInNames:
    if "OST_StructuralFraming" == str(item):
        cat.append(item)

# for elements in doc
elements = []
for i in range(len(cat)):
    elements.append(FilteredElementCollector(doc).OfCategory(cat[0]).ToElements())
    elements = elements[0]

# for used elements
elements = []
for i in range(len(cat)):
    elements.append(FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(cat[0]).ToElements())
    elements = elements[0]

OUT = elements

# open files in background#
items = IN[0]
typelist = list()
for i in items:
    try:
        typelist.append(app.OpenDocumentFile(i))
    except:
        typelist.append(list())
OUT = typelist

# collect all elements in revit model#
import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
categories = doc.Settings.Categories

model_cat = []
anno_cat = []
ana_cat = []
internal_cat = []

for c in categories:
    if c.CategoryType == CategoryType.Model:
        model_cat.append(Revit.Elements.Category.ById(c.Id.IntegerValue))
    elif c.CategoryType == CategoryType.Annotation:
        anno_cat.append(Revit.Elements.Category.ById(c.Id.IntegerValue))
    elif c.CategoryType == CategoryType.AnalyticalModel:
        ana_cat.append(Revit.Elements.Category.ById(c.Id.IntegerValue))
    elif c.CategoryType == CategoryType.Internal:
        internal_cat.append(Revit.Elements.Category.ById(c.Id.IntegerValue))

OUT = model_cat, anno_cat, ana_cat, internal_cat


"""Collect All elements in Model"""
userCategories = doc.Settings.Categories
# extract workset's name and ids
ids = []
for i in userCategories:
    try:
        ids.append(i.Id.IntegerValue)
    except:
        ids.append(0)
# Assign your output to the OUT variable
builtInNames = []
for x in ids:
    try:
        builtInNames.append(System.Enum.ToObject(BuiltInCategory, x))
    except:
        pass

listed = []
for z in builtInNames:
    try:
        listed.append(FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(z).ToElements())
    except:
        pass

OUT = listed, builtInNames

"""set parameter by name"""
OUT = [item.SetParameterByName("Cross-Section Rotation",45)for item in x]

x = IN[0]

element = x

OUT = x.GetParameterValueByName("Mark")

element.SetParameterByName

"""to set a new location line for framing"""
x = IN[0]

t= [item.Location for item in x]

o = [item.Offset(500)for item in t]

r = []
for i in range(len(x)):
	r.append(x[i].SetLocation(o[i]))

endpoint = item.EndPoint.X for item in ?

OUT = r

#Get type Parameter#
t = [item.Type for item in x]

OUT = item.GetParameterValueByName("Width")

UnwrapElement

#if Mrk contains#
x = IN[0]

Marks = [item.GetParameterValueByName("Mark")for item in x]

wing = []
for i in range(len(x)):
	if "WG" in Marks[i]:
		wing.append(x[i])

OUT = wing


#open detach and saveas revit files
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

if isinstance(IN[0], list):
	files = IN[0]
else:
	files = [IN[0]]



options = OpenOptions()
options.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets

worksharingOptions = WorksharingSaveAsOptions()
worksharingOptions.SaveAsCentral = True

SaveOptions = SaveAsOptions()
SaveOptions.SetWorksharingOptions(worksharingOptions)

for file in files:
	modelpath = FilePath(file)
	newdoc = app.OpenDocumentFile(modelpath,options)
	newfile = file[:-4] + "detached" + ".rvt"
	newdoc.SaveAs(newfile,SaveOptions)
	newdoc.Close(False)

OUT = 0
#open detach and saveas revit files


#to get elements as part od a truss
UnwrapElement(IN[0]).Members


#swtich current view
import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIDocument

TransactionManager.Instance.EnsureInTransaction(doc)
TransactionManager.Instance.ForceCloseTransaction()

view = UnwrapElement(IN[0])
uidoc.RequestViewChange( view )
#switch current view

#make column slanted#
OUT = [item.SetParameterByName("Column Style",1)for item in ele]



#Make input a list
def makelist(input):
	if isinstance(input, list):
		files = input
	else:
		files = [input]