import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, UnitUtils

doc = DocumentManager.Instance.CurrentDBDocument

def CollectElements(category):
    collector = FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType()
    return list(collector)

def GetElementVolume(element):
    parameter = element.LookupParameter('Volumen')  # Hier Volumen anpassen
    if parameter and parameter.HasValue:
        volume_internal_units = parameter.AsDouble()
        return volume_internal_units
    return 0.0

categories = [
    BuiltInCategory.OST_Walls,
    BuiltInCategory.OST_Floors,
    BuiltInCategory.OST_StructuralFoundation,
    BuiltInCategory.OST_StructuralColumns,
    BuiltInCategory.OST_StructuralFraming
]

data = []

for category in categories:
    elements = CollectElements(category)
    category_name = doc.Settings.Categories.get_Item(category).Name
    total_volume_cubic_feet = sum([GetElementVolume(element) for element in elements])
    conversion_factor = 0.0283168  # Conversion factor from cubic feet to cubic meters
    total_volume_cubic_meter = total_volume_cubic_feet * conversion_factor
    data.append([category_name, len(elements), total_volume_cubic_meter])

##################################### Muss entsprechend abgeändert werden bei einer eigenen Verwendung
csv_file_path = r'C:\Users\fedenhofner.ICOM\Documents\BBB_Versuche\CSV-Datei.csv'

try:
    with open(csv_file_path, 'w') as csv_file:
        csv_file.write('Category\tCount\tTotal Volume (cubic meters)\n')
        for entry in data:
            csv_file.write('\t'.join(str(x) for x in entry) + '\n')
        
    result = 'CSV-Datei wurde erfolgreich erstellt: {}'.format(csv_file_path)
except Exception as e:
    result = str(e)

result