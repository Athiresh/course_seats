import psycopg2
import os
from rapidfuzz import fuzz
from dotenv import load_dotenv

load_dotenv()
def get_total_seats(course_name):
    try:
        conn = psycopg2.connect(database=os.getenv('DB_NAME'),
                                user=os.getenv('DB_USER'),
                                host=os.getenv('DB_HOST'),
                                password=os.getenv('DB_PASS'),
                                port=os.getenv('DB_PORT'))

        cursor = conn.cursor()
        table_name = os.getenv('DB_TABLE')
        cursor.execute(f"SELECT college_id, college, course_details FROM {table_name}")
        colleges = cursor.fetchall()

        college_course = []
        course_key = course_name.strip().lower()

        for college in colleges:
            college_id, college_name, course_details = college

            for course in course_details:
                course_name_db = course.get('course', '').lower()
                if fuzz.token_set_ratio(course_key, course_name_db) >= 85:
                    college_course.append(college_id)
                    break

        total_seats = len(college_course)

        cursor.close()
        conn.close()

        return total_seats

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return None

if __name__ == "__main__":
    try:
        while True:
            course_name = input('Enter the course name to search (or enter "exit" to quit): ').strip()

            if course_name.lower() == 'exit':
                break

            if not course_name:
                raise ValueError("Course name cannot be empty. Please try again.")

            no_of_seats = get_total_seats(course_name)

            if no_of_seats is not None:
                print(f"The total number of colleges offering {course_name.upper()} is {no_of_seats}.")
            else:
                print(f"No information available for {course_name.upper()}.")

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")
