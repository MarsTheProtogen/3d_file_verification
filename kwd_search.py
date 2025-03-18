def extract_keywords(file_path):
    keywords = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                # Get the first token on the line (the keyword)
                token = stripped.split()[0]
                keywords.add(token)
        return keywords
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Example usage:
if __name__ == '__main__':
    file_path = 'file/path'  # Replace with your file path 
    keys = extract_keywords(file_path)

    # Print the keywords found in the file, sorted alphabetically and vertically
    if keys is not None:
        print("Keywords found in the file:")
        for k in sorted(keys):
            print(k)

        # print keys in a copy paste format
        print()
        print(keys)