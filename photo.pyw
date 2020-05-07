#!/usr/bin/python
# coding=utf8

'''
Using wxPython for GUI, already be dropped now.
'''

import os
import wx
from imaging import Imaging
from pyvin.core import Processor
import pyvin.ux
from pyvin.ux import FileDropTarget

class MainWindow(wx.Frame):
    tsize = (20, 20)

    (ID_MENUITEM_OPEN, ID_MENUITEM_SHUTDOWN,
     ID_MENUITEM_START, ID_MENUITEM_STOP, ID_MENUITEM_CLEAN_ALL,
     ID_MENUITEM_REMOVE, ID_MENUITEM_VIEW,
     ID_LIST,
     ID_TOOL_OPEN, ID_TOOL_TOGGLE, ID_TOOL_CLEAN) = range(0, 11)

    COLUMNS = ['#', 'NAME', 'PROGRESS', 'DONE']
    (COLUMN_NUM, COLUMN_NAME, COLUMN_PROGRESS, COLUMN_DONE) = range(0, 4)
    COLUMNS_WIDTH = [50, 350, 100, 50]

    def __init__(self, tt):
        wx.Frame.__init__(self, None, title=tt, size=(600, 400))

        self.POPMENU = [
            ('Remove',  'Remove',   MainWindow.ID_MENUITEM_REMOVE,    '', '', self.menuItemRemove,    MainWindow.ID_LIST),
            ('View',    'View',     MainWindow.ID_MENUITEM_VIEW,      '', '', self.menuItemView,      MainWindow.ID_LIST),
        ]

        self.TOOLBAR = [
            ('Open',            'Open',         MainWindow.ID_TOOL_OPEN,    wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON, MainWindow.tsize), wx.ITEM_NORMAL,  self.menuOpen),
            ('Start / Stop',    'Start / Stop', MainWindow.ID_TOOL_TOGGLE,  wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_BUTTON, MainWindow.tsize),      wx.ITEM_NORMAL,  self.menuStartStop),
            ('Clear All',       'Clear All',    MainWindow.ID_TOOL_CLEAN,   wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_BUTTON, MainWindow.tsize),   wx.ITEM_NORMAL,  self.menuClearAll)
        ]

        self.popupmenu = pyvin.ux.createPopmenu(self, self.POPMENU)
        self.toolbar = pyvin.ux.createToolBar(self, self.TOOLBAR)
        self.statusBar = self.CreateStatusBar()

        panel = wx.Panel(self)
        self.gauge = wx.Gauge(panel, -1, 100, style = wx.GA_PROGRESSBAR)
        self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.LC_VRULES)

        for i in range(len(MainWindow.COLUMNS)):
            self.list.InsertColumn(i, MainWindow.COLUMNS[i], width=MainWindow.COLUMNS_WIDTH[i])

        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED,  self.onItemDbClick)
        self.list.Bind(wx.EVT_CONTEXT_MENU,         self.onItemShowPopup)

        dropTarget = FileDropTarget()
        self.list.SetDropTarget(dropTarget)
        dropTarget.bind(FileDropTarget.EVT_ON_DROP_FILES, self.onDropFiles)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.gauge, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(self.list, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        # vbox.Add(self.teInfo, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

        panel.SetSizer(vbox)

        self.Centre()

        self.listRows = 0
        self.processIdx = 0
        self.img = Imaging()

    def appendItem(self, name, progress='==========', done=''):
        self.list.InsertStringItem(self.listRows, '%d' % (self.listRows+1))
        self.list.SetStringItem(self.listRows, MainWindow.COLUMN_NAME, name)
        self.list.SetStringItem(self.listRows, MainWindow.COLUMN_PROGRESS, progress)
        self.list.SetStringItem(self.listRows, MainWindow.COLUMN_DONE, done)
        self.listRows += 1

        self.list.SetColumnWidth(MainWindow.COLUMN_NUM, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(MainWindow.COLUMN_NAME, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(MainWindow.COLUMN_PROGRESS, wx.LIST_AUTOSIZE)
        # self.list.SetColumnWidth(MainWindow.COLUMN_DONE, wx.LIST_AUTOSIZE)

    def setProgress(self, idx, prog):
        if idx < self.listRows:
            ppp = ''
            prog /= 10
            for i in range(prog):
                ppp += '>'
            for i in range(10 - prog):
                ppp += '='
            self.list.SetStringItem(idx, MainWindow.COLUMN_PROGRESS, ppp)

    def setDone(self, idx, done=True):
        if done:
            self.list.SetStringItem(idx, MainWindow.COLUMN_DONE, ' ^_^ ')
        else:
            self.list.SetStringItem(idx, MainWindow.COLUMN_DONE, '')

    def clearList(self):
        self.list.DeleteAllItems()

    def menuOpen(self, event):
        file_wildcard = "Picture Files (*.jpg;*.jpeg;*.png;*.bmp)|*.jpg;*.jpeg;*.png;*.bmp|All files(*.*)|*.*"
        msg = "Select picture file(s) to compress..."
        ret, files = pyvin.ux.showFileDlg(self, msg, os.getcwd(), file_wildcard, False)
        if ret:
            self.paths = files
            print files
            for i in range(len(self.paths)):
                self.appendItem(self.paths[i])

    def menuStartStop(self, event):
        if True:
            self.process = Processor()
            self.process.bind(Processor.EVT_START, self.onStart)
            self.process.bind(Processor.EVT_LOOP, self.onLoop)
            self.process.bind(Processor.EVT_STOP, self.onStop)
            self.process.start()
        else:
            self.process.stop()

    def menuClearAll(self, event):
        self.clearList()
        self.listRows = 0
        self.processIdx = 0

    def onItemDbClick(self,event):
        idx = self.list.GetFocusedItem()
        name = self.list.GetItemText(idx, MainWindow.COLUMN_NAME)
        pyvin.ux.openInNewTab(name)

    def onItemShowPopup(self, event):
        if self.list.GetFirstSelected() != -1:
            pos = event.GetPosition()
            pos = self.list.ScreenToClient(pos)
            self.list.PopupMenu(self.popupmenu, pos)
        else:
            print 'no item selected'

    def menuItemRemove(self, event):
        print 'menuItemRemove'
        idx = self.list.GetFocusedItem()
        self.list.DeleteItem(idx)

    def menuItemView(self, event):
        print 'menuItemView'
        idx = self.list.GetFirstSelected()
        if idx != -1:
            url = self.list.GetItemText(idx, MainWindow.COLUMN_NAME)
            pyvin.ux.openInNewTab(url)

    def onDropFiles(self, event, files):
        for f in files:
            self.appendItem(f)

    def onStart(self, event):
        print 'onStart'
        self.processIdx = 0
        self.gauge.SetValue(0);
        return True

    def onLoop(self, event):
        print 'onLoop'
        if self.processIdx < self.listRows:
            name = self.list.GetItemText(self.processIdx, MainWindow.COLUMN_NAME)

            self.img.resize(name)

            self.setProgress(self.processIdx, 100)
            self.setDone(self.processIdx, True)
            self.processIdx += 1
            self.gauge.SetValue(self.processIdx * 100 / self.listRows);
            return True
        else:
            return False

    def onStop(self, event):
        print 'onStop'
        self.gauge.SetValue(100);
        pyvin.ux.showMsg(self, 'Finish', 'Compress Picture')
        return True

if __name__ == '__main__':
    app = wx.App(0)
    win = MainWindow('Picture Compressor')
    win.Show(True)
    app.MainLoop()