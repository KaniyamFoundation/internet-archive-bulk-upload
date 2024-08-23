# get all the files in current folder and write their names in a csv file
import os
import csv

# Get the current working directory
current_folder = os.getcwd()


# Iterate over all files in the current folder
for file_name in os.listdir(current_folder):
    old_file_path = os.path.join(current_folder, file_name)
    
    # Check if it's a file and not a directory
    if os.path.isfile(old_file_path):
        # Replace spaces with underscores
        new_file_name = file_name.replace(' ', '_')
        new_file_path = os.path.join(current_folder, new_file_name)
        
        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f'Renamed: "{file_name}" to "{new_file_name}"')
        

# Get a list of files in the current folder
files = [f for f in os.listdir(current_folder) if os.path.isfile(os.path.join(current_folder, f))]

# Define the CSV file path
csv_file_path = os.path.join(current_folder, 'files_list.csv')

# Write the list of files to the CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['FileName'])  # Write the header
    for file_name in files:
        writer.writerow([file_name])  # Write each file name

print(f'File names have been written to {csv_file_path}')



'''
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
import re

def is_tamil(word):
    # Unicode range for Tamil script: \u0B80-\u0BFF
    return bool(re.search(r'[\u0B80-\u0BFF]', word))

def transliterate_tamil_to_english(word):
    if is_tamil(word):
        return transliterate(word, sanscript.TAMIL, sanscript.ITRANS)
    return word

# Test cases
def test_transliteration():
    words = [
        "தமிழ்",               # Tamil
        "Tamil",               # English
        "hello",               # English
        "வணக்கம்",             # Tamil for "Hello"
        "123தமிழ்",           # Mixed with numbers
        "தமிழ்123",           # Mixed with numbers
    ]
    
    expected_results = [
        "tamizh",             # Transliterated Tamil
        "Tamil",              # No Tamil characters
        "hello",              # No Tamil characters
        "vaNakkam",           # Transliterated Tamil
        "123tamizh",          # Mixed with numbers, transliterated
        "tamizh123",          # Mixed with numbers, transliterated
    ]
    
    results = [transliterate_tamil_to_english(word) for word in words]
    
    assert results == expected_results, f"Failed! Expected {expected_results} but got {results}"
    print("All test cases passed!")

# Run the test
test_transliteration()



'''
