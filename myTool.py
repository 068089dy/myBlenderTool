import bpy

class myTool(bpy.types.Panel):
    bl_label = "myTool"
    bl_idname = "dyTool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "myTool"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator(AddFingerControl.bl_idname)

# 手指控制
class AddFingerControl(bpy.types.Operator):
    bl_idname = "bone.finger_control"
    bl_label = 'Add Finger Control'
    
    def execute(self, context):
        obj = bpy.context.object
        if (obj.mode == "POSE"):
            bone = bpy.context.active_pose_bone
            if bone:
                if not [c for c in bone.constraints if c.type=='LIMIT_ROTATION']:
                    crc = bone.constraints.new('LIMIT_ROTATION')
                crc = bone.constraints["Limit Rotation"]
                crc.use_limit_x = True
                crc.use_limit_y = True
                crc.use_limit_z = True
                crc.max_x = 1.5708
                while bone.child:
                    bone = bone.child
                    print(bone.bone)
                    if not [c for c in bone.constraints if c.type=='COPY_ROTATION']:
#                        bpy.ops.pose.constraint_add(type="COPY_ROTATION")
                        bone.constraints.new('COPY_ROTATION')
                    crc = bone.constraints["Copy Rotation"]
                    crc.target_space = 'LOCAL'
                    crc.owner_space = 'LOCAL'
                    crc.target = obj
                    crc.use_y = False
                    crc.use_z = False
                    crc.subtarget = bone.parent.name
#                bpy.context.object.pose.bones["Bone"].constraints["Copy Rotation"].target_space = 'LOCAL'
#                bpy.context.object.pose.bones["Bone"].constraints["Copy Rotation"].target_space = 'LOCAL'
        return {'FINISHED'}


def register():
    bpy.utils.register_class(myTool)
    bpy.utils.register_class(AddFingerControl)

if __name__ == "__main__":
    register()
            
