#!/usr/bin/env python3

# Title: Fortinet Contract Reader and Parser (FortiCRP)
#
# Description: Fortinet Contract Reader and Parser (FortiCRP) is a python script to extract
#              registration codes from Fortinet PDF license and support contract files.
#
# Author: Glenn Akester (@glennake)
#
# Version: 0.0.1
#
# FortiCRP is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FortiCRP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# If you don't have a copy of the GNU General Public License,
# it is available here <http://www.gnu.org/licenses/>.

# Imports

import csv
from datetime import datetime
import os
from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError
import re
from zipfile import ZipFile


class forticrap:
    def __init__(self, license_dir):

        # Read file listing from license directory

        dir_file_list = os.listdir(license_dir)

        self.license_dir = license_dir

        self.license_zip_list = []

        for dir_file in dir_file_list:

            if dir_file.endswith(".zip"):

                self.license_zip_list.append(dir_file)

        # Static variables

        self.parsed_licenses = {}
        self.ignored_files_patterns = ["__MACOSX"]

        # Define regex patterns

        self.re_lic_regcode = (
            r"Registration Code\s\s\s:\s\s(.....-.....-.....-.....-......)"
        )

        self.re_supp_regcode = r"ContractRegistrationCode:(.+?)Support"

    def _parse_licenses(self):

        for zip_file in self.license_zip_list:

            contract_sku = zip_file.split("_")[0]

            if contract_sku not in self.parsed_licenses:
                self.parsed_licenses[contract_sku] = []

            zip_file_contents = ZipFile(self.license_dir + "/" + zip_file, "r")

            zip_file_contents_namelist = zip_file_contents.namelist()

            for ignored_pattern in self.ignored_files_patterns:
                for i, file_name in enumerate(zip_file_contents_namelist):
                    if ignored_pattern in file_name:
                        zip_file_contents_namelist.pop(i)

            for pdf_file in zip_file_contents_namelist:

                pdf_raw = zip_file_contents.open(pdf_file, "r")

                try:
                    pdf_data = PdfFileReader(pdf_raw)
                except PdfReadError:
                    print(
                        "Failed to read pdf file "
                        + pdf_file
                        + " in zip archive "
                        + zip_file
                    )

                pdf_text = ""

                for page in range(pdf_data.numPages):
                    page_data = pdf_data.getPage(page)
                    pdf_text += page_data.extractText()

                self.parsed_licenses[contract_sku].append(pdf_text)

    def get_parsed_licenses(self):

        if not self.parsed_licenses:
            self._parse_licenses()

        return self.parsed_licenses

    def get_registration_codes(self):

        if not self.parsed_licenses:
            self._parse_licenses()

        registration_codes = {}

        for contract_sku, license_data in self.parsed_licenses.items():

            registration_codes[contract_sku] = []

            for data in license_data:

                reg_code = ""

                if not reg_code:

                    re_match = re.search(self.re_lic_regcode, data)

                    if re_match:
                        registration_codes[contract_sku].append(re_match.group(1))

                if not reg_code:

                    re_match = re.search(self.re_supp_regcode, data)

                    if re_match:
                        registration_codes[contract_sku].append(re_match.group(1))

        return registration_codes


def main(license_dir):

    timestamp = str(datetime.now().strftime("%Y%m%d_%H%M%S"))

    fcrap = forticrap(license_dir)
    registration_codes = fcrap.get_registration_codes()

    import json

    with open(license_dir + "/licenses_" + timestamp + ".csv", "w") as csv_file:

        csv_writer = csv.DictWriter(
            csv_file, fieldnames=["contract_sku", "registration_code"], delimiter=","
        )

        csv_writer.writeheader()

        for contract_sku, reg_codes in registration_codes.items():

            for reg_code in reg_codes:

                line = {"contract_sku": contract_sku, "registration_code": reg_code}

                csv_writer.writerow(line)


if __name__ == "__main__":

    # Imports

    import argparse

    # Parse arguments

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "-d", "--dir", help="directory containing license files", required=True,
    )

    args = arg_parser.parse_args()

    # Call main

    license_dir = args.dir

    main(license_dir)
