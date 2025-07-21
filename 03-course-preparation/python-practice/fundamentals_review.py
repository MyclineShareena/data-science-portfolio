"""
Python Fundamentals Review for DAMG Courses
Focus: Data structures, functions, classes, file handling
"""

import pandas as pd
import json
import sqlite3
from datetime import datetime
import os

def data_structures_review():
    """Review essential Python data structures"""
    print("=== DATA STRUCTURES REVIEW ===")
    
    # Lists and comprehensions
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    even_squares = [x**2 for x in numbers if x % 2 == 0]
    print(f"Even squares: {even_squares}")
    
    # Dictionaries and operations
    student_data = {
        'Alice': {'grade': 85, 'major': 'CS'},
        'Bob': {'grade': 92, 'major': 'Data Science'},
        'Charlie': {'grade': 78, 'major': 'Engineering'}
    }
    
    # Dictionary comprehension
    high_performers = {name: data for name, data in student_data.items() if data['grade'] > 80}
    print(f"High performers: {high_performers}")
    
    # Sets for unique operations
    courses_taken = {'Python', 'SQL', 'Statistics', 'ML', 'Python', 'SQL'}
    unique_courses = set(courses_taken)
    print(f"Unique courses: {unique_courses}")
    
    return student_data

def functions_and_classes():
    """Review functions and object-oriented programming"""
    print("\n=== FUNCTIONS AND CLASSES ===")
    
    # Function with multiple return types
    def analyze_grades(grades):
        """Analyze student grades with comprehensive metrics"""
        if not grades:
            return None
        
        return {
            'count': len(grades),
            'average': sum(grades) / len(grades),
            'highest': max(grades),
            'lowest': min(grades),
            'passing_rate': sum(1 for g in grades if g >= 70) / len(grades) * 100
        }
    
    # Class for data processing
    class StudentAnalyzer:
        def __init__(self, data):
            self.data = data
            self.processed_data = None
        
        def clean_data(self):
            """Remove invalid entries"""
            self.processed_data = {
                name: info for name, info in self.data.items() 
                if info['grade'] is not None and 0 <= info['grade'] <= 100
            }
            return self
        
        def get_statistics(self):
            """Get comprehensive statistics"""
            if not self.processed_data:
                self.clean_data()
            
            grades = [info['grade'] for info in self.processed_data.values()]
            return analyze_grades(grades)
        
        def get_major_distribution(self):
            """Get distribution by major"""
            if not self.processed_data:
                self.clean_data()
            
            major_counts = {}
            for info in self.processed_data.values():
                major = info['major']
                major_counts[major] = major_counts.get(major, 0) + 1
            
            return major_counts
    
    # Test the classes
    student_data = data_structures_review()
    analyzer = StudentAnalyzer(student_data)
    
    stats = analyzer.get_statistics()
    majors = analyzer.get_major_distribution()
    
    print(f"Grade statistics: {stats}")
    print(f"Major distribution: {majors}")
    
    return analyzer

def file_handling_practice():
    """Practice different file handling scenarios"""
    print("\n=== FILE HANDLING PRACTICE ===")
    
    os.makedirs('../data', exist_ok=True)
    # JSON handling
    sample_data = {
        'timestamp': datetime.now().isoformat(),
        'metrics': {
            'total_students': 150,
            'average_grade': 84.5,
            'courses_offered': 12
        },
        'departments': ['CS', 'Data Science', 'Engineering']
    }
    
    # Write JSON
    with open('../data/sample_metrics.json', 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    # Read JSON
    with open('../data/sample_metrics.json', 'r') as f:
        loaded_data = json.load(f)
    
    print(f"Loaded data: {loaded_data['metrics']}")
    
    # CSV handling with pandas
    df = pd.DataFrame({
        'student_id': range(1, 11),
        'name': [f'Student_{i}' for i in range(1, 11)],
        'grade': [85, 92, 78, 88, 94, 76, 89, 91, 83, 87],
        'major': ['CS', 'DS', 'ENG', 'CS', 'DS', 'ENG', 'CS', 'DS', 'ENG', 'CS']
    })
    
    df.to_csv('../data/students.csv', index=False)
    loaded_df = pd.read_csv('../data/students.csv')
    print(f"CSV data loaded: {loaded_df.shape}")
    
    return loaded_df

def database_basics():
    """Basic database operations for course prep"""
    print("\n=== DATABASE BASICS ===")
    
    # Create in-memory SQLite database
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            grade INTEGER,
            major TEXT
        )
    ''')
    
    # Insert data
    students = [
        (1, 'Alice', 85, 'CS'),
        (2, 'Bob', 92, 'Data Science'),
        (3, 'Charlie', 78, 'Engineering'),
        (4, 'Diana', 88, 'CS'),
        (5, 'Eve', 94, 'Data Science')
    ]
    
    cursor.executemany('INSERT INTO students VALUES (?, ?, ?, ?)', students)
    conn.commit()
    
    # Query data
    cursor.execute('SELECT major, AVG(grade) as avg_grade FROM students GROUP BY major')
    results = cursor.fetchall()
    
    print("Average grades by major:")
    for major, avg_grade in results:
        print(f"  {major}: {avg_grade:.2f}")
    
    conn.close()
    return results

def main():
    """Main execution function"""
    print("Python Fundamentals Review for Data Science Courses")
    print("=" * 50)
    
    # Run all reviews
    data_structures_review()
    analyzer = functions_and_classes()
    student_df = file_handling_practice()
    db_results = database_basics()
    
    # Final summary
    print("\n=== REVIEW COMPLETE ===")
    print("✅ Data structures and comprehensions")
    print("✅ Functions and classes")
    print("✅ File handling (JSON, CSV)")
    print("✅ Basic database operations")
    print("✅ Ready for advanced coursework!")
    
    return True

if __name__ == "__main__":
    success = main()
    print(f"\nReview completed successfully: {success}")