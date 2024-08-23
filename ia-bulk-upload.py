# write a program to bulk uplod files to internetarchive.

# read metadata in CSV. the fields in CSV file are file,identifier,title,alt_title,creator,alt_creator,publisher,alt_publisher,year,source,description,collection,license,language,mediatype,subject

# check if all the files is there in local system

# add current timestamp in the identifier


# move the uploaded file to another folder
# sleep for 30 sec

# move error files to another folder

# on error move to next file

# show the summary, csv file name, success count, failed count with file name.



import os
import csv
import shutil
import time
import datetime
from internetarchive import upload

def read_metadata(csv_file):
    metadata = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            metadata.append(row)
    return metadata





# List of required fields
required_fields = [
    "file", "identifier", "title", "alt_title", "creator", "alt_creator", 
    "publisher", "alt_publisher", "year", "source", "description", 
    "collection", "license", "language", "mediatype", "subject"
]

def check_csv_fields(file_path):
    # Read the CSV file and get the headers
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        
        # Check for missing fields
        missing_fields = [field for field in required_fields if field not in headers]
        
        if not missing_fields:
            print("All required fields are present.")
        else:
            print(f"Missing fields: {', '.join(missing_fields)}")
            sys.exit()




# List of required fields
required_fields = ["alt_title", "title", "creator", "language"]

def check_csv_values(file_path):
    missing_values = []  # To store rows with missing values
    
    # Open the CSV file and read it using DictReader
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Iterate over each row to check for missing values in required fields
        for i, row in enumerate(reader, start=1):
            for field in required_fields:
                if not row.get(field):  # Check if the field is empty or None
                    missing_values.append((i, field))
    
    # Report the results
    if not missing_values:
        print("All required fields have values in all rows.")
    else:
        print("Missing values found:")
        for row_num, field in missing_values:
            print(f"Row {row_num} is missing a value for the field '{field}'.")
            sys.exit()
            
            



def upload_files(metadata, upload_folder, success_folder, error_folder):
    success_count = 0
    failed_count = 0
    errors = []

    for item in metadata:
        file_path =  os.path.join(upload_folder, item['file'].strip())
        if not os.path.isfile(file_path):
            errors.append((item['file'].strip(), 'File does not exist'))
            failed_count += 1
            continue

        # Prepare metadata with timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        identifier = f"{item['alt_title']}_{timestamp}"

        metadata_for_upload = {
            'title': item['title'].strip(),
            'alt_title': item['alt_title'].strip(),
            'creator': item['creator'].strip(),
            'alt_creator': item['alt_creator'].strip(),
            'publisher': item['publisher'].strip(),
            'alt_publisher': item['alt_publisher'].strip(),
            'year': item['year'].strip(),
            'source': item['source'].strip(),
            'description': item['description'].strip(),
            'collection': item['collection'].strip(),
            'license': item['license'].strip(),
            'language': item['language'].strip(),
            'mediatype': item['mediatype'].strip(),
            'subject': item['subject'].strip()
        }

        try:
            # Upload file to Internet Archive
            print("Uploading " + file_path)
            upload(identifier, file_path, metadata=metadata_for_upload)
            # Move file to success folder
            print("Uploaded")
            shutil.move(file_path, os.path.join(success_folder, item['file'].strip()))
            success_count += 1
            time.sleep(30)  # Sleep for 30 seconds
        except Exception as e:
            # Move file to error folder
            shutil.move(file_path, os.path.join(error_folder, item['file']))
            errors.append((item['file'].strip(), str(e)))
            failed_count += 1

    return success_count, failed_count, errors

def print_summary(csv_file, success_count, failed_count, errors):
    print(f"Summary for CSV file: {csv_file}")
    print(f"Success count: {success_count}")
    print(f"Failed count: {failed_count}")
    if failed_count > 0:
        print("Failed files:")
        for error in errors:
            print(f"File: {error[0]} - Error: {error[1]}")

def main(csv_file, upload_folder, success_folder, error_folder):
    check_csv_fields(csv_file)
    check_csv_values(csv_file)

    # Create folders if they do not exist
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(success_folder, exist_ok=True)
    os.makedirs(error_folder, exist_ok=True)

    # Read metadata from CSV
    metadata = read_metadata(csv_file)

    # Upload files and handle errors
    success_count, failed_count, errors = upload_files(metadata, upload_folder, success_folder, error_folder)

    # Print summary
    print_summary(csv_file, success_count, failed_count, errors)





if __name__ == "__main__":
    csv_file = 'metadata.csv'
    upload_folder = './'
    success_folder = 'success_folder'
    error_folder = 'error_folder'

    main(csv_file, upload_folder, success_folder, error_folder)
