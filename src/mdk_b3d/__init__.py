""" mdk_b3d
 
* VFX用Blender互換パッケージ

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya YAMAGISHI
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.1 2024-11-15 Tatsuya Yamagishi
        * added: path
"""

VERSION = 'v0.0.1'
NAME = 'mdk_b3d'

import os
import pathlib
import platform
import re
import subprocess
import sys


import bpy


if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdk_b3d package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')



#=======================================#
# Settings
#=======================================#
FILE_FILTER_USD = re.compile(r'.+\.(usd|usdc|usda)')

EXT_LIST = [
    '.b3d',
    '.abc',
    '.fbx',
    '.obj',
    '.usd',
]


EXT_DICT = {
    'asset': '.b3d',
    'geo': '.abc',
    'shot': '.b3d',
    'usd': '.usd',
}

SCRIPT_EXTS = ['.py']


# ======================================= #
# Decorators
# ======================================= #
def context_window(func):
    """
    Reference from : https://blender.stackexchange.com/questions/269960/bpy-context-object-changes-within-pyside2-button-callback
    
    Support running operators from QT (ex. on button click).
    Decorator to override the context window for a function,
    """
    def wrapper(*args, **kwargs):
        with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
            return func(*args, **kwargs)

    return wrapper


# ======================================= #
# Get
# ======================================= #
def get_ext() -> str:
    return '.b3d'

def get_ext_list() -> list[str]:
    """ 拡張子リストを返す"""
    return list(EXT_LIST)

def get_filepath() -> str:
    """現在開いているファイルパスを取得"""
    return bpy.context.blend_data.filepath

def get_selected_nodes() -> list:
    """ 選択しているノードを取得
   
    Returns:
        list: 選択しているノードリスト
    """
    return bpy.context.selected_objects

def get_script_exts() -> list[str]:
    """ スクリプト拡張子リストを取得
    
    Returns:
        list[str]: スクリプト拡張子リスト
    """
    return SCRIPT_EXTS

# ======================================= #
# Functions
# ======================================= #
def create_playblast(filepath: str, size: list|tuple=None, range: list|tuple=None, filetype='jpg'):
    """ プレイブラストを作成
    
    Args:
        filepath(str): 出力ファイルパス
        size(list | turple): サイズ
        range(list | turple): サイズ
    """

    raise RuntimeError('未実装')




@context_window
def import_usd(filepath: str, scale: float = 0.01):
    """ USDファイルをインポート

    Reference from:

    * https://devtalk.blender.org/t/issue-with-importing-usd-files-via-bpy-ops-wm-usd-import-and-python/26152

    bpy.ops.wm.usd_import(
        filepath=self.file_path, 
        import_cameras=True, 
        import_curves=True, 
        import_lights=True, 
        import_materials=True, 
        import_meshes=True, 
        import_volumes=True, 
        scale=1.0, 
        read_mesh_uvs=True, 
        read_mesh_colors=False, 
        import_subdiv=False, 
        import_instance_proxies=True, 
        import_visible_only=True,
        import_guide=False,
        import_proxy=True,
        import_render=True,
        set_frame_range=True,
        relative_path=True,
        create_collection=False,
        light_intensity_scale=1.0,
        mtl_name_collision_mode='MAKE_UNIQUE',
        import_usd_preview=True,
        set_material_blend=True)
    """
    # _override = get_override_context()

    bpy.ops.wm.usd_import(
            # _override,
            filepath=filepath,
            scale=scale,)


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


@context_window
def save_file(filepath, context=False):
    """ ファイルを保存
    Args:
        filepath (str): 保存するファイルパス
        context (bool): コンテキストを使用するかどうか
    """
    if context:
        _override = bpy.context.copy()
        _override['blend_data'] = bpy.data

        bpy.ops.wm.save_as_mainfile(_override, filepath=filepath)

    else:
        bpy.ops.wm.save_as_mainfile(filepath=filepath)



@context_window
def set_current_time(value: int):
    """ 現在のフレームをセット
    Args:
        value (int): フレーム番号
    """
    # print(f'MDK | current_time = {value}')
    bpy.context.scene.frame_current = int(value)


@context_window
def set_fps(value: int):
    """ FPSをセット 
    Args:
        value (int): FPS値
    """
    print(f'MDK | fps = {value}')

    if type(value) is int:
        bpy.context.scene.render.fps = int(value)
    elif type(value) is float:
        raise TypeError('FPS must be int or float')


@context_window
def set_frame_range(start: int, end: int) -> None:
    """ フレームレンジをセット """
    print(f'MDK | frame_range = {start} - {end}')

    bpy.context.scene.frame_start = int(start)
    bpy.context.scene.frame_end = int(end)

    # bpy.context.scene.frame_preview_start = 10
    # bpy.context.scene.frame_preview_end = 100

    # bpy.ops.action.view_all()


