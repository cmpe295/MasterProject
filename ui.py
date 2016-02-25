#!/usr/local/bin/python2.7
import wx
from Gen import Gen

class Menu(wx.Frame):

    def __init__(self, parent, title):
        super(Menu, self).__init__(parent, title=title, size=(400, 400))

        self.InitUI()
        self.Centre()
        self.Show()
        self.nameVar = ''
        self.ioIntensiveVar = ''
        self.startAddressVar = ''
        self.endAddressVar = ''
        self.ioCountVar = ''
        self. writePercentageVar = ''
        self.randomWritePercentageVar = ''
        self.randomReadPercentageVar = ''
        self.result = ''

    def InitUI(self):

        panel = wx.Panel(self)

        sizer = wx.GridBagSizer(5, 5)
        """
        draw a line
        """
        # line = wx.StaticLine(panel)
        # sizer.Add(line, pos=(1, 0), span=(1, 5),
        #     flag=wx.EXPAND|wx.BOTTOM, border=10)

        text1 = wx.StaticText(panel, label="Name")
        sizer.Add(text1, pos=(1, 0), flag=wx.LEFT, border=10)

        self.tc1 = wx.TextCtrl(panel)
        sizer.Add(self.tc1, pos=(1, 1), span=(1, 2), flag=wx.TOP)
        self.Bind(wx.EVT_TEXT, self.setName, self.tc1)


        text2 = wx.StaticText(panel, label="IO Intensive")
        sizer.Add(text2, pos=(2, 0), flag=wx.TOP|wx.LEFT, border=10)

        self.intensiveSelection = ""
        intensiveList = ["", "High", "Medium", "Low"]
        self.combo = wx.ComboBox(panel, choices=intensiveList)
        self.combo.Bind(wx.EVT_COMBOBOX, self.ioIntensive)

        sizer.Add(self.combo, pos=(2, 1), span=(1, 2), flag=wx.TOP, border=5)

        text3 = wx.StaticText(panel, label="Address Range")
        sizer.Add(text3, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)

        self.tc2 = wx.TextCtrl(panel)
        self.tc2.SetHint('Start Address')
        sizer.Add(self.tc2, pos=(3, 1), span=(1, 1), flag=wx.TOP, border=5)
        self.Bind(wx.EVT_TEXT, self.startAddress, self.tc2)

        self.tc3 = wx.TextCtrl(panel)
        self.tc3.SetHint('End Address')
        sizer.Add(self.tc3, pos=(3, 2), span=(0, 1), flag=wx.TOP, border=5)
        self.Bind(wx.EVT_TEXT, self.endAddress, self.tc3)

        text4 = wx.StaticText(panel, label="IO Count")
        sizer.Add(text4, pos=(4, 0), flag=wx.LEFT|wx.TOP, border=10)
        self.tc4 = wx.TextCtrl(panel)
        sizer.Add(self.tc4, pos=(4, 1), span=(1, 1), flag=wx.TOP, border=5)
        self.Bind(wx.EVT_TEXT, self.ioCount, self.tc4)

        text5 = wx.StaticText(panel, label="Write Percentage")
        sizer.Add(text5, pos=(5, 0), flag=wx.LEFT|wx.TOP, border=10)
        self.tc5 = wx.TextCtrl(panel)
        sizer.Add(self.tc5, pos=(5, 1), span=(1, 1), flag=wx.TOP, border=5)
        self.Bind(wx.EVT_TEXT, self.writePercentage, self.tc5)

        text6 = wx.StaticText(panel, label="Random Write Percentage")
        sizer.Add(text6, pos=(6, 0), flag=wx.LEFT|wx.TOP, border=10)
        self.tc6 = wx.TextCtrl(panel)
        sizer.Add(self.tc6, pos=(6, 1), span=(1, 1), flag=wx.TOP, border=5)
        self.Bind(wx.EVT_TEXT, self.randomWritePercentage, self.tc6)

        text7 = wx.StaticText(panel, label="Random Read Percentage")
        sizer.Add(text7, pos=(7, 0), flag=wx.LEFT|wx.TOP, border=10)
        self.tc7 = wx.TextCtrl(panel)
        sizer.Add(self.tc7, pos=(7, 1), span=(1, 1), flag=wx.TOP, border=5)
        self.Bind(wx.EVT_TEXT, self.randomReadPercentage, self.tc7)


        button4 = wx.Button(panel, label="Ok")
        sizer.Add(button4, pos=(10, 1))
        button4.Bind(wx.EVT_BUTTON, self.onClose)
        
        button5 = wx.Button(panel, label="Clear")
        sizer.Add(button5, pos=(10, 0), span=(1, 1), flag=wx.BOTTOM|wx.CENTER, border=5)

        sizer.AddGrowableCol(2)

        panel.SetSizer(sizer)

    def setName(self, event):
        self.nameVar = self.tc1.GetValue()
        return self.nameVar

    def ioIntensive(self, event):
        self.ioIntensiveVar = self.combo.GetValue()
        return self.ioIntensiveVar

    def startAddress(self, event):
        self.startAddressVar = self.tc2.GetValue()
        return self.startAddressVar

    def endAddress(self, event):
        self.endAddressVar = self.tc3.GetValue()
        return self.endAddressVar

    def ioCount(self, event):
        self.ioCountVar = self.tc4.GetValue()
        return self.ioCountVar

    def writePercentage(self, event):
        self.writePercentageVar = self.tc5.GetValue()
        return self.writePercentageVar

    def randomWritePercentage(self,event):
        self.randomWritePercentageVar = self.tc6.GetValue()
        return self.randomWritePercentageVar

    def randomReadPercentage(self, event):
        self.randomReadPercentageVar = self.tc7.GetValue()
        return self.randomReadPercentageVar

    def onClose(self, event):
        self.result = {'name': self.nameVar, 'io_intensive': self.ioIntensiveVar,
         'range': (int(self.startAddressVar), int(self.endAddressVar)),
         'count': int(self.ioCountVar), 'write_percent': float(self.writePercentageVar),
         'write_ran_percent': float(self.randomWritePercentageVar),
         'read_ran_percent': float(self.randomReadPercentageVar)}
        print(self.result)

        myGen = Gen(self.result)
        myGen.gen()



if __name__ == '__main__':
    app = wx.App()
    Menu(None, title="IO Generator")
    app.MainLoop()
