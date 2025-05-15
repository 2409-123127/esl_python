import csv
from ClassStudent import Student

# Class for saving data to output csv file
class Writer:
    # Class constructor
    # @arg csv_file_path - location of csv file for the class to read
    def __init__(self, output_file_path: str):
        self._output_file_path = output_file_path

    # Save students data to output csv file
    # @arg students:list of Students objects, returns none
    def save_students(self, students_data: list[dict]):
        if not students_data:
            print("Writer Error: No students to save")
            return None
        
        try:
            with open(self._output_file_path, "w", newline="", encoding="utf-8") as output_file:

                all_columns = set()
                for student in students_data:
                    all_columns.update(student.keys())

                # Sort them for consistency
                fieldnames = sorted(all_columns, key=self._column_sort_order)

                writer = csv.DictWriter(output_file, fieldnames=fieldnames)

                writer.writeheader()
                
                for student in students_data:
                    writer.writerow(student)
            print(f"Writer: Successfully saved {len(students_data)} students to {self._output_file_path}")

            # Handle exceptions
        except IOError:
            print(f"Writer Error: I/O error, file {self._output_file_path} can not be written")
        except PermissionError:
            print(f"Writer Error: Program do not have permission to create file {self._output_file_path}")
        except IsADirectoryError:
            print(f"Writer Error: {self._output_file_path} is a directory")
        except UnicodeDecodeError:
            print(f"Writer Error: {self._output_file_path} file encoding is wrong, expected utf-8")
        except Exception as e:
            print(f"Writer Error: Unexpected exception when saving {self._output_file_path} \nError: {e}")

    def _column_sort_order(self, field):
        if field == "name":
            return "0_" + field
        elif field in ("total_score", "average_score", "final_grade"):
            return "1_" + field
        elif field.endswith("_score") or field.endswith("_grade"):
            return "2_" + field
        elif field == "summary":
            return "3_" + field
        return "4_" + field
