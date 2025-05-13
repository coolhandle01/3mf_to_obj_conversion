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
    
    # Extract each mesh object
    count = 0
    for obj in root.findall(f".//{namespace}object"):
        count += 1
        mesh = obj.find(f".//{namespace}mesh")
        
        if mesh is None:
            continue
            
        vertices_elem = mesh.find(f".//{namespace}vertices")
        triangles_elem = mesh.find(f".//{namespace}triangles")
        
        if vertices_elem is None or triangles_elem is None:
            continue
            
        # Extract vertices
        vertices = []
        for vertex in vertices_elem.findall(f".//{namespace}vertex"):
            x = float(vertex.get('x', 0))
            y = float(vertex.get('y', 0))
            z = float(vertex.get('z', 0))
            vertices.append((x, y, z))
            
        # Extract triangles
        triangles = []
        for triangle in triangles_elem.findall(f".//{namespace}triangle"):
            v1 = int(triangle.get('v1', 0))
            v2 = int(triangle.get('v2', 0))
            v3 = int(triangle.get('v3', 0))
            triangles.append((v1, v2, v3))
            
        # Write OBJ file
        output_file = os.path.join(output_dir, f"kidney_part_{count}.obj")
        with open(output_file, 'w') as f:
            for v in vertices:
                f.write(f"v {v[0]} {v[1]} {v[2]}\n")
                
            for t in triangles:
                f.write(f"f {t[0]+1} {t[1]+1} {t[2]+1}\n")
                
        print(f"Saved component {count} to {output_file}")
    
    # Clean up temporary files
    import shutil
    shutil.rmtree(output_dir + '/temp')
    
    print(f"Extracted {count} components from {input_file}")

# include the 3mf file, a directory to save the extracted component
extract_3mf_components_simple("link_to_3mf_file", "folder_for_storing_extracted_files")