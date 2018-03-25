# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 12:13:07 2018

@author: proc1
"""

#!/usr/bin/python
# -*- coding: UTF-8 -*-

#!/usr/bin/env python
import wx
 
app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "Hello World") # A Frame is a top-level window.
frame.Show(True)     # Show the frame.
app.MainLoop()