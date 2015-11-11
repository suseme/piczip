__author__ = 'vin@misday'

import wx, webbrowser

def createMenubar(wnd, menuDef):
    '''menuDef = [('FILE', (
                            ('Open', 'Open a file', MainWindow.ID_MENUITEM_OPEN, self.menuOpen),
                            )
                  )]'''
    menuBar = wx.MenuBar()
    for eachMenu in menuDef:
        label = eachMenu[0]
        items = eachMenu[1]
        menuBar.Append(createMenuItems(wnd, items), label)
    wnd.SetMenuBar(menuBar)
    return menuBar

def createMenuItems(wnd, menuData):
    menu = wx.Menu()
    for item in menuData:
        if len(item) == 2:
            label = item[0]
            subMenu = wnd.createMenuItems(item[1])
            menu.AppendMenu(wx.ID_ANY, label, subMenu)
        else:
            label = item[0]
            help = item[1]
            id = item[2]
            handler = item[3]
            if len(item) > 4:
                kind = item[4]
            else:
                kind = wx.ITEM_NORMAL

            if label:
                menu.Append(id, label, help, kind=kind)
                wnd.Bind(wx.EVT_MENU, handler, id=id)
            else:
                menu.AppendSeparator()
    return menu

def createPopmenu(wnd, popmenuDef):
    wnd.popupmenu = wx.Menu()
    for item in popmenuDef:
        wnd.popupmenu.Append(item[0],   item[1])
        wnd.Bind(wx.EVT_MENU, item[2], id=item[0],     id2=item[3])
    return wnd.popupmenu

def createToolBar(wnd, toolbarDef):
    '''self.TOOLBAR = [
        (MainWindow.ID_TOOL_FETCH, 'Fetch', wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_BUTTON, MainWindow.tsize), self.onUpdate),
        '''
    toolbar = wnd.CreateToolBar()
    for item in toolbarDef:
        toolbar.AddLabelTool(item[0], item[1], item[2])
        wnd.Bind(wx.EVT_TOOL, item[3], id=item[0])
    toolbar.Realize()
    return toolbar

def showDirDlg(wnd, msg = '', path = ''):
    ret = True
    filePath = ''
    dlg = wx.DirDialog(wnd,
                        msg,
                        path,
                        style = wx.OPEN,
                        )
    if dlg.ShowModal() == wx.ID_OK:
        filePath = dlg.GetPath()
    else:
        ret = False
    dlg.Destroy()
    return (ret, filePath)

def showFileDlg(wnd, msg = '', path = '', wildcard = "All Files(*.*)|*.*", single = True):
    if single:
        style = wx.OPEN
    else:
        style = wx.MULTIPLE

    ret = True
    filePath = ''
    dlg = wx.FileDialog(wnd,
                        msg,
                        path,
                        style = style,
                        wildcard = wildcard
                        )
    if dlg.ShowModal() == wx.ID_OK:
        filePath = dlg.GetPath()
    else:
        ret = False
    dlg.Destroy()
    return (ret, filePath)

def showMsg(wnd, msg = '', title = ''):
    dlg = wx.MessageDialog(wnd, msg, title, wx.OK)
    dlg.ShowModal()
    dlg.Destroy()
    return True

def openInNewTab(url):
        '''open in browser with new tab'''
        if len(url) > 0:
            webbrowser.open(url, new=2, autoraise=True)
        else:
            print('url is empty')
