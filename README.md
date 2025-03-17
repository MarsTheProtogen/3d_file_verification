# 3D File Verification

## Overview
This library is designed to detect and verify various 3D file formats by analyzing their binary or text-based structures. It provides a basic pre-scan to ensure the file type is as expected before further processing or use. This helps prevent errors, ensures compatibility, and adds a basic security layer by preventing incorrect or potentially harmful files from being processed.

## Supported File Types

### 1. **STL (Stereolithography)**
   - **Binary STL**
     - Identified by an 80-byte header followed by a 4-byte unsigned integer indicating the number of triangles.
     - The expected file size is calculated as: `84 + (50 * num_triangles)` bytes.
     - Detection method: Read the first 80 bytes, verify format, and check the expected file size.
   
   - **ASCII STL**
     - Starts with the keyword `solid` followed by the model name.
     - Contains lines with `facet`, `vertex`, and `endfacet` keywords.
     - Detection method: Read the first few lines and confirm the presence of expected keywords.

### 2. **OBJ (Wavefront OBJ)**
   - Plain text format, human-readable.
   - Uses keywords such as `v` (vertex), `vn` (vertex normal), `vt` (texture coordinate), `f` (face), and `usemtl` (material usage).
   - Detection method: Scan the first few lines and ensure at least one of the key OBJ-related keywords is present.

### 3. **3MF (3D Manufacturing Format)**
   - Compressed ZIP archive containing XML files.
   - Key file: `[Content_Types].xml` which must include an entry for `application/vnd.ms-package.3dmanufacturing-3dmodel+xml`.
   - Detection method: Verify that the file is a ZIP archive and check for the existence and contents of `[Content_Types].xml`.

## How Detection Works
The library follows a structured detection process:
1. **File Extension Check** (Optional, but useful as a first filter)
2. **File Size Verification** (Ensures file is not empty or corrupted)
3. **Binary Signature Analysis** (For binary STL)
4. **Keyword Matching** (For text-based OBJ and ASCII STL)
5. **Archive & XML Validation** (For 3MF)

## Security & Safety Considerations
- **Basic Pre-Scan Protection**
  - Ensures the file is what it claims to be before processing.
  - Helps prevent incorrect file types from being loaded into a 3D application.
  
- **Potential Security Risks Mitigated**
  - Detects malformed or incomplete files.
  - Reduces risk of certain attack vectors (e.g., malformed 3MF files attempting to exploit XML parsing vulnerabilities).
  - Can be extended to include additional validation, such as checking for overly large files that may cause memory issues.

## Example Usage
```python
from file_detector import detect_3d_file

file_path = "model.stl"
valid, message = detect_3d_file(file_path)
print(valid, message)
```

## Future Improvements
- **Checksum validation** to detect file corruption.
- **Support for more formats** (e.g., PLY, glTF, AMF).
- **Deeper security scans** (e.g., sandboxing for XML parsing in 3MF files).

## Conclusion
This library provides a fast and effective way to detect common 3D file formats before further processing. It serves as an essential first step in verifying file integrity and ensuring safety in 3D modeling workflows.

