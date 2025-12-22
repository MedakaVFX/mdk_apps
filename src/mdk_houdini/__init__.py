""" mdk_houdini
 
* VFX用Pythonパッケージ

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya Yamagishi
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.2 [v0.0.2] 2025-12-15 Tatsuya Yamagishi
        * added: get_frame_range()

    * v0.0.1 2025-11-15 Tatsuya Yamagishi
        * New
"""

VERSION = 'v0.0.2'
NAME = 'mdk_houdini'

import os
import re
import pathlib
import platform
import subprocess
import sys

import hou


if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdk_houdini package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')

# ======================================= #
# Settings
# ======================================= #
EXT = {
    'hindie': '.hiplc',
    'houdinifx': '.hip',
}

EXT_LIST = [
    '.abc',
    '.hip',
    '.hiplc',
    '.bgeo',
]

EXT_DICT = {
    'asset': '.dat',
    'shot': '.txt',
    'geo': '.abc',
    'usd': '.usd',
}

FILE_FILTER_HIP = re.compile(r'.+\.(hip)')
FILE_FILTER_USD = re.compile(r'.+\.(usd|usdc|usda|usdz)')
FILE_FILTER_VBD = re.compile(r'.+\.(vdb)')

FILENODE_DICT = {
    'alembic': 'filename',
    'arnold': 'ar_picture',
    'arnold_rendersettings': 'productName',
    'configurelayer': 'savepath',
    'file': 'file',
    'filecache::2.0': 'file',
    'reference::2.0': 'sopoutput',
    'rop_alembic': 'rop_alembic',
    'rop_geometry': 'sopoutput',
    'usdexport': 'lopoutput',
    'usd_rop': 'lopoutput',
    'volume': 'filepath1',
}

SCRIPT_EXT_LIST = ['.py']

# ======================================= #
# Get
# ======================================= #
def get_ext() -> str:
    """ 拡張子を返す
    * モードを判定して拡張子を返す
    
    Returns:
        str: 拡張子 hip, hiplc
    """
    _mode = hou.applicationName()
    _ext = EXT.get(_mode)

    if _ext:
        return _ext
    else:
        return '.hip'
    
def get_ext_list():
    """ 拡張子リストを返す"""
    return list(EXT_LIST)

def get_fps() -> float:
    """ FPSを取得
    * Plugin Builtin Function

    Returns:
        float: フレームレート
    """
    return hou.fps()
    
def get_filepath() -> str:
    """ Plugin Builtin Function """
    return hou.hipFile.path()

def get_frame_range() -> tuple[int, int]:
    """ フレームレンジを取得
    
    Returns:
        tuple[int, int]: フレームレンジ (start, end)
    """
    start, end = hou.playbar.frameRange()
    return (int(start), int(end))

def get_main_window():
    """ Get the Houdini main window.

    * Reference from: https://russell-vfx.com/blog/2020/8/20/main-window

    Returns:
        PySide2.QtWidgets.QWidget: 'QWidget' Houdini main window.
    """
    return hou.qt.mainWindow()


def get_selected_nodes() -> list:
    """ 選択しているノードを取得
    
    Returns:
        list: 選択しているノードリスト
    """
    return hou.selectedNodes()

def get_script_exts() -> list[str]:
    """ スクリプト拡張子リストを取得
    
    Returns:
        list[str]: スクリプト拡張子リスト
    """
    return SCRIPT_EXT_LIST


# ======================================= #
# Set
# ======================================= #
def set_fps(value: float):
    """ フレームレートを設定 """
    hou.setFps(int(value+0.05))

def set_framerange(head_in: int, cut_in: int, cut_out: int, tail_out: int):
    """ フレームレンジを設定
    
    Args:
        head_in (int): ヘッドイン
        cut_in (int): カットイン
        cut_out (int): カットアウト
        tail_out (int): テイルアウト
    """
    hou.playbar.setPlaybackRange(cut_in, cut_out)     # 再生範囲
    hou.playbar.setFrameRange(head_in, tail_out)

def set_unit(unit: str):
    """ 単位を設定

    * houdiniは単位設定がないのでpass
    
    """
    unit_dict = {
        'centimeter': 0.01,
        'millimeter': 0.001,
        'meter': 1.0,
        'kilometer': 1000.0,
    }
    

