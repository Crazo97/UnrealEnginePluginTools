#All the unreal property that needed to create a material and fbx in Unreal Engine
from unreal import (
    AssetToolsHelpers,
    AssetTools,
    EditorAssetLibrary,
    Material,
    MaterialFactoryNew,
    MaterialProperty,
    MaterialEditingLibrary,
    MaterialExpressionTextureSampleParameter2D as TexSample2D,
    AssetImportTask,
    fbxImportUI,

)
import os
#Placing the material in the folder and have it organized when the code execute in Unreal Engine
class UnrealUtility:
    def __init__(self):
        self.substanceRootDir = "/game/Substance/" # The location in the under content folder in unreal engine
        self.baseMaterialName = "M_SubstanceBase" #The name of the material
        self.substanceTempDir = "game/Substance/Temp/" # The location of the folder
        self.baseMaterialPath = self.substanceRootDir + self.baseMaterialName #Finding the path for the Base Material
        self.baseColorName = "Base Color" #Map name for Base color
        self.normalName = "Normal" #Map name for Normal
        self.occRoughnessMetallicName = "OcclusionRoughnessMetallic" #Map name for Ambient Occlusion, Roughness, and Metallic Map

    #Creating a Material and connecting the node in the blue print
    def FindOrCreateBaseMaterial(self):
        if EditorAssetLibrary.does_asset_exist(self.baseMaterialPath):
            return EditorAssetLibrary.load_asset(self.baseMaterialPath)
        
        #Creating the Base Material and placing it the right folder
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(self.baseMaterialName, self.substanceRootDir, Material, MaterialFactoryNew())

        #Connecting the Base Color map to the Base color node base material in the Material Editor
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 0)
        baseColor.set_editor_property("parameter_name", self.baseColorName)
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR)

        #Connecting the normal map to the normal node base material in the Material Editor
        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400)
        normal.set_editor_property("parameter_name", self.normalName)
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)
        
        #Connecting the Roughness/Metallic map to the Red, Green, Blue node base material in the Material Editor
        occRoughnessMetallic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 800)
        occRoughnessMetallic.set_editor_property("parameter_name", self.occRoughnessMetallicName)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "G", MaterialProperty.MP_ROUGHNESS)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "B", MaterialProperty.MP_METALLIC)

        #Saving the Base material
        EditorAssetLibrary.save_asset(baseMat.get_path_name())
        return baseMat
    
        # Opening the window and find the fbx files to import in Unreal Engine
    def LoadMeshFromPath(self, meshPath):
        meshName = os.path.split(meshPath)[-1].replace(".fbx","")
        importTask = AssetImportTask()
        importTask.replace_existing = True
        importTask.filename = meshPath
        importTask.destination_path = "/game/" + meshName
        importTask.save = True
        importTask.automated = True

        #Importing the fbx files with only the mesh and and not the material and not the joint
        fbxImportOptions = fbxImportUI()
        fbxImportOptions.import_mesh = True
        fbxImportOptions.import_as_skeletal = False
        fbxImportOptions.import_material = False
        fbxImportOptions.static_mesh_import_data.combine_meshes = True

        #Creating the import fbx option
        importTask.options = fbxImportOptions

        #Saving the fbx model in Unreal Engine
        AssetToolsHelpers.get_asset_tools().import_asset_tasks([importTask])
        return importTask.get_objects()[0]

        #Loading the right file as .fbx
    def LoadFromDir(self, fileDir):
        for file in os.listdir(fileDir):
            if " .fbx" in file:
                self.LoadMeshFromPath(os.path.join(fileDir, file)) 