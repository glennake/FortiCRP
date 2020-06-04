# FortiCRP
Fortinet Contract Reader and Parser (FortiCRP) is a python script to extract registration codes from Fortinet PDF license and support contract files.

## Usage
Put all the .zip archives containing license and support contract files from Fortinet in a directory (Note: do not unzip them!)

Run the parser, passing the above directory path:

python3 forticrp.py --dir /path/to/directory

A CSV file will be generated in the same folder containing all of the parsed registration codes.
