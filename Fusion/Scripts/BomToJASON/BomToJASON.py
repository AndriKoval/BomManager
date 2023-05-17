# Author- BM
# Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import json
import os

def getallcomponents(root: adsk.fusion.Component) -> list[adsk.fusion.Component]:
    components = [root]
    ids=[root.id]
    for occ in root.allOccurrences:
        if occ.component.id not in ids:
            components.append(occ.component)
            ids.append(occ.component.id)
    return components


def getcomponents(root: adsk.fusion.Component) -> list[adsk.fusion.Component]:
    components = []
    for occ in root.occurrences:
        if occ.component not in components:
            components.append(occ.component)
    return components


def getbom(root: adsk.fusion.Component):
    components = getallcomponents(root)
    occurences = []
    compstrs = []
    for component in components:
        compstrs.append({
            'id':component.id,
            'PartNumber':component.partNumber,
            'Description':component.description
            })
        for child in getcomponents(component):
            occurences.append({
                'InComp':component.id, 
                 'OfComp':child.id, 
                 'Count':component.allOccurrencesByComponent(child).count
                 })
    return {'Components':compstrs, 'Occurences':occurences}


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        root = design.rootComponent
        bom = getbom(root)
        with open('E:/CODE/BomManager/Fusion/Scripts/BomToJASON/bom.json','w', encoding='utf16') as out:
            _as_json = json.dumps(bom, indent=4, ensure_ascii=False)
            out.write(_as_json)
        print('Done')
    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
