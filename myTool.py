import bpy

class myTool(bpy.types.Panel):
    bl_label = "myTool"
    bl_idname = "dyTool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "myTool"
    
    def draw(self, context):
        layout = self.layout
#        row = layout.row()
        layout.operator(AddFingerControl.bl_idname)
        layout.operator(AddLegIk.bl_idname)
        layout.operator(AddArmIk.bl_idname)


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

# model face to +Y axis
class AddLegIk(bpy.types.Operator):
    
    bl_idname = "bone.leg_ik"
    bl_label = 'Add Leg Ik(face+Y)'
    
    def execute(self, context):
        obj = bpy.context.object
        if (obj.mode == "POSE"):
            bone = bpy.context.active_pose_bone
            if bone:
                # create ik bone
                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                edit_bones = obj.data.edit_bones
                ik_bone_name = bone.name + '.ik'
                ik_bone = edit_bones.new(ik_bone_name)
                ik_bone.head = bone.tail
                ik_bone.tail = (bone.tail.x, bone.tail.y+0.3, bone.tail.z)
                
                # create pole bone
                #bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                pole_bone = edit_bones.new(bone.name + '.pole')
                pole_bone.head = (bone.head.x, bone.head.y+1.0, bone.head.z)
                pole_bone.tail = (bone.head.x, bone.head.y+1.3, bone.head.z)
                bpy.ops.object.mode_set(mode='POSE')
                #bpy.ops.object.mode_set(mode='POSE')
                if not [c for c in bone.constraints if c.type=='IK']:
                    bone.constraints.new('IK')
                crc = bone.constraints["IK"]
                crc.target = obj
                crc.subtarget = ik_bone_name
                crc.chain_count = 2
                crc.pole_target = obj
                crc.pole_angle = 1.5708
                crc.pole_subtarget = pole_bone.name
        return {'FINISHED'}

# model face to +Y axis
class AddArmIk(bpy.types.Operator):
    
    bl_idname = "bone.arm_ik"
    bl_label = 'Add Arm Ik(face+Y&Tpose)'
    
    def execute(self, context):
        obj = bpy.context.object
        if (obj.mode == "POSE"):
            bone = bpy.context.active_pose_bone
            if bone:
                # create ik bone
                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                edit_bones = obj.data.edit_bones
                ik_bone_name = bone.name + '.ik'
                ik_bone = edit_bones.new(ik_bone_name)
                ik_bone.head = bone.tail
                ik_bone.tail = (bone.tail.x, bone.tail.y+0.3, bone.tail.z)
                
                # create pole bone
                #bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                pole_bone_name = bone.name + '.pole'
                pole_bone = edit_bones.new(pole_bone_name)
                pole_bone.head = (bone.head.x, bone.head.y-1.0, bone.head.z)
                pole_bone.tail = (bone.head.x, bone.head.y-1.3, bone.head.z)
                bpy.ops.object.mode_set(mode='POSE')
                #bpy.ops.object.mode_set(mode='POSE')
                if not [c for c in bone.constraints if c.type=='IK']:
                    bone.constraints.new('IK')
                crc = bone.constraints["IK"]
                crc.target = obj
                crc.subtarget = ik_bone_name
                crc.chain_count = 2
                crc.pole_target = obj
                crc.pole_angle = -1.5708
                crc.pole_subtarget = pole_bone_name
        return {'FINISHED'}

def register():
    bpy.utils.register_class(myTool)
    bpy.utils.register_class(AddFingerControl)
    bpy.utils.register_class(AddLegIk)
    bpy.utils.register_class(AddArmIk)

if __name__ == "__main__":
    register()
