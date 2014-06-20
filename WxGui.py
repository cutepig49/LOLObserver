# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.html

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"LOL Observer", pos = wx.DefaultPosition, size = wx.Size( 706,614 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook2 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel9 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.home_browser = wx.html.HtmlWindow( self.m_panel9, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO )
		bSizer3.Add( self.home_browser, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel9.SetSizer( bSizer3 )
		self.m_panel9.Layout()
		bSizer3.Fit( self.m_panel9 )
		self.m_notebook2.AddPage( self.m_panel9, u"首页", True )
		self.game_panel = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.game_listbook = wx.Listbook( self.game_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LB_DEFAULT )
		
		bSizer4.Add( self.game_listbook, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.button_play = wx.Button( self.game_panel, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.button_play.Hide()
		
		bSizer4.Add( self.button_play, 0, wx.ALL, 5 )
		
		
		self.game_panel.SetSizer( bSizer4 )
		self.game_panel.Layout()
		bSizer4.Fit( self.game_panel )
		self.m_notebook2.AddPage( self.game_panel, u"我的录像", False )
		self.download_panel = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.download_listbook = wx.Listbook( self.download_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LB_DEFAULT )
		
		bSizer5.Add( self.download_listbook, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.download_panel.SetSizer( bSizer5 )
		self.download_panel.Layout()
		bSizer5.Fit( self.download_panel )
		self.m_notebook2.AddPage( self.download_panel, u"下载列表", False )
		self.m_panel13 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.help_browser = wx.html.HtmlWindow( self.m_panel13, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO )
		bSizer12.Add( self.help_browser, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel13.SetSizer( bSizer12 )
		self.m_panel13.Layout()
		bSizer12.Fit( self.m_panel13 )
		self.m_notebook2.AddPage( self.m_panel13, u"帮助", False )
		self.m_panel12 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText5 = wx.StaticText( self.m_panel12, wx.ID_ANY, u"League of Legends 路径：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer8.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txt_client_path = wx.TextCtrl( self.m_panel12, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer9.Add( self.txt_client_path, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.button_choose_client = wx.Button( self.m_panel12, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.button_choose_client, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer8.Add( bSizer9, 0, wx.EXPAND, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel12, wx.ID_ANY, u"录像文件目录：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		bSizer8.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txt_lob_path = wx.TextCtrl( self.m_panel12, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer10.Add( self.txt_lob_path, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.button_choose_record_dir = wx.Button( self.m_panel12, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.button_choose_record_dir, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer8.Add( bSizer10, 0, wx.EXPAND, 5 )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_checkBox1 = wx.CheckBox( self.m_panel12, wx.ID_ANY, u"观战时自动录像", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox1.SetValue(True) 
		self.m_checkBox1.Enable( False )
		
		gSizer1.Add( self.m_checkBox1, 0, wx.ALL, 5 )
		
		self.m_checkBox2 = wx.CheckBox( self.m_panel12, wx.ID_ANY, u"开机启动", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox2.Enable( False )
		
		gSizer1.Add( self.m_checkBox2, 0, wx.ALL, 5 )
		
		
		bSizer8.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_apply = wx.Button( self.m_panel12, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.button_apply, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )
		
		
		bSizer11.AddSpacer( ( 0, 0), 1, 0, 5 )
		
		self.button_cancel = wx.Button( self.m_panel12, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.button_cancel, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )
		
		
		bSizer8.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		
		self.m_panel12.SetSizer( bSizer8 )
		self.m_panel12.Layout()
		bSizer8.Fit( self.m_panel12 )
		self.m_notebook2.AddPage( self.m_panel12, u"设置", False )
		
		bSizer2.Add( self.m_notebook2, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		self.download_timer = wx.Timer()
		self.download_timer.SetOwner( self, wx.ID_ANY )
		self.download_timer.Start( 1000 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.MainFrameOnClose )
		self.m_notebook2.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.m_notebook2OnNotebookPageChanged )
		self.button_play.Bind( wx.EVT_BUTTON, self.button_playOnButtonClick )
		self.button_choose_client.Bind( wx.EVT_BUTTON, self.button_choose_clientOnButtonClick )
		self.button_choose_record_dir.Bind( wx.EVT_BUTTON, self.button_choose_record_dirOnButtonClick )
		self.button_apply.Bind( wx.EVT_BUTTON, self.button_applyOnButtonClick )
		self.button_cancel.Bind( wx.EVT_BUTTON, self.button_cancelOnButtonClick )
		self.Bind( wx.EVT_TIMER, self.download_timerOnTimer, id=wx.ID_ANY )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def MainFrameOnClose( self, event ):
		event.Skip()
	
	def m_notebook2OnNotebookPageChanged( self, event ):
		event.Skip()
	
	def button_playOnButtonClick( self, event ):
		event.Skip()
	
	def button_choose_clientOnButtonClick( self, event ):
		event.Skip()
	
	def button_choose_record_dirOnButtonClick( self, event ):
		event.Skip()
	
	def button_applyOnButtonClick( self, event ):
		event.Skip()
	
	def button_cancelOnButtonClick( self, event ):
		event.Skip()
	
	def download_timerOnTimer( self, event ):
		event.Skip()
	