# ======================================= #
# Functins
# ======================================= #
def create_playblast(
        filepath: str,
        size: tuple[int]|list[int],
        framerange: tuple[int],
    ):


    _cur_desktop = hou.ui.curDesktop()
    _scene = _cur_desktop.paneTabOfType(hou.paneTabType.SceneViewer)
    if not _scene:
        return

    if not _scene.isCurrentTab():
        _scene.setIsCurrentTab()

    _flip_options = _scene.flipbookSettings().stash()
    _flip_options.resolution(size) 
    _flip_options.outputToMPlay(False)
    _flip_options.frameRange(framerange)
    _flip_options.output(filepath)
    _scene.flipbook(_scene.curViewport(), _flip_options)


def open_dir(filepath):
    """
    フォルダを開く
    """
    _filepath = pathlib.Path(filepath)
    OS_NAME = platform.system()

    if _filepath.exists():
        if _filepath.is_file():
            _filepath = _filepath.parent

        if OS_NAME == 'Windows':
            cmd = 'explorer {}'.format(str(_filepath))
            subprocess.Popen(cmd)

        elif OS_NAME == 'Darwin':
            subprocess.Popen(['open', _filepath])

        else:
            subprocess.Popen(["xdg-open", _filepath])


def open_folder(value: str):
    """
    フォルダを開く
    """
    _filepath = pathlib.Path(value)
    OS_NAME = platform.system()

    if _filepath.exists():
        if _filepath.is_file():
            _filepath = _filepath.parent

        if OS_NAME == 'Windows':
            cmd = 'explorer {}'.format(str(_filepath))
            subprocess.Popen(cmd)

        elif OS_NAME == 'Darwin':
            subprocess.Popen(['open', _filepath])

        else:
            subprocess.Popen(["xdg-open", _filepath])



def open_in_explorer(filepath: str):
    """
    Explorerでフォルダを開く
    """
    if os.path.exists(filepath):
        if platform.system() == 'Windows':
            filepath = str(filepath)
            filepath = filepath.replace('/', '\\')

            filebrowser = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
            subprocess.run([filebrowser, '/select,', os.path.normpath(filepath)])
        
        elif platform.system() == 'Darwin':
            subprocess.call(['open', filepath])
        
        else:
            subprocess.Popen(["xdg-open", filepath])
    else:
        raise FileNotFoundError(f'File is not found.')


def save_file(filepath: str):
    """ Plugin Builtin Function
    
    * 名前を付けて保存

    """
    hou.hipFile.save(file_name=filepath, save_to_recent_files=True)

