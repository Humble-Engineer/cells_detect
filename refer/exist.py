import os

path_to_check = "./samples/img(100).png"

if os.path.exists(path_to_check):
    print(f"The file or directory at {path_to_check} exists.")
else:
    print(f"The file or directory at {path_to_check} does not exist.")
