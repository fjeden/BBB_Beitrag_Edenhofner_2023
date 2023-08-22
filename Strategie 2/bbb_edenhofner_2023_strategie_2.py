
import ifcopenshell
import csv
import tkinter as tk
from tkinter import filedialog

def choose_ifc_file():
    file_path = filedialog.askopenfilename(filetypes=[("IFC files", "*.ifc")])
    if file_path:
        ifc_entry.delete(0, tk.END)
        ifc_entry.insert(0, file_path)

def choose_csv_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        csv_entry.delete(0, tk.END)
        csv_entry.insert(0, file_path)

def analyze_and_save():
    ifc_file_path = ifc_entry.get()
    csv_file_path = csv_entry.get()

    if not ifc_file_path or not csv_file_path:
        result_label.config(text="Bitte wähle IFC- und CSV-Datei aus.")
        return

    model = ifcopenshell.open(ifc_file_path)
    bauteiltypen = ["IfcWall", "IfcSlab", "IfcFooting", "IfcColumn", "IfcBeam"]
    bauteil_volumina = {typ: {"Anzahl": 0, "Gesamtvolumen": 0} for typ in bauteiltypen}

    for bauteil_typ in bauteiltypen:
        for bauteil in model.by_type(bauteil_typ):
            for relDefines in bauteil.IsDefinedBy:
                if relDefines.is_a("IfcRelDefinesByProperties"):
                    property_set = relDefines.RelatingPropertyDefinition
                    if property_set.is_a("IfcQuantitySet"):
                        for quantity in property_set.Quantities:
                            if quantity.is_a("IfcQuantityVolume") and quantity.Name == "NetVolume":
                                volumen = quantity.VolumeValue
                                bauteil_volumina[bauteil_typ]["Anzahl"] += 1
                                bauteil_volumina[bauteil_typ]["Gesamtvolumen"] += volumen

    with open(csv_file_path, mode="w", newline="") as csv_file:
        fieldnames = ["Bauteiltyp", "Anzahl", "Gesamtvolumen"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for bauteil_typ, daten in bauteil_volumina.items():
            writer.writerow({"Bauteiltyp": bauteil_typ,
                             "Anzahl": daten["Anzahl"],
                             "Gesamtvolumen": daten["Gesamtvolumen"]})

    result_label.config(text="Analyse abgeschlossen. Ergebnisse wurden in " + csv_file_path + " gespeichert.")

# Erstelle das GUI-Fenster
root = tk.Tk()
root.title("IFC Analyzer")

ifc_label = tk.Label(root, text="Wähle IFC-Datei:")
ifc_label.pack()

ifc_entry = tk.Entry(root, width=40)
ifc_entry.pack()

ifc_button = tk.Button(root, text="Durchsuchen", command=choose_ifc_file)
ifc_button.pack()

csv_label = tk.Label(root, text="Wähle CSV-Datei Speicherort:")
csv_label.pack()

csv_entry = tk.Entry(root, width=40)
csv_entry.pack()

csv_button = tk.Button(root, text="Durchsuchen", command=choose_csv_file)
csv_button.pack()

analyze_button = tk.Button(root, text="Analyse durchführen", command=analyze_and_save)
analyze_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
