# 3D File Verification

## Overview
This library is designed to detect and verify various 3D file formats by analyzing their binary or text-based structures. It provides a basic pre-scan to ensure the file type is as expected before further processing or use (such as potential malware injection). This helps prevent errors, ensures compatibility, and adds a basic security layer by preventing incorrect or potentially harmful files from being processed.

## Supported File Types

### 1. **STL (Stereolithography)**
   - **Binary STL**
     - Identified by an 80-byte header followed by a 4-byte unsigned integer indicating the number of triangles.
     - The expected file size is calculated as: `header_size + (50 * num_triangles)` bytes.
        **why 50?**
        - 12 bytes → 3 normal vector floats (float32 × 3)
        - 36 bytes → 3 vertices (float32 × 9)
        - 2 bytes → Attribute byte count
     - Detection method: Read the first 80 bytes, verify format, and check the expected file size.

returns ```is_valid: bool, mesage: str, triangle_count: int```

*in the case of an error, triangle_count = 0*

   - **ASCII STL**
     - Starts with the keyword `solid` followed by the model name.
     - Contains lines with `facet`, `vertex`, and `endfacet` keywords.
     - Detection method: Read the first few lines and confirm the presence of expected keywords.

returns ```is_valid:bool```

### 2. **OBJ (Wavefront OBJ)**
   - Plain text format, human-readable.
   - Uses keywords such as `v` (vertex), `vn` (vertex normal), `vt` (texture coordinate), `f` (face), and `usemtl` (material usage).
   - Detection method: Scan the first few lines and ensure at least one of the key OBJ-related keywords is present.

### 3. **3MF (3D Manufacturing Format)** (future)
   - <None>

### 4. **STEP ()** (future)
   - <None>

### 5. **3DS ()** (future)
   - <None>

### 5. **IGES ()** (future)
   - <None>
   
   
## How Detection Works
The library follows a structured detection process:
1. ClamAV to scan files for general malware
2. **DoS** specific vulnerablilities 
   - **File Size Verification** (Ensures file is not empty or corrupted)
   - **Binary Signature Analysis** (For binary STL)
     
   - **Keyword Matching** (For text-based OBJ and ASCII STL)
   - **Archive & XML Validation** (For 3MF)

## Security & Safety Considerations
- **Basic Pre-Scan Protection**
  - Helps ensures the file is what it claims to be before processing.
  - Helps prevent incorrect file types from being loaded into a 3D application.
  
- **Potential Security Risks Mitigated**
  - Detects malformed or incomplete files.
  - Reduces risk of certain attack vectors e.g.
     - malformed 3MF files attempting to exploit XML parsing vulnerabilities
     - memory over flow for STLs, OBJs
  - Can be extended to include additional validation, such as checking for overly large files that may cause memory issues.

## Example Usage
```python
None
```

## Possible Improvements
- **Checksum validation** to detect file corruption.
- **Support for detecting specific errors** (malware, or file error).
- **Deeper security scans** (e.g., sandboxing for XML parsing in 3MF files).
- **more file type supports**

<br></br>

<br></br>

<br></br>

<br></br>

<br></br>

<br></br>