def set_render_frame_range(first: int, last: int):
    """ レンダーフレームレンジをセット 
    Blenderではレンダーフレームレンジはシーンのフレームレンジと同じになるため、シーンのフレームレンジをセットする

    """
    print(f'MDK | render_frame_range = {first} - {last}')
    print('Blender render frame range is fixed to scene frame range')


@context_window
def set_render_size(width: int, height: int) -> None:
    """ レンダーサイズをセット 
    Args:
        width (int): 幅
        height (int): 高さ
    """
    print(f'MDK | render_size = {width}x{height}')
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.resolution_percentage = 100

def set_renderer(value: str):
    """ レンダラーをセット """
    print(f'MDK | renderer = {value}')

def set_unit(value: str):
    """ 単位をセット """
    print(f'MDK | unit = {value}')


# ======================================= #
# Class
# ======================================= #
# class AppMain:
#     def __init__(self):
#         pass

#     def get_ext(self, key: str = None) -> str:
#         return '.b3d'

#     def get_ext_list(self):
#         """ 拡張子リストを返す"""
#         return list(EXT_LIST)
    

#     def get_filepath(self) -> str:
#         return bpy.context.blend_data.filepath


#     def get_framerange(self):
#         """ フレームレンジを取得
#         """
#         _start_frame = bpy.context.scene.frame_start
#         _end_frame = bpy.context.scene.frame_end
#         return _start_frame, _start_frame, _end_frame, _end_frame
    

#     def get_selected_nodes(self):
#         """ 選択中のオブジェクトをリストとして取得 
#         # selected_objects = bpy.context.selected_objects
#         # selected_objects = plugin.context.selected_objects
#         """
#         return [_obj for _obj in bpy.context.scene.objects if _obj.select_get() ] 
    

#     @context_window
#     def import_abc(self, filepath: str):
#         """
        
#         """
#         bpy.ops.wm.alembic_import(filepath=filepath)

#     def import_file(self, filepath: str):
#         """ ファイルをインポート
#         """
#         if self.is_usd(filepath):
#             self.import_usd(filepath)
#         elif self.is_abc(filepath):
#             self.import_abc(filepath)

#     def import_files(self, filepath_list: list[str], namespace=None):
#         for _filepath in filepath_list:
#             self.import_file(_filepath, namespace=namespace)


#     @context_window
#     def import_usd(self, filepath: str, scale: float = 0.01):
#         """ USDファイルをインポート

#         Reference from:

#         * https://devtalk.blender.org/t/issue-with-importing-usd-files-via-bpy-ops-wm-usd-import-and-python/26152

#         bpy.ops.wm.usd_import(
#             filepath=self.file_path, 
#             import_cameras=True, 
#             import_curves=True, 
#             import_lights=True, 
#             import_materials=True, 
#             import_meshes=True, 
#             import_volumes=True, 
#             scale=1.0, 
#             read_mesh_uvs=True, 
#             read_mesh_colors=False, 
#             import_subdiv=False, 
#             import_instance_proxies=True, 
#             import_visible_only=True,
#             import_guide=False,
#             import_proxy=True,
#             import_render=True,
#             set_frame_range=True,
#             relative_path=True,
#             create_collection=False,
#             light_intensity_scale=1.0,
#             mtl_name_collision_mode='MAKE_UNIQUE',
#             import_usd_preview=True,
#             set_material_blend=True)
#         """
#         # _override = get_override_context()

#         bpy.ops.wm.usd_import(
#                 # _override,
#                 filepath=filepath,
#                 scale=scale,)


#     def is_usd(self, filepath: str) -> tuple:
#         """ USDファイル判定 """
#         return FILE_FILTER_USD.match(filepath)
    

    

#     def open_dir(self):
#         """ Plugin Builtin Function """
#         _nodes = self.get_selected_nodes()

#         if _nodes:
#             raise NotImplementedError('未実装')
#         else:
#             _filepath = self.get_filepath()
#             open_dir(_filepath)

#     def open_file(self, filepath, recent=False):
#         """ Plugin Builtin Function """
#         bpy.ops.wm.open_mainfile(filepath=filepath)  
    

#     @context_window
#     def save_file(self, filepath, context=False):
#         if context:
#             _override = bpy.context.copy()
#             _override['blend_data'] = bpy.data

#             bpy.ops.wm.save_as_mainfile(_override, filepath=filepath)

#         else:
#             bpy.ops.wm.save_as_mainfile(filepath=filepath)