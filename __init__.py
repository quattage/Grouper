# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Grouper",
    "author": "quattage",
    "description": "Automatically groups collections and sorts objects for baking",
    "blender": (3, 00, 0),
    "version": (0, 0, 1),
    "location": "View3D > Sidebar > Grouper Tab",
    "warning": "",
    "category": "Object"
}

import importlib
import bpy
import os

from bpy.props import IntProperty
from bpy.app.handlers import persistent

from .panel import GROUPER_PT_OpsPanel
from .panel import GROUPER_UL_MDViewer
from .panel import GROUPER_PT_EnumsPanel
from .preferences import GROUPER_PT_PrefsPanel
from .preferences import GROUPER_PT_PrefsProperties, GROUPER_PT_MDList, GROUPER_PT_GDList
from .utils.logger import logger


GROUPER_Misc = [
    GROUPER_PT_OpsPanel,
    GROUPER_PT_PrefsPanel,
    GROUPER_PT_EnumsPanel,
    GROUPER_UL_MDViewer
]


GROUPER_OpsProperties = (
    ('poly_midpoint', bpy.props.IntProperty(name='Mid', default=10000, description="Midpoint in tris. Anything above this triangle count will be considered high-poly and anything below it will be considered low-poly")),
)


def register():
    logger.enable()
    register_modules("operators", "LOAD")
    register_props("LOAD")
    register_pointers("LOAD")
    register_misc("LOAD")
    bpy.app.handlers.load_post.append(load_handler)
    bpy.app.handlers.load_factory_startup_post.append(load_startup_handler)
    logger.log("MODULES REGISTERED", "REGISTRY")


@persistent
def load_handler(dummy):
    bpy.ops.grouper.register_defaults()


def load_startup_handler(dummy):
    bpy.ops.grouper.register_defaults()


def unregister():
    register_modules("operators", "UNLOAD")
    register_props("UNLOAD")
    register_pointers("UNLOAD")
    register_misc("UNLOAD")
    logger.log("MODULES UNREGISTERED", "REGISTRY")
    

def register_pointers(operation: str = "LOAD"):
    if operation == "LOAD":
        logger.log("Added " + GROUPER_PT_PrefsProperties.__name__ + " as PointerProperty to bpy.types.scene", "REGISTRY")
        bpy.utils.register_class(GROUPER_PT_PrefsProperties)
        bpy.types.Scene.grouper_prefs = bpy.props.PointerProperty(type=GROUPER_PT_PrefsProperties)
        bpy.utils.register_class(GROUPER_PT_MDList)
        bpy.types.Scene.grouper_mdlist = bpy.props.CollectionProperty(type=GROUPER_PT_MDList)
        bpy.utils.register_class(GROUPER_PT_GDList)
        bpy.types.Scene.grouper_gdlist = bpy.props.CollectionProperty(type=GROUPER_PT_GDList)

    elif operation == "UNLOAD":
        try:
            bpy.utils.unregister_class(GROUPER_PT_PrefsProperties)
            del bpy.types.Scene.GROUPER_PT_PrefsProperties
        except:
            pass
        try:
            bpy.utils.unregister_class(GROUPER_PT_MDList)
            del bpy.types.Scene.GROUPER_PT_MDList
        except:
            pass
        try:
            bpy.utils.unregister_class(GROUPER_PT_GDList)
            del bpy.types.Scene.GROUPER_PT_GDList
        except:
            pass
        


def register_misc(operation: str = "LOAD"):
    for thiscls in GROUPER_Misc:
        if operation == "LOAD":
            bpy.utils.register_class(thiscls)
        elif operation == "UNLOAD":
            bpy.utils.unregister_class(thiscls)


def register_props(operation: str = "LOAD"):
    for name, value in GROUPER_OpsProperties:
        if operation == "LOAD":
            setattr(bpy.types.Scene, name, value)
        elif operation == "UNLOAD":
            delattr(bpy.types.Scene, name)


def register_modules(sub: str, operation: str = "LOAD"):
        #brace yourself
        modules_list = sorted([name[:-3] for name in os.listdir(os.path.join(__path__[0], sub)) if name.endswith('.py')])
        for module in modules_list:            
            impexec = "from ." + sub + " import " + module
            exec(impexec)
            importlib.reload(eval(module))        # i am very sorry
            class_to_load = eval(module).op_class
            if operation == "LOAD":
                logger.log("Loading " + __name__ + "/" + sub + "/" + module + ".py/" + class_to_load.__name__ + ".class", "REGISTRY")
                bpy.utils.register_class(class_to_load)
            elif operation == "UNLOAD":
                logger.log("Unloading " + __name__ + "/" + sub + "/" + module + ".py/" + class_to_load.__name__ + ".class", "REGISTRY")
                try:
                    bpy.utils.unregister_class(class_to_load)
                except RuntimeError:
                    pass
