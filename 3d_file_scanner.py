import struct
import os

def is_valid_binary_stl(file_path):
    """
    Validates whether a binary STL file is well-formed and reports any unrecognized keywords.
      1. Reads the first 80 bytes to check for STL-specific keywords.
      3. Checks if the number of triangles matches the expected value.
    
    Returns:
        bool: True if the file is valid, False otherwise.
        str: Message describing the validation status.
        int: The number of triangles in the file. (0 if error)
    """
    try:
        # get file size
        file_size = os.path.getsize(file_path)

        # Check the first 80 bytes for the expected header
        with open(file_path, 'rb') as f:
            header = f.read(80)  # Read the 80-byte header
            num_triangles_data = f.read(4) # Read the number of triangles
            # check if the header is complete
            if len(num_triangles_data) < 4:
                return False, "Incomplete file: unable to read triangle count.", 0
            
            # convert from binary to int
            num_triangles = struct.unpack('<I', num_triangles_data)[0]
            
            # calculate the number of triangles, plus the header section
            # read the docs on more information for this formula
            expected_size = 84 + num_triangles * 50
            if file_size == expected_size:
                return True, "Valid binary STL file.", num_triangles
            else:
                return False, f"Size mismatch: expected {expected_size} bytes, got {file_size} bytes.", 0
    except Exception as e:
        return False, f"Error processing file: {e}", 0


def validate_ascii_stl(file_path, extra_allowed_keywords=None):
    """
    Validates whether an ASCII STL file is well-formed and reports any unrecognized keywords.
      1. Reads the first 4096 characters to check for STL-specific keywords.
      2. Validates that the file starts with "solid" and ends with "endsolid".
      3. Counts facets (lines starting with "facet normal") and vertices (expecting exactly 3 per facet).
      4. Scans the entire file to collect any unrecognized keywords.
    
    Parameters:
      file_path (str): Path to the ASCII STL file.
      extra_allowed_keywords (list of str, optional): Additional allowed keywords.
    
    Returns:
      valid (bool): True if the file is valid, otherwise False.
      message (str): A message describing the result.
      unrecognized (set): A set of unrecognized keywords found (empty if none).
    """
    valid = False
    message = ""
    unrecognized = set()

    try:
        # check if file is valid and empty
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            message = "File is empty. "
            return False, message+str(unrecognized), 0

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Check the first 4096 characters for required STL keywords.
        first_chunk = content[:4096].lower()
        required_keywords = ["facet normal", "outer loop", "vertex", "endloop", "endfacet"]
        missing_keywords = [kw for kw in required_keywords if kw not in first_chunk]
        if missing_keywords:
            message = f"Missing keywords in the first chunk: {', '.join(missing_keywords)}"
            return False, message+str(unrecognized), 0

        # Split the file into lines for detailed validation.
        lines = content.splitlines()
        if not lines:
            message = "File has no content. "
            return False, message+str(unrecognized), 0

        # Validate start and end of the file.
        if not lines[0].strip().lower().startswith('solid'):
            message = "File does not start with 'solid' keyword. "
            return False, message, unrecognized

        if not lines[-1].strip().lower().startswith('endsolid'):
            message = "File does not end with 'endsolid'. "
            return False, message+str(unrecognized), 0

        num_facets = 0
        num_vertices = 0
        inside_facet = False

        # Count facets and vertices.
        for line in lines:
            stripped = line.strip().lower()
            if stripped.startswith('facet normal'):
                num_facets += 1
                inside_facet = True
            elif stripped.startswith('vertex') and inside_facet:
                num_vertices += 1
            elif stripped.startswith('endfacet'):
                inside_facet = False

        if num_facets == 0:
            message = "No 'facet normal' keywords found; not a valid STL."
            return False, message+str(unrecognized), 0

        if num_vertices != num_facets * 3:
            message = f"Mismatch: Expected {num_facets * 3} vertices, found {num_vertices}."
            return False, message+str(unrecognized), 0

        message = f"Valid ASCII STL file with {num_facets} facets."
        valid = True

        # Prepare the set of recognized keywords.
        recognized_keywords = {"solid", "endsolid", "facet normal", "outer loop", "vertex", "endloop", "endfacet"}
        if extra_allowed_keywords:
            recognized_keywords.update(kw.lower() for kw in extra_allowed_keywords)

        # Scan each line for potential unrecognized keywords.
        for line in lines:
            stripped = line.strip().lower()
            if not stripped:
                continue
            # Skip lines starting with numeric data.
            if stripped[0].isdigit() or stripped[0] in "-+.":
                continue
            tokens = stripped.split()
            token1 = tokens[0]
            token2 = " ".join(tokens[:2]) if len(tokens) >= 2 else token1
            if token1 not in recognized_keywords and token2 not in recognized_keywords:
                unrecognized.add(token1)

        return False, message+str(unrecognized), num_facets
    except Exception as e:
        message = f"Error processing file: {e}"
        return False, message, unrecognized

# Example usage:
# if __name__ == "__main__":
#     file_path = "test.stl"  # Replace with your STL file path.
#     valid, message, num_facets = validate_xxx_stl(file_path)
#     print(valid)           # Boolean indicating validity.
#     print(message)         # Descriptive message.
#     print(num_facets)    # Set of unrecognized keywords (if any).


def is_valid_obj(file_path):
    try:
        # Check that the file is not empty
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return False, "File is empty."
        
        # Read the file as text
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Define a tuple of typical OBJ keywords
        valid_keywords = ('o', '#', 'vn', 's', 'mtllib', 'f', 'vt', 'v', 'usemtl')
        
        # Look for at least one line that starts with a valid keyword
        for line in lines:
            stripped = line.strip()
            if stripped and stripped.startswith(valid_keywords):
                return True, "Valid OBJ file structure detected."
        
        return False, "No valid OBJ keywords found. This may not be a valid OBJ file."
    except Exception as e:
        return False, f"Error processing file: {e}"

# # Example usage:
# file_path = "malware test/test_files/detect stl test.stl"
# is_valid, message = is_ascii_stl(file_path)
# print(message)