# FortiCRP

Fortinet Contract Reader and Parser (FortiCRP) is a python script to extract registration codes from Fortinet PDF license and support contract files.

## Usage

Make sure git is installed on your system.

Clone the repo:

    git clone https://github.com/glennake/FortiCRP.git

Install dependancies using pip:

    pip3 install -r requirements.txt

Put all the .zip archives containing license and support contract files from Fortinet in a directory (note: do not unzip them).

Run the parser, passing the above directory path:

    python3 forticrp.py --dir /path/to/directory

A CSV file will be generated in the same directory that contains all the parsed registration codes.
