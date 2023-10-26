import sys
import os
import argparse

def main():
    """
    Renames all subdirectories of the given directory that contain the
    given substring by replacing the substring with the given replacement.
    """
    print("This function will takes a DICOM parent folder")
    print("Enter a desired directory containing subdirectories sorted and named at the case level ie. '123456-789123' ")
    directory_path = input("Please Copy Parent Directory: ")
    substring = input("Please input Site_id substring: ")
    replacement = input ("Please enter correct site_id: ")
    subdir_count = 0 
    for subdir_name in os.listdir(directory_path):
        subdir_path = os.path.join(directory_path, subdir_name)
        if os.path.isdir(subdir_path) and substring in subdir_name:
            parts = subdir_name.split("-")
            new_subdir_name = f"{replacement}-{parts[1]}"
            new_subdir_path = os.path.join(directory_path, new_subdir_name)
            os.rename(subdir_path, new_subdir_path)
            subdir_count += 1
            print(f'Renamed "{subdir_name}" to "{new_subdir_name}"')
    print ("Renamed " + str(subdir_count) + " folders")
    input("Press anything to exit function")




            
if __name__ == "__main__":
   main()


    
