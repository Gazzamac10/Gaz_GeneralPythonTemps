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