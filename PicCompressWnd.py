#!/usr/bin/python
# coding=utf8

__author__ = 'vin@misday.com'

import os, wx, wx.grid
import  vinux

class MainWindow(wx.Frame):
    tsize = (20, 20)

    BG_FREED = wx.Colour(255, 255, 153)
    BG_DOWN = wx.Colour(146, 208, 80)

    (ID_MENUITEM_OPEN, ID_MENUITEM_SHUTDOWN,
     ID_MENUITEM_START, ID_MENUITEM_STOP, ID_MENUITEM_CLEAN_ALL,
     ID_MENUITEM_REMOVE, ID_MENUITEM_VIEW,
     ID_LIST,
     ID_TOOL_OPEN, ID_TOOL_TOGGLE, ID_TOOL_CLEAN) = range(0, 11)

    COLUMNS = ['PICTURE', 'PROGRESS', 'RESULT']

    (COLUMN_TITLE, COLUMN_PROGRESS, COLUMN_RESULT) = range(0, 3)
    COLUMNS_WIDTH = [50, 200, 200, 200, 200, 100]

    def __init__(self, tt):

        self.MENUBAR = [('&File', (
                                ('&Open',                 '', MainWindow.ID_MENUITEM_OPEN,           self.menuOpen),
                                ("", '', '', ""),
                                ('Shutdown after finish', '', MainWindow.ID_MENUITEM_SHUTDOWN,       self.menuShutdown, wx.ITEM_CHECK),
                        )),
                        ('&Edit', (('Start',        '', MainWindow.ID_MENUITEM_START,     self.menuStartStop),
                                   ('Stop',         '', MainWindow.ID_MENUITEM_STOP,      self.menuStartStop),
                                   ("", "", '', ""),
                                   ('Clear All',    '', MainWindow.ID_MENUITEM_CLEAN_ALL, self.menuClearAll),
                        ))
               ]

        self.POPMENU = [
            (MainWindow.ID_MENUITEM_VIEW,   'View',     self.menuItemView,      MainWindow.ID_LIST),
            (MainWindow.ID_MENUITEM_REMOVE, 'Remove',   self.menuItemRemove,    MainWindow.ID_LIST),
        ]

        self.TOOLBAR = [
            (MainWindow.ID_TOOL_OPEN,   'Open',          wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON, MainWindow.tsize),   self.menuOpen),
            (MainWindow.ID_TOOL_TOGGLE, 'Start / Stop',  wx.ArtProvider.GetBitmap(wx.ART_FIND, wx.ART_BUTTON, MainWindow.tsize),        self.menuStartStop),
            (MainWindow.ID_TOOL_CLEAN,  'Clear All',     wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_BUTTON, MainWindow.tsize),     self.menuClearAll)
        ]

        wx.Frame.__init__(self, None, title=tt, size=(1020, 800))

        self.menubar = vinux.createMenubar(self, self.MENUBAR) #self.createMenubar(self.MENUBAR)
        self.toolbar = vinux.createToolBar(self, self.TOOLBAR)
        self.statusBar = self.CreateStatusBar()
        vinux.createPopmenu(self, self.POPMENU)

        #panel######################################
        panel = wx.Panel(self)

        self.gauge = wx.Gauge(panel, -1, 100, style = wx.GA_PROGRESSBAR)
        # self.list = wx.ListCtrl(panel, MainWindow.ID_LIST, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.LC_VRULES)
        self.list = wx.grid.Grid(panel)
        table = VinTable(MainWindow.COLUMNS)
        self.list.SetTable(table, True)
        dropTarget = FileDropTarget(table, self.list)
        self.list.SetDropTarget(dropTarget)
        # self.list.ForceRefresh()
        # self.teInfo = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.HSCROLL)

        # for i in range(len(MainWindow.COLUMNS)):
        #     self.list.InsertColumn(i, MainWindow.COLUMNS[i], width=MainWindow.COLUMNS_WIDTH[i])

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.gauge, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(self.list, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        # vbox.Add(self.teInfo, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

        panel.SetSizer(vbox)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,   self.menuItemView,    id=MainWindow.ID_LIST)
        self.Bind(wx.EVT_CONTEXT_MENU,          self.onShowPopup,       id=MainWindow.ID_LIST)

        self.downloadIdx = 0

        # self.redir = RedirectText(self)
        # sys.stdout = self.redir

        self.Centre()


    def menuOpen(self, event):
        # print 'open'
        ret, file = vinux.showFileDlg(self, 'select picture to compress', wildcard = "Picture Files(*.jpg;*.jpeg;*.png;*.bmp)|*.jpg;*.jpeg;*.png;*.bmp", single = False)
        if ret:
            vinux.showMsg(self, file)

    def menuStartStop(self, event):
        vinux.showMsg(self, 'start/stop')

    def menuClearAll(self, event):
        vinux.showMsg(self, 'clear all')

    def menuShutdown(self, event):
        print self.menubar.IsChecked(MainWindow.ID_MENUITEM_SHUTDOWN)

    def menuItemView(self, event):
        pass

    def menuItemRemove(self, event):
        pass

    def appendItem(self, id, title='', author='', link='', freed=False, done=False, progress='=========='):
        newIdx = self.list.GetItemCount()
        self.list.InsertStringItem(newIdx, '%d' % (newIdx + 1))
        self.list.SetStringItem(newIdx, MainWindow.COLUMN_ID, id)
        self.list.SetStringItem(newIdx, MainWindow.COLUMN_TITLE, title)
        self.list.SetStringItem(newIdx, MainWindow.COLUMN_AUTHOR, author)
        self.list.SetStringItem(newIdx, MainWindow.COLUMN_LINK, link)
        self.list.SetStringItem(newIdx, MainWindow.COLUMN_PROGRESS, progress)

        if freed:
            self.list.SetItemBackgroundColour(newIdx, MainWindow.BG_FREED)
        if done:
            self.list.SetItemBackgroundColour(newIdx, MainWindow.BG_DOWN)

        self.adjustListWidth()

    def adjustListWidth(self):
        self.list.SetColumnWidth(MainWindow.COLUMN_NUM, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(MainWindow.COLUMN_ID, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(MainWindow.COLUMN_TITLE, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(MainWindow.COLUMN_AUTHOR, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(MainWindow.COLUMN_LINK, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(MainWindow.COLUMN_PROGRESS, wx.LIST_AUTOSIZE)

    # set download column progress
    def setProgress(self, idx, prog):
        if idx < self.list.GetItemCount():
            ppp = ''
            prog /= 10
            for i in range(prog):
                ppp += '>'
            for i in range(10 - prog):
                ppp += '='
            self.list.SetStringItem(idx, MainWindow.COLUMN_PROGRESS, ppp)

    def setUrl(self, url):
        self.teUrl.SetValue(url)

    def addLog(self, log):
        self.teInfo.AppendText(log)
        pass

    def onUpdate(self, event):
        self.gauge.SetValue(10)
        # proxy = self.conf.getProxy()
        # special = Special(proxy[0], proxy[1], proxy[2])
        # special.bind(Special.EVT_FIND_LINK, self.cbAddUrl)
        # special.bind(Special.EVT_FIND_BOOK, self.cbAddBook)
        # special.start()
        self.gauge.SetValue(100)

    # download a book
    def onDownloadItem(self,event):
        idx = self.list.GetFocusedItem()
        id = self.list.GetItemText(idx, MainWindow.COLUMN_ID)
        title = self.list.GetItemText(idx, MainWindow.COLUMN_TITLE)
        # win = DownloaderWnd(self.conf, title)
        # win.setId(id)
        # win.setName(id)
        # win.Show(True)

    # show popup menu
    def onShowPopup(self, event):
        if self.list.GetFirstSelected() != -1:
            pos = event.GetPosition()
            pos = self.list.ScreenToClient(pos)
            self.list.PopupMenu(self.popupmenu, pos)

    # open link in browser
    def onBrowserItem(self, event):
        idx = self.list.GetFirstSelected()
        if idx != -1:
            url = self.list.GetItemText(idx, MainWindow.COLUMN_LINK)
            # self.duokan.openInNewTab(url)

    # rename a item from id to title
    def onRenameItem(self, event):
        idx = self.list.GetFirstSelected()
        if idx != -1:
            id = self.list.GetItemText(idx, MainWindow.COLUMN_ID)
            title = self.list.GetItemText(idx, MainWindow.COLUMN_TITLE)
            # self.duokan.rename(id, title)

    # delete an item
    def onRemoveItem(self, event):
        idx = self.list.GetFirstSelected()
        if idx != -1:
            self.list.DeleteItem(idx)

    def onCropItem(self, event):
        idx = self.list.GetFirstSelected()
        if idx != -1:
            id = self.list.GetItemText(idx, MainWindow.COLUMN_ID)
            # self.duokan.crop(id)

    def onMergeItem(self, event):
        idx = self.list.GetFirstSelected()
        if idx != -1:
            id = self.list.GetItemText(idx, MainWindow.COLUMN_ID)
            # self.duokan.merge(id)

    def startDownload(self):
        if self.downloadIdx < self.list.GetItemCount():
            id = self.list.GetItemText(self.downloadIdx, MainWindow.COLUMN_ID)
            # proxy = self.conf.getProxy()
            # self.down = Downloader(id, id, proxy[0], proxy[1], proxy[2])
            # self.down.bind(Downloader.EVT_START, self.cbStart)
            # self.down.bind(Downloader.EVT_STOP, self.cbStop)
            # self.down.bind(Downloader.EVT_LOG, self.cbLog)
            # self.down.bind(Downloader.EVT_PROG, self.cbProgress)
            # self.down.start()

    # for downloader
    def cbStart(self, event):
        wx.CallAfter(self.setProgress, self.downloadIdx, 0)

    # for downloader
    def cbStop(self, event):
        wx.CallAfter(self.setProgress, self.downloadIdx, 100)
        wx.CallAfter(self.gauge.SetValue, 100)
        self.list.SetItemBackgroundColour(self.downloadIdx, MainWindow.BG_DOWN)

        # start next
        self.downloadIdx += 1
        self.startDownload()

        if self.downloadIdx >= self.list.GetItemCount():
            if self.menubar.IsChecked(MainWindow.ID_MENUITEM_SHUTDOWN):
                os.system('shutdown -t 60 -f -s')

    # for downloader
    def cbLog(self, event, str):
        wx.CallAfter(self.addLog, str)
        print str

    # for downloader
    def cbProgress(self, event, prog):
        # itemCount = self.list.GetItemCount()
        # wx.CallAfter(self.setProgress, self.downloadIdx, prog)
        wx.CallAfter(self.gauge.SetValue, prog)



class FileDropTarget(wx.FileDropTarget):
    def __init__(self, adapter, window):
          wx.FileDropTarget.__init__(self)
          self.adapter = adapter
          self.window = window

    def OnDropFiles(self,  x,  y, fileNames):
        print fileNames
        numRows = len(fileNames)
        for fileName in fileNames:
            self.adapter.AppendItem(fileName)
        wx.CallAfter(self.window.ForceRefresh)
        # self.window.ForceRefresh()

class VinTable(wx.grid.PyGridTableBase):
    def __init__(self, colLabel):
        wx.grid.PyGridTableBase.__init__(self)
        self.colLabel = colLabel
        self.data = {}

        self.odd=wx.grid.GridCellAttr()
        self.odd.SetBackgroundColour("white")
        self.odd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.even=wx.grid.GridCellAttr()
        self.even.SetBackgroundColour("light blue")
        self.even.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

    # these five are the required methods
    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.colLabel)

    def IsEmptyCell(self, row, col):
        return self.data.get((row, col)) is not None

    def GetValue(self, row, col): #为网格提供数据
        value = self.data.get((row, col))
        if value is not None:
            return value
        else:
            return ''

    def SetValue(self, row, col, value):#给表赋值
        self.data[(row,col)] = value

    def GetRowLabelValue(self, row):
        '''return the label of the row'''
        return (row + 1)

    def GetColLabelValue(self, col):
        '''return the lable of the column'''
        return self.colLabel[col]

    # the table can also provide the attribute for each cell
    def GetAttr(self, row, col, kind):
        attr = [self.even, self.odd][row % 2]
        attr.IncRef()
        # if col == 0:
        #     # renderer = wx.grid.GridCellBoolRenderer
        #     attr.SetRenderer(wx.grid.GridCellBoolRenderer())
        return attr

    def AppendItem(self, value):
        self.data[(len(self.data), 0)] = value

        gridView = self.GetView()
        gridView.BeginBatch()
        appendMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
        gridView.ProcessTableMessage(appendMsg)
        gridView.EndBatch()

        # print len(self.data)
        return True

    def DeleteItem(self, pos=0, numRows=1):
        if self.data is None or len(self.data) == 0:
            return False

        for rowNum in range(0,numRows):
            self.data.remove(self.data[pos+rowNum])

        gridView = self.GetView()
        gridView.BeginBatch()
        deleteMsg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,pos,numRows)
        gridView.ProcessTableMessage(deleteMsg)
        gridView.EndBatch()

if __name__ == '__main__':
    app = wx.App(0)
    win = MainWindow('Pic Compressor')
    win.Show(True)
    app.MainLoop()