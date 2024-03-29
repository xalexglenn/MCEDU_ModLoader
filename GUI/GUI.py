#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.0 on Tue Jan 22 13:01:03 2019
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((770, 754))
        self.prompt = wx.StaticText(self, wx.ID_ANY, "Today is a good day for Minecraft")
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)
        self.main_pane = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.directory_choose_button = wx.Button(self.main_pane, wx.ID_ANY, u"📁 Change Mod Folder")
        self.mod_directory = wx.StaticText(self.main_pane, wx.ID_ANY, "!Mod Folder Not Found!")
        self.minecraft_directory_choose_button = wx.Button(self.main_pane, wx.ID_ANY, u"📁 Change MinecraftEDU Directory")
        self.minecraft_directory = wx.StaticText(self.main_pane, wx.ID_ANY, "!MinecraftEDU Application Folder Not Found!")
        self.mod_config_dropdown = wx.ComboBox(self.main_pane, wx.ID_ANY, choices=["None (Create New Mod Configuration)"], style=wx.CB_DROPDOWN)
        self.save_mod_config_button = wx.Button(self.main_pane, wx.ID_ANY, "Save Mod Configuration")
        self.load_mod_config_button = wx.Button(self.main_pane, wx.ID_ANY, "Load Mod Configuration")
        self.client_checkbox = wx.CheckBox(self.main_pane, wx.ID_ANY, "Client")
        self.server_checkbox = wx.CheckBox(self.main_pane, wx.ID_ANY, "Server")
        self.refresh_button = wx.Button(self.main_pane, wx.ID_ANY, u"↻ Refresh Mod List")
        self.clear_mod_checkboxes_button = wx.Button(self.main_pane, wx.ID_ANY, "Clear Mod Checkboxes")
        self.ip_address_textbox = wx.TextCtrl(self.main_pane, wx.ID_ANY, "localhost")
        self.load_mods_button = wx.Button(self.main_pane, wx.ID_ANY, "Load Mods")
        self.load_and_run_button = wx.Button(self.main_pane, wx.ID_ANY, "Load Mods and Run")
        self.panel = wx.ScrolledWindow(self.main_pane, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.settings_pane = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.mod_configurations_pane = wx.Panel(self.notebook_1, wx.ID_ANY)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Alex Glenn's Mod Loader 3000 Deluxe")
        self.prompt.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.mod_config_dropdown.SetSelection(0)
        self.client_checkbox.SetValue(1)
        self.ip_address_textbox.SetMinSize((150, 22))
        self.load_mods_button.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.load_mods_button.SetDefault()
        self.load_and_run_button.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.load_and_run_button.SetDefault()
        self.panel.SetScrollRate(10, 10)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        mod_config_pane_sizer = wx.BoxSizer(wx.VERTICAL)
        settings_pane_sizer = wx.BoxSizer(wx.VERTICAL)
        pane_1_sizer = wx.BoxSizer(wx.VERTICAL)
        self.bottom_area = wx.BoxSizer(wx.VERTICAL)
        top_area = wx.BoxSizer(wx.VERTICAL)
        Load_Mods_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        client_server_options = wx.BoxSizer(wx.HORIZONTAL)
        mod_configs = wx.BoxSizer(wx.HORIZONTAL)
        Minecraft_Directory_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        mod_directory_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.prompt, 0, wx.ALIGN_CENTER | wx.TOP, 5)
        mod_directory_sizer.Add(self.directory_choose_button, 0, wx.BOTTOM | wx.TOP, 3)
        mod_directory_sizer.Add(self.mod_directory, 0, wx.BOTTOM | wx.TOP, 3)
        top_area.Add(mod_directory_sizer, 1, wx.EXPAND, 0)
        Minecraft_Directory_Sizer.Add(self.minecraft_directory_choose_button, 0, wx.BOTTOM | wx.TOP, 3)
        Minecraft_Directory_Sizer.Add(self.minecraft_directory, 0, wx.BOTTOM | wx.TOP, 3)
        top_area.Add(Minecraft_Directory_Sizer, 1, wx.EXPAND, 0)
        static_line_3 = wx.StaticLine(self.main_pane, wx.ID_ANY)
        top_area.Add(static_line_3, 0, wx.EXPAND, 0)
        mod_configs.Add(self.mod_config_dropdown, 0, wx.ALL, 3)
        mod_configs.Add(self.save_mod_config_button, 0, wx.ALL, 3)
        mod_configs.Add(self.load_mod_config_button, 0, wx.ALL, 3)
        top_area.Add(mod_configs, 1, wx.ALL | wx.EXPAND, 0)
        static_line_4 = wx.StaticLine(self.main_pane, wx.ID_ANY)
        top_area.Add(static_line_4, 0, wx.BOTTOM | wx.EXPAND | wx.TOP, 2)
        client_server_options.Add(self.client_checkbox, 0, 0, 0)
        client_server_options.Add(self.server_checkbox, 0, 0, 0)
        client_server_options.Add(self.refresh_button, 0, wx.LEFT, 25)
        client_server_options.Add(self.clear_mod_checkboxes_button, 0, wx.LEFT | wx.RIGHT, 15)
        top_area.Add(client_server_options, 0, wx.BOTTOM | wx.TOP, 2)
        label_1 = wx.StaticText(self.main_pane, wx.ID_ANY, "Direct Connect Server IP")
        sizer_1.Add(label_1, 0, 0, 0)
        sizer_1.Add(self.ip_address_textbox, 0, wx.LEFT | wx.RIGHT, 1)
        top_area.Add(sizer_1, 1, wx.BOTTOM | wx.EXPAND | wx.TOP, 3)
        Load_Mods_Sizer.Add(self.load_mods_button, 0, wx.RIGHT, 20)
        Load_Mods_Sizer.Add(self.load_and_run_button, 0, 0, 5)
        top_area.Add(Load_Mods_Sizer, 0, wx.BOTTOM | wx.EXPAND | wx.TOP, 2)
        static_line_1 = wx.StaticLine(self.main_pane, wx.ID_ANY)
        top_area.Add(static_line_1, 0, wx.EXPAND | wx.TOP, 5)
        pane_1_sizer.Add(top_area, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        self.bottom_area.Add((0, 0), 0, 0, 0)
        self.panel.SetSizer(self.bottom_area)
        pane_1_sizer.Add(self.panel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        self.main_pane.SetSizer(pane_1_sizer)
        settings_pane_sizer.Add((0, 0), 0, 0, 0)
        self.settings_pane.SetSizer(settings_pane_sizer)
        mod_config_pane_sizer.Add((0, 0), 0, 0, 0)
        self.mod_configurations_pane.SetSizer(mod_config_pane_sizer)
        self.notebook_1.AddPage(self.main_pane, "Main")
        self.notebook_1.AddPage(self.settings_pane, "Settings")
        self.notebook_1.AddPage(self.mod_configurations_pane, "Mod Configurations")
        main_sizer.Add(self.notebook_1, 1, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 1)
        self.SetSizer(main_sizer)
        self.Layout()
        # end wxGlade

# end of class MyFrame

class ModLoader(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class ModLoader

if __name__ == "__main__":
    ModLoader = ModLoader(0)
    ModLoader.MainLoop()
