import csv
from io import TextIOWrapper

# Class reader, reads data from csv file
class Reader:

    # Class constructor
    # @arg csv_file_path - path to input csv file
    def __init__(self, csv_file_path: str) -> None:
        if not csv_file_path:
            raise ValueError("Reader Error: csv_file_path can not be empty")

        # Set class attributes
        self._csv_file_path: str = csv_file_path 
        self._data:list[dict] = []
        self._file_len:int = 0

    # Retrun stored list of rows
    # Must run read_csv_file before using this method
    def get_rows(self) -> list[dict]:
        if not self._data: return []

        return self._data
 
    # Method _csv_file_path, reads data from _csv_file_path attribute, set in constructor
    def read_csv_file(self) -> None:
        try:
            # Try to open the CSV file in read mode with UTF-8 encoding
            with open(self._csv_file_path, 'r', encoding='utf-8') as file:
                # Read first 1024 bytes from csv file for a csv sniffer sample
                sample = file.read(1024)
                # Go to beginning of the file 1024 bytes back
                file.seek(0)

                # Create csv.sniffer instance for header detection
                sniffer = csv.Sniffer()
                # https://www.ietf.org/rfc/rfc4180.txt
                # According to RFC4180 csv file headers are optional
                has_header = sniffer.has_header(sample)

                if has_header:
                    self.read_headers_csv(file)
                else:
                    self.read_no_header_csv(file)

        # Handle exceptions
        except FileNotFoundError:
            print(f"Reader Error: csv file {self._csv_file_path} not found")
        except IOError:
            print(f"Reader Error: I/O error, file {self._csv_file_path} can not be open")
        except PermissionError:
            print(f"Reader Error: Program does not have permission to open file {self._csv_file_path}")
        except IsADirectoryError:
            print(f"Reader Error: {self._csv_file_path} is a directory, exptected file")
        except UnicodeDecodeError:
            print(f"Reader Error: {self._csv_file_path} file encoding is wrong, expected utf-8")
        except Exception as e:
            print(f"Reader Error: Unexpected exception when opening {self._csv_file_path} \nError: {e}")

    # Parse csv file with headers
    def read_headers_csv(self, file:TextIOWrapper):
        # Use csv DictReader to read rows into dictionary with keys and values
        reader = csv.DictReader(file)
        
        # Loop rows in the reader
        for row in reader:
            self._file_len += 1
            converted_values["id"] = self._file_len
            # Skip empty row
            if not any(row):
                print("Skipping empty line {self._file_len}")
                continue
            converted_values:dict = {}
            non_int_values = 0
            # Loop each value in a row and try to convert it to int
            for key, value in row.items():
                try:
                    # Try to conver value into int
                    converted_values[key] = int(value)
                    # If fail except value error
                except ValueError:
                    non_int_values += 1
                    # Value error means that string can not be converted to int, we can expect this value to be a name
                    if 'name' not in row and 'name' not in converted_values:
                        # if there is not name in reader keys and converted_values name is not set, make this value a name
                        converted_values["name"] = value
                    else:
                        # Or set it to default key:value
                        converted_values[key] = value
            # Store row in class _data attribute
            if non_int_values == 1:
                self._data.append(converted_values)
            else:
                print(f"Reader Error: Skipping line: {self._file_len}, only one value must be string: {row}")

    def read_no_header_csv(self, file: TextIOWrapper):
        # Initialize a CSV reader to read rows from the file
        reader = csv.reader(file)
        # Loop through each row in the CSV file
        for row in reader:

            converted_values: dict = {}
            self._file_len += 1
            converted_values["id"] = self._file_len

            # Initialize subject_id to 0 for each row
            subject_id = 0
            # Create an empty dictionary to store converted data for each row
            non_int_values = 0
            # Loop through each value in the row
            for value in row:
                try:
                    # Increment subject_id for each valid subject value found
                    subject_id += 1 
                    # Attempt to convert the value to an integer and store it as subject{subject_id}
                    converted_values[f"subject{subject_id}"] = int(value)
                except ValueError:
                    non_int_values += 1
                    # If conversion fails (i.e., the value is not an integer), handle it differently
                    if 'name' not in converted_values:
                        # If the 'name' key doesn't exist, it means we've encountered the name value
                        subject_id -= 1  # Adjust subject_id back to the correct value
                        converted_values["name"] = value  # Store the name
                    else:
                        # For any other non-integer values after 'name', store it as subject{subject_id}
                        converted_values[f"subject{subject_id}"] = value
            
            # Append the converted row data (as a dictionary) to the internal data list
            if non_int_values == 1 and len(converted_values['name']) > 0:
                self._data.append(converted_values)
            else:
                print(f"Reader Error: Skipping line: {self._file_len}, only one value must be string: {row}")

    def get_file_len(self) -> int:
        return self._file_len
