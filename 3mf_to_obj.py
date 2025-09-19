import zipfile
import xml.etree.ElementTree as ET
import os
import re

def extract_3mf_components_simple(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Extract the 3MF file (it's a ZIP archive)
    with zipfile.ZipFile(input_file, 'r') as zip_ref:
        zip_ref.extractall(output_dir + '/temp')
    
    # Parse the 3D model XML file
    tree = ET.parse(output_dir + '/temp/3D/3dmodel.model')
    root = tree.getroot()
    
    # Find the namespace
    ns_match = re.match(r'{.*}', root.tag)
    namespace = ns_match.group(0) if ns_match else ""
    
    # Extract each mesh colorgroup
    color_palette = {}
    namespaces = {
        '': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02',
        'm': 'http://schemas.microsoft.com/3dmanufacturing/material/2015/02'
    }
    resources = root.find('resources', namespaces)

    if resources is not None:
        for m_colorgroup in resources.findall("m:colorgroup", namespaces):
            palette_id = int(m_colorgroup.get('id', '-1'))
            color_palette[palette_id] = []
            for m_color in m_colorgroup.findall("m:color", namespaces):
                color = m_color.get('color', '#FFFFFFFF').lstrip('#')
                r = int(color[0:2], 16) / 255.0
                g = int(color[2:4], 16) / 255.0
                b = int(color[4:6], 16) / 255.0
                a = int(color[6:8], 16) / 255.0
                color_palette[palette_id].append((r, g, b))

    # Extract each mesh object
    count = 0
    for obj in root.findall(f".//{namespace}object"):
        count += 1
        mesh = obj.find(f".//{namespace}mesh")
        name = obj.get('name', 'kidney_part')
        
        if mesh is None:
            continue
            
        vertices_elem = mesh.find(f".//{namespace}vertices")
        triangles_elem = mesh.find(f".//{namespace}triangles")
        
        if vertices_elem is None or triangles_elem is None:
            continue
            
        # Extract vertices
        vertices = []
        colors = []
        for vertex in vertices_elem.findall(f".//{namespace}vertex"):
            x = float(vertex.get('x', 0))
            y = float(vertex.get('y', 0))
            z = float(vertex.get('z', 0))
            vertices.append((x, y, z))
            colors.append((1.0, 1.0, 1.0)) # default color
            
        # Extract triangles
        triangles = []
        for triangle in triangles_elem.findall(f".//{namespace}triangle"):
            v1 = int(triangle.get('v1', 0))
            v2 = int(triangle.get('v2', 0))
            v3 = int(triangle.get('v3', 0))
            triangles.append((v1, v2, v3))

            palette_id = triangle.get('pid')
            if palette_id is not None:
                p1 = triangle.get('p1')
                p2 = triangle.get('p2')
                p3 = triangle.get('p3')
                if p1 is not None and p2 is not None and p3 is not None:
                    colors[v1]=color_palette[int(palette_id)][int(p1)]
                    colors[v2]=color_palette[int(palette_id)][int(p2)]
                    colors[v3]=color_palette[int(palette_id)][int(p3)]
            
        # Write OBJ file
        output_file = os.path.join(output_dir, f"{name}_{count}.obj")
        with open(output_file, 'w') as f:
            for i, v in enumerate(vertices):
                rgb = colors[i] 
                f.write(f"v {v[0]} {v[1]} {v[2]} {rgb[0]} {rgb[1]} {rgb[2]}\n")
                
            for t in triangles:
                f.write(f"f {t[0]+1} {t[1]+1} {t[2]+1}\n")
                
        print(f"Saved component {count} to {output_file}")
    
    # Clean up temporary files
    import shutil
    shutil.rmtree(output_dir + '/temp')
    
    print(f"Extracted {count} components from {input_file}")

# include the 3mf file, a directory to save the extracted component
extract_3mf_components_simple("link_to_3mf_file", "folder_for_storing_extracted_files")