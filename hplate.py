import bpy
import math
import bmesh

bpy.ops.object.select_all(action='SELECT')

bpy.ops.object.delete()

# Parameters
length = 0.1  # Length of the surface in m
thickness = 0.0005  # Thickness of the surface in m
amplitude = 0.0026/2  # Amplitude of the sine wave

width = 0.03  # Length of the extension in m
extension_angle = math.radians(60)  # Angle of extension in radians
pitch = 100; #need to cjeck pitch calculation
#frequency = 1000  # Frequency of the sine wave
frequency = math.pi*2*pitch






# Create a new mesh and object
mesh = bpy.data.meshes.new("SinusoidalSurface")
obj = bpy.data.objects.new("SinusoidalSurface", mesh)

# Link the object to the scene
scene = bpy.context.scene
scene.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# Create a bmesh object to build the geometry
bm = bmesh.new()

# Generate vertices for the sinusoidal part
num_points = 1000  # Number of points along the X-axis
for i in range(num_points + 1):
    x = i * ((length*3) / num_points)
    y = 0  # Y-axis remains 0
    z = amplitude * math.sin(frequency * x)
    bm.verts.new((x, y, z))
    bm.verts.new((x, y, z + thickness))

# Ensure all vertices are added to the mesh
bm.verts.ensure_lookup_table()

# Generate faces for the sinusoidal part
for i in range(num_points):
    v1 = bm.verts[i * 2]
    v2 = bm.verts[i * 2 + 1]
    v3 = bm.verts[(i + 1) * 2]
    v4 = bm.verts[(i + 1) * 2 + 1]
    bm.faces.new((v1, v2, v4, v3))

# Finalize the bmesh and write to the mesh
bm.to_mesh(mesh)
bm.free()

# Update the mesh with new data
mesh.update()

# Switch to edit mode to perform extrusion
bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='EDIT')

# Select all faces
bpy.ops.mesh.select_all(action='SELECT')

# Calculate extrusion vector
extrude_vector = (
    (width*3) * math.cos(extension_angle),
    (width*3) * math.sin(extension_angle),
    0
)

# Perform the extrusion
bpy.ops.mesh.extrude_region_move(
    TRANSFORM_OT_translate={"value": extrude_vector}
)

# Switch back to object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Mirror the object
bpy.ops.object.duplicate_move(OBJECT_OT_duplicate=
{"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate=
{"value":(0, 0, 0), 
"orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1))})

bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False))

bpy.ops.object.select_all(action='SELECT')

bpy.ops.object.join()



#upper plate

#duplicate
bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1))})

#rotate
bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')

#move
bpy.ops.transform.translate(value=(length*3, 0, amplitude * 2 - 0.0001), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')


#add bounding box
bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(length/2, width, amplitude+0.01))

#move box
bpy.ops.transform.translate(value=(length*1.5, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')
