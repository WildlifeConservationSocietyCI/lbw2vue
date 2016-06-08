import os, sys

VueRootPath = GetVueRootPath()
VuePythonFolder = os.path.abspath(os.path.join(VueRootPath,"Python"))
VueScriptsFolder = os.path.abspath(os.path.join(VuePythonFolder,"Scripts"))
wxPythonFolder = os.path.abspath(os.path.join(VuePythonFolder,"PythonLib/site-packages/wx"))

# This should be set to LW default install location
laubPlants = "C:\Program Files\Hugin"
# imports wx from native Vue install location
try:
    os.chdir(wxPythonFolder)
    import wx
    from wx.lib.splitter import MultiSplitterWindow
    os.chdir(VueScriptsFolder)
except:
    os.chdir(VueScriptsFolder)
    Message("Error: wxPython must be installed to run this program.  Please see the installation documentation.",
            "wxPython Not Installed")


class SelectPlantVariant(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(500, 500))

        self.params = {"filepath": None, "variant": None, "age": None, "season": None}

        self.InitUI()

    # ideally this would be a part of a multipane setup, where one pane is an open file dialog,
    # and the other pane has options for each plant model, which are defined dynamically
    def InitUI(self):
        # shows open file modal
        openFileDialog = wx.FileDialog(self, "Choose a plant model", laubPlants, "",
                                       "Laubwerk Plant files (*.lbw)|*.lbw",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        self.params["filepath"] = openFileDialog.GetPath()
        openFileDialog.Destroy()

        # as stated above, it would be best if these lists were determined dynamically for each plant
        self.variants = ["One", "Two", "Three"]
        self.ages = ["Juvenile", "Adolescent", "Mature"]
        self.seasons = ["Spring", "Summer", "Fall", "Winter"]

        pnl = wx.Panel(self)
        pnl.Show()
        # defines each of the drop down menus, and their labels
        self.st = wx.StaticText(pnl, label="Choose plant parameters", pos=(10, 10))
        self.st = wx.StaticText(pnl, label="Plant variants", pos=(10,50))
        varSelector = wx.ComboBox(pnl, -1, pos=(150,50), size=(150, -1), choices=self.variants, style=wx.CB_READONLY, name="Variations")
        self.st = wx.StaticText(pnl, label="Plant ages", pos=(10, 150))
        ageSelector = wx.ComboBox(pnl, -1, pos=(150,150), size=(150, -1), choices=self.ages, style=wx.CB_READONLY, name="Age")
        self.st = wx.StaticText(pnl, label="Plant Season", pos=(10, 250))
        seasSelector = wx.ComboBox(pnl, -1, pos=(150, 250), size=(150, -1), choices=self.seasons, style=wx.CB_READONLY, name="Season")

        wx.Button(pnl, 1, "Ok", (50, 420))
        wx.Button(pnl, 1, "Close", (250,420))

        varSelector.Bind(wx.EVT_COMBOBOX, self.varSelect)
        ageSelector.Bind(wx.EVT_COMBOBOX, self.ageSelect)
        seasSelector.Bind(wx.EVT_COMBOBOX, self.seasonSelect)

        self.Bind(wx.EVT_BUTTON, self.OnClose, id=1)
        self.Centre()

        return self.params


    def OnClose(self, event):
        self.Close()

    def varSelect(self, event):
        self.params["variant"] = event.GetSelection()

    def ageSelect(self, event):
        self.params["age"] = self.ages[event.GetSelection()]

    def seasonSelect(self, event):
        self.params["season"] = self.seasons[event.GetSelection()]

    def returnSelections(self, var, age, season):
        params = {"variant": var, "age": age, "season": season}
        return params

class selectorApp(wx.App):
    def OnInit(self):
        dlg = SelectPlantVariant(None, -1, 'Laubwerk Plant Selector')
        dlg.ShowModal()
        print dlg.params
        dlg.Destroy
        return True

if __name__ == "__main__":
    app = None
    del app
    app = wx.App()
    frame = selectorApp()
    app.MainLoop()