# ======================================= #
# Class
# ======================================= #
class AppMain:
    def __init__(self):
        self._unit_scale = 0.01
    




    def get_current_network_path(self):
        """ 現在のNetwork Editorを取得 """
        network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)

        if network_editor:
            # Network Editorのパスを取得
            return network_editor.pwd().path()
        
        
    def get_current_node(self):
        _network_path = self.get_current_network_path()

        if _network_path:
            return hou.node(_network_path)
        

    def get_default_ext(self) -> str:
        """ 拡張子を返す 
        
        
        """
        EXT_DICT = {
            'hindie': '.hiplc',
            'houdinifx': '.hiplc',
            }
        
        _mode = hou.applicationName()
        
        return EXT_DICT[_mode]
            

    

    def get_filepath(self) -> str:
        return hou.hipFile.path()
    




    def get_framerange(self) -> tuple[int]:
        """ Plugin Builtin Function """
        head_in, tail_out = hou.playbar.frameRange()
        cut_in, cut_out = hou.playbar.frameRange()

        return head_in, cut_in, cut_out, tail_out
    
    

    def get_network_pane(self, cursor=True, node=None, multiple=False):
        ptype = hou.paneTabType.NetworkEditor
        under_cursor = hou.ui.paneTabUnderCursor()

        if under_cursor and under_cursor.type() == ptype and not multiple:
            if not node or node == under_cursor.pwd():
                return under_cursor

        if node:
            valid_tabs = []
            for tab in hou.ui.paneTabs():
                if tab.type() == ptype and tab.pwd() == node:
                    valid_tabs.append(tab)

            if valid_tabs:
                if multiple:
                    return valid_tabs
                else:
                    return valid_tabs[0]

        if under_cursor and under_cursor.type() == ptype:
            return under_cursor

        paneTab = hou.ui.paneTabOfType(ptype)

        if paneTab and multiple:
            return [paneTab]
        else:
            return paneTab
    


    def go_to_node(self, node):
        if node is not None:
            if type(node) == str:
                node = hou.node(node)

            node.setCurrent(True, clear_all_selected=True)

            _pane_tab = self.get_network_pane(node=node.parent())
            
            if _pane_tab is not None:
                _pane_tab.setCurrentNode(node)
                _pane_tab.homeToSelection()

                
    
    def import_file(self, filepath: str):
        """ ファイルをインポートする """
        # self.logger.info(f'JTP | Houdini | file = {filepath}')

        _network_path = self.get_current_network_path()
        _node = None
        _root_node = hou.node(_network_path)
        _name = self.optimize_name(pathlib.Path(filepath).stem)

        if os.path.exists(filepath):
            if self.is_usd(filepath):
                _node = self.import_usd(filepath, name=_name, network=_network_path, root_node=_root_node)

            elif self.is_vdb(filepath):
                _node = self.import_vdb(filepath, name=_name, network=_network_path, root_node=_root_node)

            elif self.is_hip(filepath):
                _node = self.import_hipfile(filepath)

            else:
                raise TypeError()
            

            if _node:
                _node.moveToGoodPosition()
                
                return _node
            
        else:
            raise FileNotFoundError()
        


    def import_hipfile(self, filepath: str):
        """ hipファイルを読み込み """

        _node = self.get_current_node()
        _node.loadItemsFromFile(filepath)



    def import_usd(self, filepath: str, name: str=None, network=None, root_node=None):
        """ USDファイルをインポートする """
        _node = None
        _node_type = root_node.type().name()
        _DISPLAY_FLAG = True


        if network is None:
            network_path = self.get_current_network_path()
            root_node = hou.node(network_path)
            _node_type = root_node.type().name()


        print(f'MDK | Houdini | {network=}')
        print(f'MDK | Houdini | {filepath=}')


        if _node_type == 'obj':
            _node = root_node.createNode('geo', name)
            _usd_node = _node.createNode('usdimport')
            _usd_node.parm('filepath1').set(filepath)
            _node.setDisplayFlag(_DISPLAY_FLAG)

        elif _node_type == 'geo':
            _node = root_node.createNode('usdimport')
            _node.parm('filepath1').set(filepath)
            _node.setDisplayFlag(_DISPLAY_FLAG)

        elif _node_type == 'stage' or _node_type == 'lopnet':
            _node = root_node.createNode('reference')
            _node.parm('filepath1').set(filepath)
            _node.setDisplayFlag(_DISPLAY_FLAG)


        return _node


    def import_vdb(self, filepath: str, name: str=None, network=None, root_node=None):
        _node = None
        _node_type = root_node.type().name()


        print(f'MDK | Houdini | {network=}')
        print(f'MDK | Houdini | {filepath=}')
        print(f'MDK | Houdini | node_type = {_node_type}')


        if _node_type == 'obj':
            _node = root_node.createNode('geo', name)
            _file_node = _node.createNode('file')
            _file_node.parm('file').set(filepath)
            _node.setDisplayFlag(False)

        
        elif _node_type == 'geo':
            _node = _node.createNode('file')
            _node.parm('file').set(filepath)
            _node.setDisplayFlag(False)


        elif _node_type == 'stage' or _node_type == 'lopnet':
            _node = root_node.createNode('volume', name)
            _node.parm('filepath1').set(filepath)
            _node.bypass(True)





    def is_hip(self, filepath: str):
        """ USDファイル判定 """
        return FILE_FILTER_HIP.match(filepath)


    def is_usd(self, filepath: str):
        """ USDファイル判定 """
        return FILE_FILTER_USD.match(filepath)


    def is_vdb(self, filepath: str):
        """ VDBファイル判定 """
        return FILE_FILTER_VBD.match(filepath)
    

    def open_dir(self):
        print('MDK | Open Dir')

        nodes = hou.selectedNodes()

        if len(nodes)==0:
            _filepath = hou.hipFile.path()
            _filepath.replace(':SDF_FORMAT_ARGS:format=usda', '')

            print(f'MDK | File = {_filepath}')
            
            if os.path.exists(_filepath):
                open_in_explorer(_filepath)

        else:
            for node in nodes:
                filepath_list = []
                node_type = node.type().name()

                print(f'MDK | Nodetype = {node_type}')

                if node_type in sorted(FILENODE_DICT):
                    key = FILENODE_DICT.get(node_type)
                    filepath_list.append(node.parm(key).eval())
                
                print(filepath_list)

                for _filepath in filepath_list:
                    _filepath = _filepath.replace(':SDF_FORMAT_ARGS:format=usda', '')
                    open_dir(_filepath)



        
    def optimize_name(self, value: str):
        return re.sub('[.]', '_', str(value))



    def save_selection(self, filepath: str):
        """ 選択しているノードを保存 """
        _root_node = self.get_current_node()
        _nodes = hou.selectedNodes()

        if not _root_node:
            raise ValueError('Not found root node.')
        
        if not _nodes:
            raise ValueError('No selected nodes.')


        _root_node.saveItemsToFile(_nodes, filepath)

