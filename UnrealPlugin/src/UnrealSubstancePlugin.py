import tkinter.filedialog
from unreal import ToolMenuContext, ToolMenus, ToolMenuEntryScript, uclass, ufunction
import sys
import os
import importlib
import tkinter

#Finding the file located in the src folder
srcDir = os.path.dirname(os.path.abspath(__file__))
if srcDir not in sys.path:
    sys.path.append(srcDir)

#Grabing the UnrealUtilites python code from UnrealUnitilies.py
import UnrealUtilities
importlib.reload(UnrealUtilities)

#Creating a Window with the UnrealUnitilies.py 
@uclass()
class LoadFromDirEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute (self, context):
        window = tkinter.Tk()
        window.withdraw()
        fileDir = tkinter.filedialog.askdirectory()
        window.destory()
        UnrealUtilities.UnrealUtility().LoadFromDir(fileDir)


#Creating a Base Material Script 
@uclass()
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self,context: ToolMenuContext) -> None:
        UnrealUtilities.UnrealUtility().FindOrCreateBaseMaterial()

# Creating a Menu Button and name it Substance Plugin on the Top Menu panel in Unreal Engine
class UnrealSubstancePlugin:
    def __init__(self):
        self.subMenuName="SubstancePlugin"
        self.subMenuLabel="Substance Plugin"
        self.InitUI()

    #Creating a Button after clicking Substance Plugin and creating another button and name it Build Base Material
    def InitUI(self):
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")
        self.subMenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", "SubstancePlugin", "Substance Plugin")
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript())
        self.AddEntryScript("LoadfromDir", "Load from Directory", LoadFromDirEntryScript())
        ToolMenus.get().refresh_all_widgets()

    # Naming the UI Tool menu with name and label
    def AddEntryScript(self, name, label, script: ToolMenuEntryScript):
        script.init_entry(self.subMenu.menu_name, self.subMenu.menu_name, "", name, label)
        script.register_menu_entry()

# Running or transfering the python script to execute in Unreal Engine 
UnrealSubstancePlugin()