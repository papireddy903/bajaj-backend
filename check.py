import magic

mime = magic.Magic(mime=True)
print(mime.from_file(r"C:\Users\papir\OneDrive\Desktop\example.txt"))
