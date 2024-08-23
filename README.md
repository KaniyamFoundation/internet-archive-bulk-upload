This project helps to bulk upload files to internet archive.

# INSTALL

1.
install python3

2.
Then install the python library "internetarchive"

python3 -m pip install internetarchive


check here https://archive.org/developers/internetarchive/ for more details.

3.
configure ia

```
ia configure
```

It will ask for your credentials for archive.org
give them and ensure the config is saved.


# Steps

1. copy all the files you want upload to a specific folder
2. copy  the files get_all_filenames.py and ia-bulk-upload.py to that folder
3. Run the command

```
python3 get_all_filenames.py
```

This will create file called files_list.csv with all the file names in the current folder

4. Create a CSV file,  metadata.csv with below fields, using libreoffice calc, or MS excel or google sheets.

file,identifier,title,alt_title,creator,alt_creator,publisher,alt_publisher,year,source,description,collection,license,language,mediatype,subject



5. copy the contents from files_list.csv and paste in the "file" column.

6. Fill title with original name of the item. This can be in native language or english

7. Fill alt_title with an english title. Must be in english

8. leave the identifier as empty

9. Fill other columns.

10. The manditory fields are title, alt_title, creator, language

11. The more info you give, the more good.

12. if you need to give multiple values for author or subjects, seperate them with ;

13. Then run the below command

```
python3 ia-bulk-upload.py
```

This will upload all the files to archive.org

On completion, the file will be moved to a folder "success_folder"
On error, the file will be moved to "error_folder" or kept on current folder.

# License

General Public License V3