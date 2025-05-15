class Student:

    # Class constructor with class attributes
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._subjects: list[dict] = []
        self._total_score: int = 0

    # Add student subject and calculate grades and increase total_score
    # @arg subject_name:str - subject name
    # @arg subject_score - students score for this subject
    def add_subject(self, subject_name: str, subject_score: int) -> None:
                
        # Increase total score
        self._total_score += subject_score
        # Calculate grade from score
        subject_grade = self._calculate_grade(subject_score)
        # Store subject for student in _subjects attribute
        self._subjects.append({"name": subject_name, "score": subject_score, "grade": subject_grade})

    # Calculate grade method
    # @arg score: int - score for a subject
    # @return grade:str -  returns grade A,B,C,D,F
    def _calculate_grade(self, score: int) -> str:
        if score >= 90: return "A"
        if score >= 80: return "B"
        if score >= 70: return "C"
        if score >= 60: return "D"
        return "F"
    
    # Returns total student score
    def total_score(self) -> int:
        return self._total_score
    
    # Calculates average score total_score/number of subjects
    def average_score(self) -> float:
        if not self._subjects:
            return 0.0
        return round(self._total_score/len(self._subjects), 2)
    
    # Returns final grade from average score 
    def final_grade(self) -> str:
        return self._calculate_grade(self.average_score())
    
    # Generates summary comment
    def generate_summary(self):

        text = f"{self._name.capitalize()} have "

        # List all subjects with grade F, final_grade and average score
        failed_subjects = [item["name"].capitalize() for item in self._subjects if item.get('grade') == "F"]
        final_grade = self.final_grade()
        average_score = self.average_score()

        # If student has F from any subject, generate output with fail message
        if len(failed_subjects) > 0:
            
            # Add message to inform that final_grade is not F but if there is F on subject 
            if final_grade != "F":
                text += f"{final_grade} as final grade but will "
            
            # List all subjects with F grade
            text += f"fail the year because of F in {' and '.join(failed_subjects)}. "
        elif final_grade == "F":
            text += f"fail the year because with F as the final and {average_score} average score."
        else:
                # Generate pass message for student that did not have grade F from any subject
            text += f"pass the year with average score of {average_score} and {final_grade} as his final grade."
        
        return text
    

    # Returns all student data as a dictionary
    def get_student_data(self) -> dict:

        student_data:dict = {}

        student_data["name"] = self._name
        
        # Add subjects to student data with a keys subjectName_score, subjectName_grade and set the values
        for subject in self._subjects:
            student_data[subject["name"]+"_score"] = subject["score"]
            student_data[subject["name"]+"_grade"] = subject["grade"]

        student_data["total_score"] = self._total_score
        student_data["average_score"] = self.average_score()
        student_data["final_grade"] = self.final_grade()
        student_data["summary"] = self.generate_summary()
        
        return student_data