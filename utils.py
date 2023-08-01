import chardet

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# Example usage
file_path = r'C:\Users\CAML078995\Documents\Python\ExplorateurDeFichier\test.txt'
encoding = detect_file_encoding(file_path)
print('Encoding:', encoding)