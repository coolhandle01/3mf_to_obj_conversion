# 3mf_to_obj_conversion
Turns out 3mf files store information in a layered structure. I needed the individual components of the kidney and in obj format. The script extracts the constituents of the 3mf file and saves them in obj format



----------------------------------------------------------------------------------------------------------------------------------------------------------
# 3MF to OBJ Converter

A Python script that extracts 3D mesh components from 3MF files and converts them to individual OBJ files.

## Overview

This tool parses 3MF (3D Manufacturing Format) files, extracts each mesh object component, and saves them as separate OBJ (Wavefront) files. 3MF files are essentially ZIP archives containing XML descriptions of 3D models, and this script handles the extraction and conversion process automatically.

## Requirements

- Python 3.x
- Standard Python libraries (no external dependencies required):
  - `zipfile`
  - `xml.etree.ElementTree`
  - `os`
  - `re`
  - `shutil`

## Installation

1. Download the script `extract_3mf_components.py`
2. Ensure Python 3.x is installed on your system
3. No additional package installation required

## Usage

```python
from extract_3mf_components import extract_3mf_components_simple

# Extract components from a 3MF file
extract_3mf_components_simple(
    input_file="/path/to/your/file.3mf",
    output_dir="/path/to/output/directory"
)
```

### Command Line Usage

```python
# Example usage
extract_3mf_components_simple(
    "/link_to_3mf_file", 
    "folder_for_storing_extracted_files"
)
```

## Function Parameters

- `input_file`: Path to the input 3MF file
- `output_dir`: Directory where the extracted OBJ files will be saved

## How It Works

1. **Extract 3MF Archive**: The script unzips the 3MF file to a temporary directory
2. **Parse XML**: Reads the `3D/3dmodel.model` XML file from the extracted contents
3. **Extract Components**: For each mesh object found:
   - Extracts vertex coordinates (x, y, z)
   - Extracts triangle face definitions (vertex indices)
   - Saves as an individual OBJ file
4. **Clean Up**: Removes temporary extraction directory

## Output

- Creates individual OBJ files named `kidney_part_1.obj`, `kidney_part_2.obj`, etc.
- Each OBJ file contains:
  - Vertex data (v lines)
  - Face data (f lines)
- Console output shows progress and file locations

## Features

- Automatic namespace detection for XML parsing
- Handles multiple mesh objects in a single 3MF file
- Creates output directory if it doesn't exist
- Cleans up temporary files after extraction
- Provides console feedback during processing

## Error Handling

The script includes basic error handling:
- Skips objects without mesh data
- Skips meshes without vertices or triangles
- Uses default values (0) for missing coordinates

## Limitations

- Only extracts mesh geometry (vertices and faces)
- Does not preserve:
  - Materials
  - Colors
  - Textures
  - Transforms
  - Other 3MF-specific metadata
- OBJ vertex indices are 1-based (converted from 0-based in 3MF)

## Example Console Output

```
Saved component 1 to /path/to/output/kidney_part_1.obj
Saved component 2 to /path/to/output/kidney_part_2.obj
Saved component 3 to /path/to/output/kidney_part_3.obj
Extracted 3 components from /path/to/input/file.3mf
```

## Notes

- The script is designed for medical/anatomical models (hence the "kidney" naming convention)
- To use with other types of 3D models, you may want to modify the output naming scheme
- The temporary extraction directory is created at `{output_dir}/temp`





## Version

1.0.0

## Changelog

- Initial release: Basic 3MF to OBJ extraction functionality