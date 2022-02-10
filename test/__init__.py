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
    "name" : "Blender Plugin",
    "author" : "Ciara Daly",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 3),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

import bpy

from . plugin_op import ButtonOperator
from . plugin_pnl import OBJECT_PT_MyPanel

classes = (ButtonOperator, OBJECT_PT_MyPanel)
def register():
    for c  in classes:
        bpy.utils.register_class(c)

def unregister():
    for c  in classes:
        bpy.utils.unregister_class(c)
