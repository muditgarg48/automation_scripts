import os
import datetime
from commandline_functions import *

# can be by:
# seperate folders for extensions and folders
# sizes (currently, by less than a KB, by less than an MB, by less than a GB, by less than a TB)
#       (future, ask the number of thresholds and then from there to there to there till 1024 TB)
# last modified (by year, by month, by date)

size_type = ['B', 'KB', 'MB', 'GB', 'TB']

def extract_extension(file):
    return os.path.splitext(file)[1]

def get_proper_size_string_from_bytes(size):
    size_type_index = 0
    for i in range(len(size_type)):
        if size > 1024:
            size /= 1024
            size_type_index += 1
    size = round(size, 3)
    return f"{size} {size_type[size_type_index]}"

def extract_size_of_file(file):
    size = os.path.getsize(file)
    return size, get_proper_size_string_from_bytes(size)

def extract_size_of_folder(folder_path):
    # print()
    totalSize = 0
    totalContent = 0
    # print(f"Files inside {folder_path}:\n")
    for item in os.listdir(folder_path):
        if not os.path.isdir(os.path.join(folder_path, item)):
            size, _ = extract_size_of_file(os.path.join(folder_path, item))
            # print(f"{item} file size: {size}")
            totalSize += size
            totalContent += 1
    # print(f"Folders inside {folder_path}:\n")
    for item in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, item)):
            size, content = extract_size_of_folder(os.path.join(folder_path, item))
            # print(f"{item} FOLDER size: {size}")
            totalSize += size
            totalContent += content
    return totalSize, totalContent

def extract_time(file):
    return datetime.datetime.fromtimestamp(os.path.getmtime(file))

def try_to_create_subfolder(parent, child):
    try:
        os.makedirs(os.path.join(parent, child))
    except:
        pass

def move_to_subfolder(file_path, subfolder_name):
    file_name = os.path.basename(file_path)
    folder_path = os.path.dirname(file_path)
    try_to_create_subfolder(folder_path, subfolder_name)
    new_file_path = os.path.join(folder_path, subfolder_name, file_name)
    os.rename(file_path, new_file_path)

def print_details_of_file(file_path):
    file_name = os.path.basename(file_path)
    print(in_bold(file_name[:file_name.rfind('.')]), end='')
    print(in_red(f"{extract_extension(file_path)}"), end=' ')
    _, file_size_string = extract_size_of_file(file_path)
    print(in_yellow(f"[{file_size_string}]"), end=' ')
    print(in_green(f"[Last Modified: {extract_time(file_path)}]"), end=' ')

def print_details_of_folder(folder_path):
    folder_name = os.path.basename(folder_path)
    print(in_bold(folder_name), end=' ')
    size, content_num = extract_size_of_folder(folder_path)
    folder_size_string = get_proper_size_string_from_bytes(size)
    print(in_yellow(f"[{folder_size_string}]"), end=' ')
    print(in_yellow(f"[{content_num} files]"), end='')

def for_every_file_in_dir(path, choice):
    print("=======")
    print("Files:")
    print("=======")
    for item in os.listdir(path):
        item = os.path.join(path,item)
        if not os.path.isdir(item):
            print_details_of_file(item)
            if choice == "display":
                print()
            if choice == "sort_by_ext":
                move_to_subfolder(item, extract_extension(item))
                print(in_green("... Done"))
            if choice == "sort_by_size_1":
                size, _ = extract_size_of_file(item)
                for i in range(len(size_type)):
                    if size <= pow(1024,i):
                        move_to_subfolder(item, f"less than 1 {size_type[i]}")
                        break
                print(in_green("... Done"))


def for_every_folder_in_dir(path, choice):
    print("=======")
    print("Folders:")
    print("=======")
    for item in os.listdir(path):
        item = os.path.join(path,item)
        if os.path.isdir(item):
            # print(os.path.basename(item), end='')
            print_details_of_folder(item)
            if choice == "display":
                print()
            elif choice == "sort_by_ext":
                move_to_subfolder(item, "folders")
                print(in_green(" ... Done"))
            if choice == "sort_by_size_1":
                size, _ = extract_size_of_folder(item)
                for i in range(len(size_type)):
                    if size <= pow(1024,i):
                        move_to_subfolder(item, f"less than 1 {size_type[i]}")
                        break
                print(in_green("... Done"))

def main():
    folder_path = input("Enter the path of the folder to organise: ")
    sort_methods = [
        'Sort into separate folders for Extensions and Folders',
        'Sort into different sizes (less than KB, less than MB ...)',
        'Sort into different last modified time periods'
    ]
    print("Sorting methods: ")
    for method_index in range(len(sort_methods)):
        print(f"{method_index+1}. {sort_methods[method_index]}")
    sorting_choice = int(input("Enter your choice: "))
    print()
    if not (sorting_choice >= len(sort_methods) or sorting_choice <= 0):
        print(in_green(f"Initiating {sort_methods[sorting_choice-1]} ... "))
    if sorting_choice == 1:
        for_every_folder_in_dir(folder_path, "sort_by_ext")
        print()
        for_every_file_in_dir(folder_path, "sort_by_ext")
    elif sorting_choice == 2:
        for_every_folder_in_dir(folder_path, "sort_by_size_1")
        print()
        for_every_file_in_dir(folder_path, "sort_by_size_1")
    elif 0 < sorting_choice <= len(sort_methods) :
        print("Still under development!")
    else:
        for_every_folder_in_dir(folder_path, "display")
        print()
        for_every_file_in_dir(folder_path, "display")

if __name__ == '__main__':
    main()