import sys
from ClassReader import Reader
from ClassStudent import Student
from ClassWriter import Writer

# Read csv file path from command line arguments
# @return string - file path with valid .csv extension
def csv_file_path() -> str:
    arguments = sys.argv
    if len(arguments) > 1 and arguments[1].lower().endswith(".csv"):
        return arguments[1]
    else:
        # Message for missing first argument
        print("Error: missing command-line argument <csv_file_path>")
    # Show general information message
    print("Use: python main.py <csv_file_path>")
    print("Example: python main.py students.csv")
    return None

# Create students objects from csv data
def process_csv_data(csv_data:list[dict]) -> list[dict]:
    students_data:list[dict] = []

    for row in csv_data:
        if not row.get("name"):
            print(f"Skipping line {row['id']} without a name.")
            continue

        # Pop name from row to process only subject scores
        name = row.pop("name")

        # Sikp row without subjects
        if len(row) <= 1:
            print(f"Skipping line {row['id']}, student {name} without a subjects.")
            continue
    
        # Create student instance with name
        student = Student(name)
        # Loop csv file subjects for this student and add them to student object

        for subject, score in row.items():
            
            # skip id because is csv line number
            if subject == 'id':
                continue

            if not isinstance(subject, str):
                print(f"Skipping invalid subject {subject} for student {name}, Line: {row['id']}")
                continue 

            if not isinstance(score, int):
                print(f"Skipping subject {subject} invalid score {score} for student {name}, Line: {row['id']}")
                continue

            if not (0 <= score <= 100):
                print(f"Score out of range for {subject}: {score} for student {name}, Line: {row['id']}")
                continue
        
            student.add_subject(subject, score)
        # Add student data from student object
        students_data.append(student.get_student_data())

    # Return list with Student instances 
    return students_data


if __name__ == "__main__":

    # Get csv file path from command-line arguments
    file_path = csv_file_path()

    # If file_path is empty exit program
    if not file_path:
        print("Program exit, file path not provided")
        exit(1)

    print(f"Input file: {file_path}")

    # Create csv reader object from Reader class with file_path
    csv_reader = Reader(file_path)
    # Read csv file content 
    csv_reader.read_csv_file()
    # Get data that was read from csv file
    csv_data = csv_reader.get_rows()

    if not csv_data:
        print("Program exit, no data was read in csv file")
        exit(1)

    full_file_len = csv_reader.get_file_len()
    print(f"Loaded {len(csv_data)} out of {full_file_len} lines from {file_path}")
    
    students_data = process_csv_data(csv_data)
    
    if not students_data:
        print("Program exit, student data can not be created from csv data")
        exit(1)

    print("Saving data to students_processed.csv")
    csv_writer = Writer("students_processed.csv")
    csv_writer.save_students(students_data)
    print("Program end")