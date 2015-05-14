#encoding=utf-8
import wx
import webbrowser
import wx.html as html

user_guide_markdown ="""</div>
    <div id="readme" class="blob instapaper_body">
    <article class="markdown-body entry-content" itemprop="mainContentOfPage"><h3>
<a id="user-content-install-extension-for-mac-dictionary" class="anchor" href="#install-extension-for-mac-dictionary" aria-hidden="true"><span class="octicon octicon-link"></span></a>install extension for Mac dictionary.</h3>

<ul>
<li>For more information on <a href="http://pooriaazimi.github.io/BetterDictionary/">website</a> . It is a perfect extension for Mac dictionary. What I do is based on its work.</li>
</ul>

<h3>
<a id="user-content-setting-path" class="anchor" href="#setting-path" aria-hidden="true"><span class="octicon octicon-link"></span></a>Setting path</h3>

<ul>
<li>remember where you installed the former extension</li>
<li>Please click menubar File-&gt;Setting, enter the right path, where the former extension is installed.</li>
<li>
<p>Check</p>

<ul>
<li>Check to find a everyday_words.txt file, which may be blank at first. But when you add a new word through Mac dictionary or you have edited some words, this file stores your new words and their frequency.</li>
<li>After <code>Setting path</code>, if you don't find everyday_words.txt, you should create it with the same file name and format by yourself.I hope everything would go well. And you need do this.</li>
</ul>
</li>
<li>
<p>About the Boxes before every new word.</p>

<ul>
<li>Check it if you remember this new words today.</li>
<li>I will display these new words in different order, which is depending on the check frequency.</li>
<li>If you want to edit a new word, such as adding a phrase, a comment or a sentence about this word, just feel free to click this word. Please what happens to the right half part. Edit it freely. The software saves your changes automatically.</li>
</ul>
</li>
</ul>
</article>
  </div>
"""
change_times = 1
class HTML_display(wx.Frame):
	"""docstring for HTML_display"""
	def __init__(self, parent, id, title,display_source):
		wx.Frame.__init__(self, parent, id, title,size=(600,400))

		self.display_source = display_source
		panel = wx.Panel(self,-1)
		vbox = wx.BoxSizer(wx.VERTICAL)
		htmlpage = html.HtmlWindow(panel, -1, style=wx.NO_BORDER)
		# I didn't open the links in the html source.
		htmlpage.SetStandardFonts()
		htmlpage.SetPage(self.display_source)

		vbox.Add((-1,10),0)
		vbox.Add(htmlpage, 1, wx.EXPAND|wx.ALL, 9)

		panel.SetSizer(vbox)
		self.MoveXY(100,100)
		self.Show(True)

