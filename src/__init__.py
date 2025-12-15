""" mdkapps
 
* VFX用 APP互換 Pythonパッケージ

Info:
    * Created : v0.1.0 2025-08-12 Tatsuya Yamagishi
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.2.0 2025-12-15 Tatsuya Yamagishi
        * improved: DCC自動判別ロジックを改善

    * v0.1.0 2025-08-12 Tatsuya Yamagishi
        * Changed : メジャーアップデート
            * 関数メインの構成に変更
"""

VERSION = 'v0.2.0'
NAME = 'mdk_apps'

import os
import sys


if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdkapps package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')


try:
   """ Import Blender """
   import bpy
   print('MDK | Successfully imported Blender Python API bpy')
   from .mdk_b3d import *

# except Exception as ex:
#     raise RuntimeError(ex)

except ImportError:
    try:
        """ Improt Cinema4D """
        import c4d
        from .mdk_c4d import *

        print('MDK | Successfully imported Cinema4D Python API c4d')

    except ImportError:
        try:
            """ Improt Houdini """
            import hou
            from .mdk_houdini import *
            print('MDK | Successfully imported Hoduini Python API hou')

        except ImportError:
            try:
                """ Improt Max """
                import pymxs
                from .mdk_max import *
                print('MDK | Successfully imported 3dsMax Python API pymxs')

            except ImportError:
                try:
                    """ Improt Maya """
                    import maya.cmds as cmds
                    from .mdk_maya import *
                    print('MDK | Successfully imported Maya Python API maya.cmds')

                except ImportError:
                    try:
                        """ Improt nuke """
                        import nuke
                        from .mdk_nuke import *
                        print('MDK | Successfully imported Nuke Python API nuke')

                    except ImportError:
                        try:
                            """ Improt standalone """
                            from .mdk_standalone import *
                            print('MDK | Successfully imported Python API standalone')
                        except ImportError:
                            print("Failed to import all libraries. Please check your environment.")

# """mdkapps

# VFX 用 APP 互換 Python パッケージ
# """

# from __future__ import annotations

# import os
# import importlib
# from typing import Callable

# VERSION = "v0.1.0"
# NAME = "mdk_apps"

# DEBUG = bool(os.environ.get("MDK_DEBUG"))


# def _debug(msg: str) -> None:
#     if DEBUG:
#         print(f"MDK | {msg}")


# _debug("---------------------------")
# _debug("[ import mdkapps package ]")
# _debug(f"{NAME} {VERSION}")
# _debug("---------------------------")


# # DCC 定義テーブル
# _DCC_IMPORTS: list[tuple[str, str, str]] = [
#     ("bpy", "mdk_b3d", "Blender"),
#     ("c4d", "mdk_c4d", "Cinema4D"),
#     ("hou", "mdk_houdini", "Houdini"),
#     ("pymxs", "mdk_max", "3dsMax"),
#     ("maya.cmds", "mdk_maya", "Maya"),
#     ("nuke", "mdk_nuke", "Nuke"),
# ]


# def _try_import_dcc():
#     for api_name, module_name, label in _DCC_IMPORTS:
#         try:
#             importlib.import_module(api_name)
#             module = importlib.import_module(f".{module_name}", __package__)
#             _debug(f"Successfully imported {label} API")
#             return module
#         except ImportError:
#             continue

#     # fallback
#     _debug("Using standalone environment")
#     return importlib.import_module(".mdk_standalone", __package__)


# # 実行
# _backend = _try_import_dcc()

# # 公開API（明示）
# __all__ = getattr(_backend, "__all__", [])
# globals().update(
#     {name: getattr(_backend, name) for name in __all__}
# )