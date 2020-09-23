import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create a document.
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
 
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        # Get the root component of the active design
        rootComp = design.rootComponent
                
        # Get extrude features
        extrudes = rootComp.features.extrudeFeatures

        # Create sketch XY Plane    
        sketches = rootComp.sketches   
        sketch = sketches.add(rootComp.xYConstructionPlane)
        sketchCircles = sketch.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(0, 0, 0)
        circle = sketchCircles.addByCenterRadius(centerPoint, 3.0)
        
        # Get the profile defined by the circle
        prof = sketch.profiles.item(0)
                      
        # Extrude Sample 1: A simple way of creating typical extrusions (extrusion that goes from the profile plane the specified distance).
        # Define a distance extent of 1 cm
        distance = adsk.core.ValueInput.createByReal(1)
        extrude1 = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)        
        # Get the extrusion body
        body1 = extrude1.bodies.item(0)
        body1.name = "Cylinder"

        # Get the state of the extrusion
        health = extrude1.healthState
        if health == adsk.fusion.FeatureHealthStates.WarningFeatureHealthState or health == adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState:
            message = extrude1.errorOrWarningMessage
        
        # Get the state of timeline object
        timeline = design.timeline
        timelineObj = timeline.item(timeline.count - 1);
        health = timelineObj.healthState
        message = timelineObj.errorOrWarningMessage
    
        # Change the workspace (next 2 lines are already above and are not needed here)
        #
        # app = adsk.core.Application.get()
        # ui = app.userInterface
        workspaces = ui.workspaces
        camWorkspace = workspaces.itemById("CAMEnvironment")
        camWorkspace.activate()
        
        #Activate the Setup Dialog
        cmd_id1 = "IronSetup"
        ui.commandDefinitions.itemById(cmd_id1).execute()
        
        # Old machine selection 
        # cmd_id2 = "IronMachineBrowserSelection"
        # ui.commandDefinitions.itemById(cmd_id2).execute()
        
        # Press ok
        # cmd_id2 = "CommitCommand"
        # ui.commandDefinitions.itemById(cmd_id2).execute()
               
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))