class MacDictionary(wx.Frame):
	"""docstring for MyDictionary"""
	def __init__(self, *args, **kws):
		super(MacDictionary, self).__init__(*args, **kws)
		self.checkbox_flag = 0
		self.Path = '/Users/zero/Library/Containers/com.apple.Dictionary/Data/Library/Application Support/BetterDictionary'
		
		self.InitData()
		self.NewWordInText()
		self.InitUI()
		self.SetSize((600,400))
		self.SetTitle('MacDictionary')
		self.Centre()
		self.Show()

	def InitData(self):
		def deal_string_line(string_line):
			new_string = string_line.strip() #remove front whitespaces
			#remove <string> or </string> flags
			flag1 = '<string>'
			flag2 = '</string>'
			new_string = new_string.replace(flag1,'')
			new_string = new_string.replace(flag2,'')
			return new_string

		def dictFile2new_wordFile(exPath):
			count = 0
			back_up = [] # a list of every line string
			aimed_structure = []
			#return this back_up list
			dictFile = open(exPath+'/saved-words.plist')
			for everyline in dictFile:
				count +=1
				if count >=5:
					dealt_line = deal_string_line(everyline)
					back_up.append(dealt_line)
			#remove the last two item in aList
			length = len(back_up)
			back_up.remove(back_up[length-1])
			back_up.remove(back_up[length-2])
			# print 'bacu up','\n',back_up,'\n',len(back_up) #list of new_words string################
			# 已经从词典的文件中拿到了真是的数据，在写入txt文件中之前，
			#先把txt文件中的数据备份一下，重要的frequency和comments

			# read data from txt
			extract_new_word_list = []
			NewWordsFile = open(self.Path+'/everyday_words.txt','r')
			for everyline in NewWordsFile:
				everyline = everyline.split('#')
			NewWordsFile.close()
			
			everyline = everyline[0:-1]
			# print 'everyline','\n',everyline#######################################
			#从中提取出new_words 单独放在一个list里面
			for i in range(len(everyline)):
				if i%3==1:
					extract_new_word_list.append(everyline[i])
			#print 'extract_new_word_list','\n',extract_new_word_list
			for new_word in back_up:
				if new_word not in extract_new_word_list:
					everyline.append('0')
					everyline.append(new_word)
					everyline.append('Comments:')
				#aimed_structure.append([0,new_word,'Comments: '])

			newFile = open(exPath+'/everyday_words.txt','w')
			for char in everyline:
				newFile.write(char+'#')
			#for aList in aimed_structure:
				# for info in aList:
					# newFile.write(str(info)+'#') #add a flag for splitting when reading
			newFile.close()

		dictFile2new_wordFile(self.Path)

	def InitUI(self):
		menubar = wx.MenuBar()

		self.CreateStatusBar()

		filem= wx.Menu()
		setting = wx.NewId()
		filem.Append(setting, '&Setting')
		self.Bind(wx.EVT_MENU,self.OnSetting, id=setting)

		help = wx.Menu()
		about = wx.NewId()
		user_guide = wx.NewId()
		help.Append(about, '&About')
		help.Append(user_guide, 'User Guide')

		self.Bind(wx.EVT_MENU, self.OnAboutBox, id=about)
		self.Bind(wx.EVT_MENU, self.OnUser_Guide, id=user_guide)

		menubar.Append(filem, '&File')
		menubar.Append(help, '&Help')
		self.SetMenuBar(menubar)

		#main_panel
		self.main_panel = wx.Panel(self,-1)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		vbox1 = wx.BoxSizer(wx.VERTICAL)

		self.RE_setlabel()

		self.Bind(wx.EVT_CHECKBOX,self.cb0_checked, self.cb0)
		self.Bind(wx.EVT_CHECKBOX,self.cb1_checked, self.cb1)
		self.Bind(wx.EVT_CHECKBOX,self.cb2_checked, self.cb2)
		self.Bind(wx.EVT_CHECKBOX,self.cb3_checked, self.cb3)
		self.Bind(wx.EVT_CHECKBOX,self.cb4_checked, self.cb4)
		self.Bind(wx.EVT_CHECKBOX,self.cb5_checked, self.cb5)
		self.Bind(wx.EVT_CHECKBOX,self.cb6_checked, self.cb6)
		self.Bind(wx.EVT_CHECKBOX,self.cb7_checked, self.cb7)
		self.Bind(wx.EVT_CHECKBOX,self.cb8_checked, self.cb8)
		self.Bind(wx.EVT_CHECKBOX,self.cb9_checked, self.cb9)
		vbox1.Add((-1, 20))
		vbox1.Add(self.cb0)
		vbox1.Add(self.cb1, 0, wx.TOP, 7)
		vbox1.Add(self.cb2, 0, wx.TOP, 7)
		vbox1.Add(self.cb3, 0, wx.TOP, 7)
		vbox1.Add(self.cb4, 0, wx.TOP, 7)
		vbox1.Add(self.cb5, 0, wx.TOP, 7)
		vbox1.Add(self.cb6, 0, wx.TOP, 7)
		vbox1.Add(self.cb7, 0, wx.TOP, 7)
		vbox1.Add(self.cb8, 0, wx.TOP, 7)
		vbox1.Add(self.cb9, 0, wx.TOP, 7)
		hbox.Add(vbox1)

		vbox2 = wx.BoxSizer(wx.VERTICAL)

		self.comment_editor = wx.TextCtrl(self.main_panel, style = wx.TE_MULTILINE)
		hbox_btn = wx.BoxSizer(wx.HORIZONTAL)
		self.change_button = wx.Button(self.main_panel, label = 'Refresh', size=(70,30))
		self.close_button  = wx.Button(self.main_panel, label = 'Close',  size=(70,30))
		#bind event
		self.Bind(wx.EVT_BUTTON, self.OnChange, self.change_button)
		self.Bind(wx.EVT_BUTTON, self.OnClose, self.close_button)
		self.Bind(wx.EVT_TEXT, self.OnSaveModified, self.comment_editor)
		hbox_btn.Add(self.change_button)
		hbox_btn.Add(self.close_button, flag=wx.LEFT|wx.BOTTOM, border=5)

		vbox2.Add(self.comment_editor, proportion=1,flag=wx.EXPAND)
		vbox2.Add(hbox_btn, proportion=1, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)


		hbox.Add(vbox2, proportion=1, flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)
		hbox.Add((-1,25))

		self.main_panel.SetSizer(hbox)
	def RE_setlabel(self):
		self.cb0 = wx.CheckBox(self.main_panel, label = self.new_words_list[0][1],size=(150,25))
		self.cb1 = wx.CheckBox(self.main_panel, label = self.new_words_list[1][1],size=(150,25))
		self.cb2 = wx.CheckBox(self.main_panel, label = self.new_words_list[2][1],size=(150,25))
		self.cb3 = wx.CheckBox(self.main_panel, label = self.new_words_list[3][1],size=(150,25))
		self.cb4 = wx.CheckBox(self.main_panel, label = self.new_words_list[4][1],size=(150,25))
		self.cb5 = wx.CheckBox(self.main_panel, label = self.new_words_list[5][1],size=(150,25))
		self.cb6 = wx.CheckBox(self.main_panel, label = self.new_words_list[6][1],size=(150,25))
		self.cb7 = wx.CheckBox(self.main_panel, label = self.new_words_list[7][1],size=(150,25))
		self.cb8 = wx.CheckBox(self.main_panel, label = self.new_words_list[8][1],size=(150,25))
		self.cb9 = wx.CheckBox(self.main_panel, label = self.new_words_list[9][1],size=(150,25))

	def OnSaveModified(self,e):
		Modified_text = self.comment_editor.GetValue()
		self.new_words_list[self.checkbox_flag][2]=Modified_text
	
	def cb0_checked(self,e):
		if self.cb0.IsChecked():
			self.checkbox_flag = 0
			self.new_words_list[self.checkbox_flag][0] += 1
			self.comment_editor.ChangeValue(self.new_words_list[0][2])
			self.Show_StatusText(self.new_words_list[0][1]+' Is checked.')
		else:
			self.Show_StatusText('')
	def cb1_checked(self,e):
		if self.cb1.IsChecked():
			self.checkbox_flag = 1
			self.new_words_list[self.checkbox_flag][0] += 1
			self.comment_editor.ChangeValue(self.new_words_list[1][2])
			self.Show_StatusText(self.new_words_list[1][1]+' Is checked.')
		else:
			self.Show_StatusText('')
	def cb2_checked(self,e):
		if self.cb2.IsChecked():
			self.checkbox_flag = 2
			self.new_words_list[self.checkbox_flag][0] += 1
			self.comment_editor.ChangeValue(self.new_words_list[2][2])
			self.Show_StatusText(self.new_words_list[2][1]+' Is checked.')
		else:
			self.Show_StatusText('')
	def cb3_checked(self,e):
		if self.cb3.IsChecked():
			self.checkbox_flag = 3 
			self.new_words_list[self.checkbox_flag][0] += 1
			self.comment_editor.ChangeValue(self.new_words_list[3][2])
			self.Show_StatusText(self.new_words_list[3][1]+' Is checked.')
		else:
			self.Show_StatusText('')
	def cb4_checked(self,e):
		if self.cb4.IsChecked():
			self.checkbox_flag = 4 
			self.new_words_list[self.checkbox_flag][0] += 1
			self.comment_editor.ChangeValue(self.new_words_list[4][2])
			self.Show_StatusText(self.new_words_list[4][1]+' Is checked.')
		else:
			self.Show_StatusText('')
	def cb5_checked(self,e):
		if self.cb5.IsChecked():
			self.checkbox_flag = 5
			self.new_words_list[self.checkbox_flag][0] += 1
			self.comment_editor.ChangeValue(self.new_words_list[5][2])
			self.Show_StatusText(self.new_words_list[5][1]+' Is checked.')
		else:
			self.Show_StatusText('')
	def cb6_checked(self,e):
		if self.cb6.IsChecked():
			self.checkbox_flag = 6
			self.new_words_list[self.checkbox_flag][0] += 1
			self.comment_editor.ChangeValue(self.new_words_list[6][2])
			self.Show_StatusText(self.new_words_list[6][1]+' Is checked.')
		else:
			self.Show_StatusText('')
	def cb7_checked(self,e):
		if self.cb7.IsChecked():
			self.checkbox_flag = 7
			self.new_words_list[self.checkbox_flag][0] += 1
			self.comment_editor.ChangeValue(self.new_words_list[7][2])
			self.Show_StatusText(self.new_words_list[7][1]+' Is checked.')
		else:
			self.Show_StatusText('')
	def cb8_checked(self,e):
		if self.cb8.IsChecked():
			self.checkbox_flag = 8
			self.new_words_list[self.checkbox_flag][0] += 1
			self.comment_editor.ChangeValue(self.new_words_list[8][2])
			self.Show_StatusText(self.new_words_list[8][1]+' Is checked.')
		else:
			self.Show_StatusText('')
	def cb9_checked(self,e):
		if self.cb9.IsChecked():
			self.checkbox_flag = 9
			self.new_words_list[self.checkbox_flag][0] += 1
			self.comment_editor.ChangeValue(self.new_words_list[9][2])
			self.Show_StatusText(self.new_words_list[9][1]+' Is checked.')
		else:
			self.Show_StatusText('')

	def Show_StatusText(self,msg):
		sb = self.GetStatusBar()
		sb.SetStatusText(msg)

	def OnSetting(self,e):
		self.setting_dialog = wx.Frame(None, -1,'Choosing the path',size=(350,200))
		panel = wx.Panel(self.setting_dialog)
		vbox = wx.BoxSizer(wx.VERTICAL)
		

		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		self.path_textctrl = wx.TextCtrl(panel,size=(320,20))
		panel.Bind(wx.EVT_TEXT,self.GetPath, self.path_textctrl)#

		hbox1.Add(self.path_textctrl, proportion=1)
		vbox.Add(hbox1,flag=wx.LEFT|wx.RIGHT|wx.TOP, border=38)
		vbox.Add((-1,80))

		# two buttons: Cancel and OK
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		button_cancle=wx.Button(panel,label='Cancel',size=(70,30))
		self.setting_dialog.Bind(wx.EVT_BUTTON,self.Onsetting_dialog_Cancle, button_cancle)#
		hbox2.Add(button_cancle)
		#--
		button_OK   =wx.Button(panel,label='OK',   size=(70,30))
		hbox2.Add(button_OK,flag=wx.LEFT|wx.BOTTOM, border=10)
		self.setting_dialog.Bind(wx.EVT_BUTTON,self.OnSetting_dialog_OK, button_OK)#
		##
		vbox.Add(hbox2,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)


		panel.SetSizer(vbox)
		self.setting_dialog.Show()
	def GetPath(self,e):
		self.Path = str(self.path_textctrl.GetValue())
		self.InitData()
		self.NewWordInText()

	def NewWordInText(self):
		# return a list of list of int and string
		self.new_words_list = []
		# text format:
		# ['0', 'Github', 'Comments: ', '0', 'Breed', 'Comments: ', '0', 'Square', 'Comments: ', '0', 'Stem', 'Comments: ', '0', 'Veto', 'Comments: ', '0', 'Toggle', 'Comments: ', '0', 'Gauge', 'Comments: ', '0', 'Intensive', 'Comments: ', '0', 'Column', 'Comments: ', '0', 'Gnome', 'Comments: ', '0', 'Structure', 'Comments: ', '0', 'Zero', 'Comments: ', '0', 'Test', 'Comments: '] 
		string_words = ''
		NewWordsFile = open(self.Path+'/everyday_words.txt','r')
		for everyline in NewWordsFile:
			everyline = everyline.split('#') #a list i want
		NewWordsFile.close()
		everyline = everyline[0:-1]
		# print everyline,'\n',len(everyline)
		for i in range(len(everyline)):
			if i%3 == 0:
				everyline[i] = int(everyline[i])  #list comprehension will be better and simple.
		middle = []
		for info in everyline:
			if len(middle)<3:
				middle.append(info)
			else:
				self.new_words_list.append(middle)
				middle = [info]
		if len(middle) != 0:
			self.new_words_list.append(middle)

		self.new_words_list.sort()
		#print self.new_words_list

		#print everyline,'\n',len(everyline)

	def Onsetting_dialog_Cancle(self,e):
		self.setting_dialog.Close()
	def OnSetting_dialog_OK(self,e):
		self.setting_dialog.Close()
	def OnAboutBox(self,e):
		info = wx.AboutDialogInfo()
		info.SetName(' About ')
		info.SetWebSite('https://github.com/zeroLZY')
		info.AddDeveloper('Zero Lee')
		info.AddDocWriter('Zero Lee')
		info.AddArtist('Zero Lee')
		info.AddTranslator('Zero Lee')
		wx.AboutBox(info)

	def OnUser_Guide(self,e):
		display_user_guide = HTML_display(None, -1, 'User Guide',user_guide_markdown)

	def OnChange(self,e):
		#Save first
		change_times = 0
		Save_File = open(self.Path + '/everyday_words.txt','w')
		for aList in self.new_words_list:
			for info in aList:
				Save_File.write(str(info)+'#')
		Save_File.close()


		#clear all check
		self.cb0.SetValue(0)
		self.cb1.SetValue(0)
		self.cb2.SetValue(0)
		self.cb3.SetValue(0)
		self.cb4.SetValue(0)
		self.cb5.SetValue(0)
		self.cb6.SetValue(0)
		self.cb7.SetValue(0)
		self.cb8.SetValue(0)
		self.cb9.SetValue(0)

		# re_ setlabel only
		self.new_words_list.sort()
		self.cb0.SetLabel(self.new_words_list[0][1])
		self.cb1.SetLabel(self.new_words_list[1][1])
		self.cb2.SetLabel(self.new_words_list[2][1])
		self.cb3.SetLabel(self.new_words_list[3][1])
		self.cb4.SetLabel(self.new_words_list[4][1])
		self.cb5.SetLabel(self.new_words_list[5][1])
		self.cb6.SetLabel(self.new_words_list[6][1])
		self.cb7.SetLabel(self.new_words_list[7][1])
		self.cb8.SetLabel(self.new_words_list[8][1])
		self.cb9.SetLabel(self.new_words_list[9][1])



	def OnClose(self,e):
		Save_File = open(self.Path + '/everyday_words.txt','w')
		for aList in self.new_words_list:
			for info in aList:
				Save_File.write(str(info)+'#')
		Save_File.close()
		self.Close()




if __name__ == '__main__':
	ex = wx.App()
	MacDictionary(None)
	ex.MainLoop()
