#   Created by Alexander Glenn in 2018
#
#
#
#   mod_directory is a string representing the absolute path to the root mod folder.
#   The structure for the mod folder should be:
#
#       1. a root folder (e.g. "Minecraft Mods")
#       2. in that folder, many folders, one for each "mod package"
#       3. in each of those folders are the actual mod files
#       4. if there are optional mod extensions, make a folder for them next to
#          the mods (e.g. an Extra Planets folder inside the Galacticraft folder)
#
#   "Mod Packages" should be fully functioning groups of mods, so if a mod has
#   multiple required files, all of them should be in the same folder
#

from typing import Dict

import pathlib
import wx
import shutil
import os
import multiprocessing
import subprocess
import configparser
import itertools
import io
import json
import time
import datetime

import ModFolder
from GUI import GUI


class ModLoader(wx.App):
    frame: GUI.MyFrame
    config_files: Dict[str, configparser.ConfigParser]
    paths: Dict[str, pathlib.Path]
    locked_paths: Dict[str, pathlib.Path]
    mod_folder: ModFolder

    def OnInit(self):
        self.frame = GUI.MyFrame(None, wx.ID_ANY, "")
        self.mod_folder = None
        self.locked_paths = {'settings': pathlib.Path('mod_loader_settings.txt'),
                             'this_app': pathlib.Path.cwd(),
                             'local_mod_configs': pathlib.Path.home() / 'Documents/Mod_Loader_Configs'}
        self.paths = {'shared_folder': pathlib.Path.home() / 'Google Drive'}
        self.paths['Mod_Loader_Folder'] = self.paths['shared_folder'] / 'Minecraft Mod Loader'
        self.paths['shared_mod_configs'] = self.paths['Mod_Loader_Folder'] / 'Mod Configurations'
        self.config_files = {}

        minecraft_dir = pathlib.Path.home() / 'Library/Application Support/minecraftedu'
        if minecraft_dir.is_dir():
            self.set_minecraftEDU_paths(minecraft_dir)
            self.frame.minecraft_directory.SetLabel('MinecraftEDU Directory: ' +
                                                    str(self.paths['minecraftedu'].expanduser()))

        mod_dir = pathlib.Path.home() / 'Google Drive' / 'Minecraft Mods'
        if mod_dir.is_dir():
            self.paths['mod_folder'] = mod_dir
            self.refresh()

        # if self.locked_paths['settings'].is_file():
            # self.load_settings()
        # else:
            # self.save_settings()

        self.bind_events()

        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

    '''
    Saves all editable settings in a JSON file
    '''
    def save_settings(self):
        os.chdir(str(self.locked_paths['this_app']))
        # construct settings dict
        temp_paths = {}
        for key, value in self.paths.items():
            temp_paths[key] = str(value)
        settings = {
            'paths': temp_paths
        }
        with open(str(self.locked_paths['settings']), 'w') as f:
            json.dump(settings, f, indent='\t')

    '''
    Load settings from JSON file created by self.save_settings()
    '''
    def load_settings(self):
        os.chdir(str(self.locked_paths['this_app']))
        with open(str(self.locked_paths['settings'])) as f:
            settings = json.load(f)
        # load settings into attributes
        for key, value in settings['paths'].items():
            self.paths[key] = pathlib.Path(value)

    '''
    Bind functions to wx GUI elements here
    '''
    def bind_events(self):
        self.Bind(wx.EVT_BUTTON, self.choose_mod_folder, self.frame.directory_choose_button)
        self.Bind(wx.EVT_BUTTON, self.choose_minecraftEDU_directory, self.frame.minecraft_directory_choose_button)
        self.Bind(wx.EVT_BUTTON, self.refresh, self.frame.refresh_button)
        self.Bind(wx.EVT_BUTTON, self.load_mods, self.frame.load_mods_button)
        self.Bind(wx.EVT_BUTTON, self.load_and_run, self.frame.load_and_run_button)
        self.Bind(wx.EVT_BUTTON, self.save_mod_config, self.frame.save_mod_config_button)
        self.Bind(wx.EVT_BUTTON, self.clear_mod_checkboxes, self.frame.clear_mod_checkboxes_button)

    '''
    Unchecks all checked mod checkboxes
    '''
    def clear_mod_checkboxes(self, event=None):
        for f in self.mod_folder:
            if isinstance(f, ModFolder.Folder) and f.parent is not None:
                f.checkbox.SetValue(False)

    def choose_mod_folder(self, event=None):  # wxGlade: MyFrame.<event_handler>
        with wx.DirDialog(self.frame, "Choose the Folder Containing ALL Minecraft Mods",
                          style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            self.paths['mod_folder'] = fileDialog.GetPath()
            self.frame.mod_directory.SetLabel('MinecraftEDU Directory:' +
                                                    str(self.paths['mod_folder'].expanduser()))
            self.refresh()

    def choose_minecraftEDU_directory(self, event=None):  # wxGlade: MyFrame.<event_handler>
        with wx.DirDialog(self.frame, "Choose the minecraftedu folder",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            self.set_minecraftEDU_paths(fileDialog.GetPath())
            self.frame.minecraft_directory.SetLabel('MinecraftEDU Directory:' +
                                                    str(self.paths['minecraftedu'].expanduser()))
            self.refresh()

    def set_minecraftEDU_paths(self, path):
        self.paths['minecraftedu'] = pathlib.Path(path)
        self.paths['client_mods'] = self.paths['minecraftedu'] / 'minecraft/mods/1.7.10'
        self.paths['server_mods']  = self.paths['minecraftedu'] / 'servertool/server/mods/1.7.10'
        self.paths['launcher_settings'] = self.paths['minecraftedu'] / 'launcher_res' / 'settings'
        self.paths['minecraft_options'] = self.paths['minecraftedu'] / 'minecraft' / 'options.txt'


        self.config_files['launcher_settings'] = configparser.ConfigParser()
        self.headless_config(self.config_files['launcher_settings'],
                             self.paths['launcher_settings'] / 'launchersettings.ini')
        self.backup_file(self.paths['launcher_settings'] / 'launchersettings.ini', only_once=True)

        self.config_files['minecraft_options'] = configparser.ConfigParser(delimiters=':')
        self.config_files['minecraft_options'].optionxform = str
        self.headless_config(self.config_files['minecraft_options'],
                             self.paths['minecraft_options'])
        self.backup_file(self.paths['minecraft_options'], only_once=True)
        self.frame.ip_address_textbox.Value = self.config_files['minecraft_options'].get('top', 'lastServer')

    def modify_config_files(self):
        self.minecraft_config_fixes()
        self.config_files['launcher_settings'].set('top', 'minecraft-client-ram', '1700')
        self.config_files['minecraft_options'].set('top', 'lastServer', self.frame.ip_address_textbox.Value)
        self.config_files['minecraft_options'].set('top', 'maxFps', '60')
        self.config_files['minecraft_options'].set('top', 'fancygraphics', 'true')
        self.config_files['minecraft_options'].set('top', 'fov', '0.0')
        self.config_files['minecraft_options'].set('top', 'enableVsync', 'true')
        self.config_files['minecraft_options'].set('top', 'mipmapLevels', '0')
        self.config_files['minecraft_options'].set('top', 'gamma', '1.0')
        self.headless_write(self.config_files['minecraft_options'], self.paths['minecraft_options'])

    def refresh(self, event=None):  # wxGlade: MyFrame.<event_handler>
        if 'mod_folder' not in self.paths:
            self.prompt('Mod Folder Path Not Set')
            return
        else:
            self.mod_folder = ModFolder.Folder(self.paths['mod_folder'])

        self.frame.mod_directory.SetLabel('Mods from Folder:' + str(self.mod_folder.path.expanduser()))
        self.frame.bottom_area.Clear()
        self.frame.Refresh()
        self.mod_folder.sizer = self.frame.bottom_area
        if 'client_mods' in self.paths:
            current_mods = list(map(lambda x: x.name, self.paths['client_mods'].glob('*')))
            self.populate_checkboxes(self.mod_folder, current_mods)
        self.frame.Layout()

    def populate_checkboxes(self, parent: ModFolder.Folder, current_mods=None, depth=0):
        if parent.parent is not None:
            parent.checkbox.Value = True
        for node in parent.children:
            if isinstance(node, ModFolder.Folder):
                mod_sizer = wx.BoxSizer(wx.VERTICAL)
                top_sizer = wx.BoxSizer(wx.HORIZONTAL)

                for i in range(depth):
                    top_sizer.Add((20, 20))
                node.checkbox = wx.CheckBox(self.frame.panel, wx.ID_ANY, str(node))

                node.checkbox.folder = node
                top_sizer.Add(node.checkbox)
                if depth > 0:
                    node.checkbox.Enable(True)

                self.Bind(wx.EVT_CHECKBOX, self.checkbox_event, node.checkbox)

                mod_sizer.Add(top_sizer, 0, 0, 0)
                node.sizer = wx.BoxSizer(wx.VERTICAL)
                mod_sizer.Add(node.sizer, 0, 0, 0)
                self.populate_checkboxes(node, current_mods, depth=depth+1)

                parent.sizer.Add(mod_sizer, 0, 0, 0)
            elif str(node) not in current_mods:
                if parent.parent is not None:
                    parent.checkbox.Value = False

    def load_mods(self, event=None):
        if self.mod_folder is None or 'minecraftedu' not in self.paths:
            self.prompt('Folder or Directory is not set')
            return
        if not self.paths['client_mods'].is_dir() or not self.paths['server_mods'].is_dir():
            self.prompt('Something is wrong with your Minecraft Directory. Change Directories or Reinstall')
            return

        self.modify_config_files()

        if self.frame.client_checkbox.GetValue():
            self.clear_directory(self.paths['client_mods'])
            for node in self.mod_folder:
                if not isinstance(node, ModFolder.Folder):
                    if node.parent.checkbox is not None and node.parent.checkbox.GetValue():
                        shutil.copy2(str(node.path), str(self.paths['client_mods']))

        if self.frame.server_checkbox.GetValue():
            self.clear_directory(self.paths['server_mods'])
            for node in self.mod_folder:
                if not isinstance(node, ModFolder.Folder):
                    if node.parent.checkbox is not None and node.parent.checkbox.GetValue():
                        shutil.copy2(str(node.path), str(self.paths['server_mods']))

    def minecraft_config_fixes(self):
        # clear any ignored client/server mods, as it does not reliably work for disabling mods
        self.paths['launcher_settings'] = self.paths['minecraftedu'] / 'launcher_res' / 'settings'
        with open(str(self.paths['launcher_settings'] / 'ignoredclientmods.ini'), 'w') as f:
            f.write('')
        with open(str(self.paths['launcher_settings'] / 'ignoredservermods.ini'), 'w') as f:
            f.write('')

    def load_and_run(self, event=None):
        self.load_mods()
        if self.frame.client_checkbox.GetValue():
            # Skip default Minecraft EDU GUI
            self.config_files['launcher_settings'].set('top', 'skip-gui-and-force-client-launch', 'true')
            multiprocessing.Process(target=self.disable_gui_skip).start()
            self.headless_write(self.config_files['launcher_settings'],
                                self.paths['launcher_settings'] / 'launchersettings.ini')

            multiprocessing.Process(target=self.launch_jar,
                                    kwargs={'path': self.paths['minecraftedu'] / 'Launcher.jar'}).start()

        if self.frame.server_checkbox.GetValue():
            multiprocessing.Process(target=self.launch_jar,
                                    kwargs={'path': self.paths['minecraftedu'] / 'servertool' / 'ServerWizard.jar'}).start()

        # keep users from spamming the Run button
        self.frame.load_and_run_button.Enable(False)
        wx.CallLater(10000, self.frame.load_and_run_button.Enable)

    def save_mod_config(self, event=None):
        save_dict = {}

        checked_mods = []
        for node in self.mod_folder:
            if hasattr(node, 'checkbox') and node.checkbox is not None and node.checkbox.GetValue():
                checked_mods.append(list(node.md5_set()))
        save_dict['checked_mods'] = checked_mods
        temp_selection = self.frame.mod_config_dropdown.GetSelection()
        if temp_selection == 0:
            print(self.paths['shared_mod_configs'].is_dir())
            with wx.FileDialog(self.frame, "Save Configuration File", defaultDir=str(self.paths['shared_mod_configs']),
                               wildcard="JSON files (*.json)|*.json",
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind
                # save the current contents in the file
                save_path = fileDialog.GetPath()
        else:
            save_path = self.paths['shared_mod_configs'] / temp_selection

        with open(save_path, 'w') as f:
            json.dump(save_dict, f)
        # TODO: establish save file path and write json file

    def launch_jar(self, path: pathlib.Path):
        # if path.parent not in self.paths:
        #     return
        os.chdir(path.parent)
        environment = os.environ.copy()
        environment["JAVA_HOME"] = str(self.determine_jdk_version() / 'Contents' / 'Home')
        subprocess.run(['java', '-jar', str(path)], env=environment)

    '''
    Eventually reenable MinecraftEDU default GUI
    There's a chance this doesn't have to be a separate Process and should use wx.CallLater
    '''
    def disable_gui_skip(self):
        time.sleep(20)
        config_setting = {'skip-gui-and-force-client-launch': 'false'}
        self.set_config(self.config_files['launcher_settings'],
                        self.paths['launcher_settings'] / 'launchersettings.ini',
                        config_setting)

    def set_config(self, config: configparser.ConfigParser, path: pathlib.Path,
                   changes: Dict[str, str], section='top'):
        for option, value in changes.items():
            config.set(section, option, value)
        self.headless_write(config, path)

    '''
    Like print, but shows relevant text on GUI as well
    Also saves text to a log file
    Generally preferred to print
    '''
    def prompt(self, message, logfile=True, gui_prompt=True):
        print(message)
        if logfile:
            self.append_write(self.paths['Mod_Loader_Folder'] / 'prompt_log.txt',
                              os.linesep.join([os.linesep, str(datetime.datetime.today()), message]))
        if gui_prompt:
            self.frame.prompt.SetForegroundColour((255, 0, 0))
            self.frame.prompt.SetLabel(message)

    '''
    credit to ʇsәɹoɈ from
    https://stackoverflow.com/questions/2885190/using-pythons-configparser-to-read-a-file-without-section-name
    
    virtually adds [top] section header to the start of a config file
    this is because configparser only works with config files that have sections indicated by [headers]
    '''
    def headless_config(self, parser: configparser.ConfigParser, file_path, head_section: str = 'top'):
        try:
            parser.read(file_path)
        except configparser.MissingSectionHeaderError:
            with open(file_path) as lines:
                lines = itertools.chain(("[" + head_section + "]",), lines)  # This line does the trick.
                try:
                    parser.read_file(lines)
                except configparser.DuplicateOptionError as e:
                    self.prompt('error in file ' + str(file_path) + ': ' + str(e))

    @staticmethod
    def append_write(path: pathlib.Path, text: str):
        if path.is_file():
            mode = 'a'
        else:
            mode = 'w'
        with open(str(path), mode) as f:
            f.write(text)

    @staticmethod
    def checkbox_event(event: wx.CommandEvent):
        folder = event.GetEventObject().folder
        for node in folder.children:
            if hasattr(node, 'checkbox'):
                if not event.IsChecked():
                    node.checkbox.SetValue(False)
                node.checkbox.Enable(event.IsChecked())
        event.Skip()

    @staticmethod
    def headless_write(parser: configparser.ConfigParser, target: pathlib.Path, head_section: str = 'top'):
        parser_data = io.StringIO()
        parser.write(parser_data, space_around_delimiters=False)
        with open(str(target), 'w') as f:
            f.write(parser_data.getvalue()[len(head_section)+2:])

    '''
    if only_once is True, only creates backup if one does not already exist
    '''
    @staticmethod
    def backup_file(path, only_once=False):
        backup_path = path.parent / ('backup_' + path.name)
        if only_once and backup_path.is_file():
            print(str(backup_path) + ' already exists, backup not created')
            return
        shutil.copy2(path, backup_path)

    @staticmethod
    def clear_directory(d: pathlib.Path):
        for p in d.iterdir():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()

    '''
    Determines if JDK1.8 is available, and returns one of the available 1.8 JDKs
    I'm sure there's a wider range of versions that don't cause problems with MCEDU,
    but testing various JDK versions is not worth it right now. 
    '''
    @staticmethod
    def determine_jdk_version():
        jdk_directory = pathlib.Path('/Library/Java/JavaVirtualMachines')
        for i in jdk_directory.glob('*'):
            if i.name.startswith('jdk1.8'):
                return i


if __name__ == "__main__":
    Mod_Manager = ModLoader(0)
    Mod_Manager.MainLoop()

