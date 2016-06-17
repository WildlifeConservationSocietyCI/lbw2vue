# 16/05/24

# creates a vue mesh object at an arbitrary location that serves as a dummy.
# if desired real-world (or Vue) coordinates are known, the objects can be placed there too.
# get_species() allows user to select a plant from a list of all installed LW plants
# Other existing modules can be used to duplicate, move, and scale object, and
# LW is working to write code that replaces object with LW plant object suitable for use in Vue

import os, sys, tempfile

# Import laubwerk module after setting the import path accordingly. Not sure why we have to do this, because
# the Laubwerk installer usually sets PYTHONPATH, which should be used automatically.
sys.path.append('C:\Program Files\Laubwerk\Python')
import laubwerk

# import the lbwtoobj helper script
# earlier versions of Vue apparently do not define __file__ properly, but also they don't need the
# current path to be appended, we just check for that case using try.
try:
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))
except:
    pass
import lbwtoobjvue

# imports wx from native Vue install location
vueRootPath = GetVueRootPath()
vuePythonFolder = os.path.abspath(os.path.join(vueRootPath,"Python"))
vueScriptsFolder = os.path.abspath(os.path.join(vuePythonFolder,"Scripts"))
wxPythonFolder = os.path.abspath(os.path.join(vuePythonFolder,"PythonLib/site-packages/wx"))
try:
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))
except:
    pass
try:
    import wx
    from wx.lib.splitter import MultiSplitterWindow
except:
    Message("Error: wxPython must be installed to run this program. Please see the installation documentation.",
            "wxPython Not Installed")


# location of root LW plant directory
plants_dir = "C:\\Program Files\\Laubwerk\\Plants\\" 





class SelectPlantVariant(wx.Dialog):

    variants = []
    seasons = []
    params = {}

    def __init__(self, parent, id, title, variants = [], seasons = [], params = []):
        wx.Dialog.__init__(self, parent, id, title, size=(500, 500))

        self.variants = variants
        self.seasons = seasons
        self.params = params

        # defines each of the drop down menus, and their labels
        self.st = wx.StaticText(self, label="Choose plant parameters", pos=(10, 10))
        self.st = wx.StaticText(self, label="Model", pos=(10,50))
        varSelector = wx.ComboBox(self, -1, pos=(150, 50), size=(150, -1), value=self.variants[self.params["variant"]], choices=self.variants, style=wx.CB_READONLY, name="Model")
        self.st = wx.StaticText(self, label="Season", pos=(10, 75))
        seasSelector = wx.ComboBox(self, -1, pos=(150, 75), size=(150, -1), value=self.seasons[self.params["season"]], choices=self.seasons, style=wx.CB_READONLY, name="Season")
        self.st = wx.StaticText(self, label="Leaf Density", pos=(10, 100))
        leafDensityCtrl = wx.SpinCtrlDouble(self, wx.ID_ANY, pos=(150, 100), size=wx.DefaultSize, style=wx.SP_VERTICAL|wx.SP_ARROW_KEYS, value="1.0", min=0.0, max=1.0, initial=1.0, inc=0.1, name="LeafDensity")

        wx.Button(self, wx.ID_OK, "", (50, 420))
        wx.Button(self, wx.ID_CANCEL, "", (250,420))

        varSelector.Bind(wx.EVT_COMBOBOX, self.varSelect)
        seasSelector.Bind(wx.EVT_COMBOBOX, self.seasonSelect)
        leafDensityCtrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.leafDensitySelect)

        self.Bind(wx.EVT_BUTTON, self.OnClose, id=1)
        self.Centre()

    def OnClose(self, event):
        self.Close()

    def varSelect(self, event):
        self.params["variant"] = event.GetSelection()

    def seasonSelect(self, event):
        self.params["season"] = event.GetSelection()

    def leafDensitySelect(self, event):
        self.params["leafDensity"] = event.GetValue()


def doImport():

    # shows open file modal
    openFileDialog = wx.FileDialog(None, "Choose a plant model", plants_dir, "",
                                   "Laubwerk Plant files (*.lbw.gz)|*.lbw.gz",
                                   wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    result = openFileDialog.ShowModal()
    #self.params["filepath"] = openFileDialog.GetPath()
    lbwPlantFilename = openFileDialog.GetPath()
    openFileDialog.Destroy()

    # check how the dialog was dismissed and react accordingly
    if result == wx.ID_CANCEL:
        return

    # load the plant (we need to do this early, so we can present options to the user)
    myPlant = laubwerk.load(lbwPlantFilename)

    # prepare list of options and default settings for the parameter dialog
    myParams = { "leafDensity" : 1.0 }
    myVariants = []
    for idx, model in enumerate(myPlant.models):
        myVariants.append(laubwerk.getLabel(model.labels, "en-US", defaultLabel=model.name))
        if model == myPlant.defaultModel:
            myParams["variant"] = idx

    mySeasons = []
    for idx, qualifier in enumerate(myPlant.defaultModel.qualifiers):
        mySeasons.append(laubwerk.getLabel(myPlant.defaultModel.qualifierLabels[qualifier], "en-US", defaultLabel=qualifier))
        if qualifier == myPlant.defaultModel.defaultQualifier:
            myParams["season"] = idx

    # bring up a plant parameters dialog
    dlg = SelectPlantVariant(None, -1, 'Laubwerk Plant Selector', variants = myVariants, seasons = mySeasons, params = myParams)
    dialogResult = dlg.ShowModal()
    dlg.Destroy()
    if not dialogResult == wx.ID_OK:
        return

    # TODO: determine a proper scene scale
    scale = 0.01

    # create temporary obj and mtl files
    tempObjFile = tempfile.NamedTemporaryFile(suffix=".obj", delete=False)
    tempMtlFile = tempfile.NamedTemporaryFile(suffix=".mtl", delete=False)
    lbwtoobjvue.writeObjByHandle(myPlant, myPlant.models[myParams["variant"]], myPlant.models[myParams["variant"]].qualifiers[myParams["season"]], tempObjFile, scale, tempMtlFile, True, myParams["leafDensity"])

    # we need to close the files so Vue can import it
    tempObjFile.close()
    tempMtlFile.close()

    # use Vue's built in import functionality to get the geometry imported
    vueObj = ImportObject(tempObjFile.name, -1, False, -1)

    # set plant name
    vueObj.SetName(myPlant.name)

    # In Vue, the default Pivot is apparently always centered. We counteract that by subtracting the position.
    vueObj.SetPivotPosition(-vueObj.Position()[0], -vueObj.Position()[1], -vueObj.Position()[2])

    # make sure to remove the temporary OBJ file so we don't fill up the hard drive
    os.remove(tempObjFile.name)
    os.remove(tempMtlFile.name)

    # TODO: store the file as a .vob
    #result = ExportObject(EONString strFilename, boolean bUseParameterizer = true, EONString dstColorPath = "", EONString dstBumpPath = "", EONString dstAlphaPath = "", EONString srcPreviewPicture = "")


if __name__ == "__main__":
    app = None
    del app
    app = wx.App()
    #frame = selectorApp()
    #app.MainLoop()
    doImport()
