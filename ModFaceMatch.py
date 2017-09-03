import wx
import locale
import shutil
import os
import FaceRecognitionInterface

class GUIFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = u"ModFaceMatch", pos = wx.DefaultPosition, size = wx.Size( 1366,768 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)

        self.notebook = wx.Notebook(self)

        mainPanel = MainPanel(self.notebook)
        self.notebook.AddPage(mainPanel, "Main Screen")

        matchFacePanel = MatchFacePanel(self.notebook) 
        self.notebook.AddPage(matchFacePanel, "Match Face")

        addFacePanel = AddFacePanel(self.notebook) 
        self.notebook.AddPage(addFacePanel, "Add Face")

        viewReferencePanel = ViewReferencePanel(self.notebook) 
        self.notebook.AddPage(viewReferencePanel, "View Face Reference Image")

    def MainScreenButtonClicked(self, event):
        self.notebook.ChangeSelection(0)

    def MatchFaceButtonClicked(self, event):
        self.notebook.ChangeSelection(1)

    def AddFaceButtonClicked(self, event):
        self.notebook.ChangeSelection(2)

    def ViewReferenceButtonClicked(self, event):
        self.notebook.ChangeSelection(3)

    def RenderImagePreview(self, path):
        imageBorderSize = int(round(0.62685185185 * wx.GetDisplaySize().GetHeight()))

        img = wx.Image(path, wx.BITMAP_TYPE_ANY)

        dimensions = [img.GetWidth(), img.GetHeight()]
        newdimensions = [0, 0]

        if dimensions[0] > dimensions[1]:
            newdimensions[0] = imageBorderSize
            newdimensions[1] = imageBorderSize * dimensions[1] / dimensions[0]
        else:
            newdimensions[1] = imageBorderSize
            newdimensions[0] = imageBorderSize * dimensions[0] / dimensions[1]

        img = img.Scale(newdimensions[0], newdimensions[1])

        return img

    def RemoveIllegalCharacters(self, text):
        illegalcharacters = ["<", ">", ":", '"', "'", "/", "\\", "|", "?", "*"]

        for i in illegalcharacters:
            text = text.replace(i, "")

        return text

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)

        self.SetBackgroundColour((237, 239, 242))

        #sizing
        sizer = wx.GridSizer(2, 3, 450, 0)

        sizer.AddSpacer(0)

        #background image, remove
        self.backgroundimage = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap( u"ModFaceMatchIntroScreenLowRes.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.backgroundimage, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

        sizer.AddSpacer(0)

        self.matchfacebutton = wx.Button(self, wx.ID_ANY, u"Match Face", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.matchfacebutton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.addfacebutton = wx.Button(self, wx.ID_ANY, u"Add Face", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.addfacebutton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.viewreferencebutton = wx.Button(self, wx.ID_ANY, u"View Reference", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.viewreferencebutton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        self.SetSizer(sizer)
        self.Layout()
        	
        self.Centre(wx.BOTH)
        
        #Button binding
        self.matchfacebutton.Bind(wx.EVT_BUTTON, self.MatchFaceButtonClicked)
        self.addfacebutton.Bind(wx.EVT_BUTTON, self.AddFaceButtonClicked)
        self.viewreferencebutton.Bind(wx.EVT_BUTTON, self.ViewReferenceButtonClicked)

    def MatchFaceButtonClicked(self, event):
        window.MatchFaceButtonClicked(event)

    def AddFaceButtonClicked(self, event):
        window.AddFaceButtonClicked(event)

    def ViewReferenceButtonClicked(self, event):
        window.ViewReferenceButtonClicked(event)

class MatchFacePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)

        self.SetBackgroundColour((237, 239, 242))

        sizer = wx.GridSizer(2, 2, 475, 0)

        #background image, remove
        self.imagepreview = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.imagepreview, 0, wx.ALL, 5)

        self.textbox = wx.TextCtrl(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.textbox, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.imagepicker = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select an image", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        sizer.Add(self.imagepicker, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.mainscreenbutton = wx.Button(self, wx.ID_ANY, u"Main Screen", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.mainscreenbutton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        self.SetSizer(sizer)
        self.Layout()
        	
        self.Centre(wx.BOTH)
        
        #Button binding
        self.imagepicker.Bind(wx.EVT_FILEPICKER_CHANGED, self.ImageSelected)
        self.mainscreenbutton.Bind(wx.EVT_BUTTON, self.MainScreenButtonClicked)

    def MainScreenButtonClicked(self, event):
        window.MainScreenButtonClicked(event)

    def ImageSelected(self, event):
        self.imagepreview.SetBitmap(wx.Bitmap(window.RenderImagePreview(event.GetPath()), wx.BITMAP_SCREEN_DEPTH))
        self.textbox.SetValue(FaceRecognitionInterface.GetMainMatch(self, event))

class AddFacePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)

        self.imagePath = ""

        self.SetBackgroundColour((237, 239, 242))

        sizer = wx.GridSizer(2, 3, 475, 0)

        self.imagepreview = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.imagepreview, 0, wx.ALL, 5)

        self.textbox = wx.TextCtrl(self, wx.ID_ANY, u"Type name here", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.textbox, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.successtext = wx.TextCtrl(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.successtext, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.imagepicker = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select an image", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        sizer.Add(self.imagepicker, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.submitbutton = wx.Button(self, wx.ID_ANY, u"Add face to library", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.submitbutton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.mainscreenbutton = wx.Button(self, wx.ID_ANY, u"Main Screen", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.mainscreenbutton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        self.SetSizer(sizer)
        self.Layout()
        	
        self.Centre(wx.BOTH)
        
        #Button binding
        self.imagepicker.Bind(wx.EVT_FILEPICKER_CHANGED, self.ImageSelected)
        self.mainscreenbutton.Bind(wx.EVT_BUTTON, self.MainScreenButtonClicked)
        self.submitbutton.Bind(wx.EVT_BUTTON, self.SubmitButtonClicked)

    def MainScreenButtonClicked(self, event):
        window.MainScreenButtonClicked(event)

    def ImageSelected(self, event):
        self.imagepreview.SetBitmap(wx.Bitmap(window.RenderImagePreview(event.GetPath()), wx.BITMAP_SCREEN_DEPTH))

        self.imagePath = event.GetPath()

    def SubmitButtonClicked(self, event):
        self.successtext.SetValue("")
        
        if self.imagePath != "":
            print("textbox = " + self.textbox.GetValue())
            
            if self.textbox.GetValue() != "" and self.textbox.GetValue() != "Type name here":
                text = window.RemoveIllegalCharacters(self.textbox.GetValue())
                
                print(self.imagePath)
                
                print("DEBUG file path button clicked ", os.path.join("KnownLibrary", (text + os.path.splitext(self.imagePath)[1])))
                
                shutil.copy2(self.imagePath, os.path.join("KnownLibrary", (text + os.path.splitext(self.imagePath)[1])))

                if os.path.isfile(os.path.join("KnownLibrary", (text + os.path.splitext(self.imagePath)[1]))):
                    self.successtext.SetValue("Add face success!")
                else:
                    self.successtext.SetValue("Add face failed.")

class ViewReferencePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)

        self.SetBackgroundColour((237, 239, 242))

        sizer = wx.GridSizer(2, 2, 475, 0)

        #background image, remove
        self.textbox = wx.TextCtrl(self, wx.ID_ANY, u"Type name here", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.textbox, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.imagepreview = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.imagepreview, 0, wx.ALL, 5)

        self.viewbutton = wx.Button(self, wx.ID_ANY, u"View reference photo for face", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.viewbutton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.mainscreenbutton = wx.Button(self, wx.ID_ANY, u"Main Screen", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.mainscreenbutton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        self.SetSizer(sizer)
        self.Layout()
        	
        self.Centre(wx.BOTH)
        
        #Button binding
        self.mainscreenbutton.Bind(wx.EVT_BUTTON, self.MainScreenButtonClicked)
        self.viewbutton.Bind(wx.EVT_BUTTON, self.ViewButtonClicked)

    def MainScreenButtonClicked(self, event):
        window.MainScreenButtonClicked(event)

    def ViewButtonClicked(self, event):
        if self.textbox.GetValue() != "" and self.textbox.GetValue() != "Type name here":
            text = window.RemoveIllegalCharacters(self.textbox.GetValue())
            
            formats = [".jpg", ".jpeg", ".png"]

            foundflag = 0
            
            for i in formats:
                if os.path.isfile(os.path.join("KnownLibrary", (text + i))):
                    path = os.path.join("KnownLibrary", (text + i))
                    
                    self.imagepreview.SetBitmap(wx.Bitmap(window.RenderImagePreview(path), wx.BITMAP_SCREEN_DEPTH))

                    foundflag = 1
            if foundflag < 1:
                    self.imagepreview.SetBitmap(wx.Bitmap(window.RenderImagePreview(os.path.join("KnownLibrary", "nofile.jpg")), wx.BITMAP_SCREEN_DEPTH))
        
app = wx.App()
window = GUIFrame(None)
window.Show(True)

print("DEBUG:", wx.GetDisplaySize().GetWidth(), wx.GetDisplaySize().GetHeight())

window.SetSize(wx.GetDisplaySize().GetWidth(), wx.GetDisplaySize().GetHeight())
window.Centre()

app.MainLoop()
