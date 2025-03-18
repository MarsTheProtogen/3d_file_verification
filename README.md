# 3D File Verification

## 📌 Overview
This library is designed to detect and verify various **3D file formats** by analyzing their **binary or text-based structures**. It provides a **pre-scan** to ensure the file type is as expected before further processing, preventing errors, ensuring compatibility, and adding a **basic security layer** to detect incorrect or potentially harmful files.

📅 **Last Update:** *March 17, 2025*

---

## 📂 Supported File Types

### 🟢 **STL (Stereolithography)**
#### 🔹 **Binary STL**
- Identified by an **80-byte header** followed by a **4-byte unsigned integer** indicating the number of triangles.
- The expected file size is calculated as: `header_size + (50 * num_triangles)` bytes.

   **Why 50 bytes per triangle?**
   - 12 bytes → 3 normal vector floats (`float32 × 3`)
   - 36 bytes → 3 vertices (`float32 × 9`)
   - 2 bytes → Attribute byte count

   ✅ **Detection Method:** Reads the first **80 bytes**, verifies format, and checks the expected file size.
   
```python
returns is_valid: bool, message: str, triangle_count: int
```

🔹 **ASCII STL**
- Starts with the keyword `solid` followed by the model name.
- Contains lines with `facet`, `vertex`, and `endfacet` keywords.
- ✅ **Detection Method:** Reads the first few lines and confirms the presence of expected keywords.

```python
returns is_valid: bool
```

---

### 🟢 **OBJ (Wavefront OBJ)**
- **Plain text format**, human-readable.
- Uses keywords like `v`, `vn`, `vt`, `f`, and `usemtl`.
- ✅ **Detection Method:** Scans the first few lines to ensure at least one OBJ-related keyword is present.

---

### 🔜 **Future Support**
#### **3MF** → _(Coming Soon)_
📌 Nothing here... for now.

#### **STEP** → _(Planned)_
🐔 No one but us chickens here!

#### **3DS** → _(Planned)_
💧 If you're reading this, take a water break!

#### **IGES** → _(Planned)_
🎶 Silence is golden... until the llamas start singing.

---

## 🔍 How Detection Works

1️⃣ **Malware Scan** → Uses **ClamAV** to detect harmful files.

2️⃣ **Denial of Service (DoS) Protection** → Prevents processing crashes & resource exhaustion.

3️⃣ **File Size Verification** → Ensures file is neither empty nor corrupted.

4️⃣ **Binary Signature Analysis** → Verifies binary STL structure.

5️⃣ **Keyword Matching** → Confirms text-based OBJ & STL integrity.

6️⃣ **Archive/XML Validation** → _(Future feature for 3MF)_

---

## 🔐 Security & Safety Considerations

✅ **Pre-Scan Protection:**
- Ensures the file **matches the expected format** before further processing.
- Prevents incorrect file types from being **loaded into a 3D application**.

⚠️ **Potential Security Risks Mitigated:**
- Detects **malformed or incomplete files**.
- Reduces **attack vectors** like:
   - Malformed **3MF files** exploiting XML parsing vulnerabilities.
   - Memory overflow attacks on **STLs/OBJs**.
- Can be extended for **further validation** (e.g., large file size detection to prevent crashes).

---

## 📌 Example Usage

#### **🔹 3D File Verification (STL)**
```python
if __name__ == "__main__":
    file_path = "test.stl"  # Replace with your STL file path.
    
    # Replace 'xxx' with the type of STL being scanned
    is_valid, message, num_facets = validate_xxx_stl(file_path)
    print(is_valid)      # Boolean indicating validity
    print(message)       # Message, including unrecognized keywords
    print(num_facets)    # Number of facets (if applicable)
```

#### **🔹 OBJ Verification**
```python
if __name__ == "__main__":
   file_path = "malware test/test_files/detect stl test.stl"
   is_valid, message = is_ascii_stl(file_path)
   print(message)
```

#### **🔹 ClamAV Scan (clam.py)**
```python
if __name__ == "__main__":
    filename = "test.txt"
    files, scan_results = clam_scan(filename)
    
    """
    Looks like the email sender is on a coffee break ☕
    (send_email() hasn't been tested yet)
    """
    # recipient = "your_email@example.com"
    # subject = "ClamAV Scan Results"
    # body = f"Here are the ClamAV scan results for {filename}:\n\n{scan_results}"
    # send_email(recipient, subject, body)
```

---

## 🛠️ Tools

The scanning tools work by detecting **keywords** in the file rather than manual searching. Use `kwd_search.py` to extract them automatically:

```python
#rest of the kwd_search file
...
 
if __name__ == '__main__':
   file_path = 'file/path'  # Replace with your file path
   keys = extract_keywords(file_path)
```
📌 Replace `file_path` with the actual text-based file.
📌 The output will **list detected keywords** vertically and provide a **copy-pasteable format** for STL/OBJ.

---

## 🚀 Possible Improvements
✅ **Checksum validation** → Detect file corruption.
✅ **Error detection** → Identify malware & file format issues.
✅ **Deeper security scans** → Sandbox execution for **3MF XML parsing**.
✅ **More file type support** → Expand compatibility beyond **STL/OBJ**.

---

<br></br>


<br></br>


<br></br>


<br></br>


<br></br>
