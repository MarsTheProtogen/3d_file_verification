# 3D File Verification

## Overview
This library is designed to detect and verify various 3D file formats by analyzing their binary or text-based structures. It provides a basic pre-scan to ensure the file type is as expected before further processing or use (such as potential malware injection). This helps prevent errors, ensures compatibility, and adds a basic security layer by preventing incorrect or potentially harmful files from being processed.

last update: 3/17/2025 (dd/mm/yy)

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

```python
returns is_valid: bool, mesage: str, triangle_count: int
```

*in the case of an error, triangle_count = 0*

   - **ASCII STL**
     - Starts with the keyword `solid` followed by the model name.
     - Contains lines with `facet`, `vertex`, and `endfacet` keywords.
     - Detection method: Read the first few lines and confirm the presence of expected keywords.

```pyhton
returns is_valid:bool
```

### 2. **OBJ (Wavefront OBJ)**
   - Plain text format, human-readable.
   - Uses keywords such as `v` (vertex), `vn` (vertex normal), `vt` (texture coordinate), `f` (face), and `usemtl` (material usage).
   - Detection method: Scan the first few lines and ensure at least one of the key OBJ-related keywords is present.

### 3. **3MF** (future update)
   - Nothing here. for now...

### 4. **STEP** (future update)
   - no one but us chickens here! 🐔

### 5. **3DS** (future update)
   - if your reading this, take a water break 

### 5. **IGES** (future update)
   - Silence is golden... until the llamas start singing
   
   
## How Detection Works
The library follows a structured detection process:
1. ClamAV to scan files for general malware
2. **DoS** specific vulnerablilities (processing crashes, over utilization ect.)
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

##### **3d_verification.py**
For STLs
```python
...

if __name__ == "__main__":
    file_path = "test.stl"  # Replace with your STL file path.

    """
    replace xxx with the type of STL is being scaned
    or you could brute force it :D, the functions are made to fail fast then test
    """
    is_valid, message, num_facets = validate_xxx_stl(file_path)
    print(is_valid)      # Boolean indicating validity.
    print(message)       # Descriptive message, can contain unrecognised keywords for text based
    print(num_facets)    # Set of unrecognized keywords (if any).
```
For OBJs
```python
...

if __name__ == "__main__":
   file_path = "malware test/test_files/detect stl test.stl"
   is_valid, message = is_ascii_stl(file_path)
   print(message)
```

##### **clam.py**
```python
...

if __name__ == "__main__":
    # Example usage
    filename = "test.txt"
    files, scan_results = clam_scan(filename)

    """
    looks like the code for the email sender is on a coffee break
    (send_email() hasn't been tested the moment)
    """

    # recipient = "your_email@example.com"
    # subject = "ClamAV Scan Results"
    # body = f"Here are the ClamAV scan results for {filename}:\n\n{scan_results}"
    # send_email(recipient, subject, body)
```

## Tools
The scanning tools work based off of key words in the file, 
so rather than mannualy seaching for them,you can find the 
ones that will be detected with `kwd_search.py`. In 
```python
...

if __name__ == '__main__':

   file_path = 'file/path'  # Replace with your file path 
   keys = extract_keywords(file_path)
   ...
```
you need to replace `file_path` with the actual text-based file. 
the output will printout verticaly the found kewords,
along with a copy-pasteable list that can be transfered to the STL and OBJ files

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
