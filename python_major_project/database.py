# import mysql.connector
# from mysql.connector import Error


# class Database:

#     def __init__(self):

#         self.config = {
#             "host": "localhost",
#             "port": 3306,
#             "user": "root",
#             "password": "Shivansh1234@@"
#         }

#         self.database_name = "student_complaint_db"

#         self.create_database()

#     def create_database(self):

#         connection = None
#         cursor = None

#         try:
#             connection = mysql.connector.connect(**self.config)
#             cursor = connection.cursor()

#             cursor.execute(
#                 f"CREATE DATABASE IF NOT EXISTS {self.database_name}"
#             )

#             cursor.execute(f"USE {self.database_name}")

#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS students (
#                     student_id VARCHAR(30) PRIMARY KEY,
#                     name VARCHAR(100) NOT NULL,
#                     password_hash VARCHAR(255) NOT NULL,
#                     course VARCHAR(50) NOT NULL,
#                     course_year INT NOT NULL,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """)

#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS admins (
#                     admin_id INT AUTO_INCREMENT PRIMARY KEY,
#                     username VARCHAR(50) NOT NULL UNIQUE,
#                     password_hash VARCHAR(255) NOT NULL,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """)

#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS complaints (
#                     complaint_id INT AUTO_INCREMENT PRIMARY KEY,
#                     student_id VARCHAR(30) NOT NULL,
#                     complaint_title VARCHAR(150) NOT NULL,
#                     complaint_description TEXT NOT NULL,
#                     status ENUM(
#                         'Pending',
#                         'In Progress',
#                         'Solved'
#                     ) NOT NULL DEFAULT 'Pending',
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                         ON UPDATE CURRENT_TIMESTAMP,
#                     FOREIGN KEY (student_id)
#                         REFERENCES students(student_id)
#                 )
#             """)

#             connection.commit()

#             print("Database and tables are ready!")

#         except Error as e:
#             print("Database Setup Error:", e)

#         finally:
#             if cursor is not None:
#                 cursor.close()

#             if connection is not None:
#                 connection.close()

#     def connect(self):

#         try:
#             config = self.config.copy()
#             config["database"] = self.database_name

#             return mysql.connector.connect(**config)

#         except Error as e:
#             print("Database Connection Error:", e)
#             return None

#     def execute_query(self, query, params=(), fetch=None):

#         connection = self.connect()

#         if connection is None:
#             return None

#         cursor = None

#         try:
#             cursor = connection.cursor(dictionary=True)
#             cursor.execute(query, params)

#             if fetch == "one":
#                 return cursor.fetchone()

#             if fetch == "all":
#                 return cursor.fetchall()

#             connection.commit()
#             return cursor.rowcount

#         except Error as e:
#             connection.rollback()
#             print("Database Error:", e)
#             return None

#         finally:
#             if cursor is not None:
#                 cursor.close()

#             connection.close()

#     def admin_exists(self):

#         result = self.execute_query(
#             "SELECT COUNT(*) AS total FROM admins",
#             fetch="one"
#         )

#         if result is None:
#             return None

#         return result["total"] > 0

#     def create_admin(self, username, password_hash):

#         return self.execute_query(
#             """
#             INSERT INTO admins (username, password_hash)
#             VALUES (%s, %s)
#             """,
#             (username, password_hash)
#         )

#     def get_admin(self, username):

#         return self.execute_query(
#             "SELECT * FROM admins WHERE username = %s",
#             (username,),
#             fetch="one"
#         )

#     def create_student(
#         self,
#         student_id,
#         name,
#         password_hash,
#         course,
#         course_year
#     ):

#         return self.execute_query(
#             """
#             INSERT INTO students
#             (student_id, name, password_hash, course, course_year)
#             VALUES (%s, %s, %s, %s, %s)
#             """,
#             (student_id, name, password_hash, course, course_year)
#         )

#     def get_student(self, student_id):

#         return self.execute_query(
#             "SELECT * FROM students WHERE student_id = %s",
#             (student_id,),
#             fetch="one"
#         )

#     def get_all_students(self):

#         return self.execute_query(
#             """
#             SELECT student_id, name, course, course_year, created_at
#             FROM students
#             ORDER BY created_at DESC
#             """,
#             fetch="all"
#         )

#     def create_complaint(self, student_id, title, description):

#         return self.execute_query(
#             """
#             INSERT INTO complaints
#             (student_id, complaint_title, complaint_description)
#             VALUES (%s, %s, %s)
#             """,
#             (student_id, title, description)
#         )

#     def get_complaints(self, student_id=None, status=None):

#         query = """
#             SELECT
#                 c.complaint_id,
#                 c.student_id,
#                 s.name,
#                 c.complaint_title,
#                 c.complaint_description,
#                 c.status,
#                 c.created_at,
#                 c.updated_at
#             FROM complaints c
#             JOIN students s ON c.student_id = s.student_id
#         """

#         conditions = []
#         params = []

#         if student_id is not None:
#             conditions.append("c.student_id = %s")
#             params.append(student_id)

#         if status is not None:
#             conditions.append("c.status = %s")
#             params.append(status)

#         if conditions:
#             query += " WHERE " + " AND ".join(conditions)

#         query += " ORDER BY c.created_at DESC"

#         return self.execute_query(
#             query,
#             tuple(params),
#             fetch="all"
#         )

#     def update_complaint_status(self, complaint_id, status):

#         return self.execute_query(
#             """
#             UPDATE complaints
#             SET status = %s
#             WHERE complaint_id = %s
#             """,
#             (status, complaint_id)
#         )


import mysql.connector

from mysql.connector import Error
from typing import Any, Optional, TypedDict, cast


class QueryRow(TypedDict, total=False):
    student_id: str
    name: str
    password_hash: str
    course: str
    course_year: int
    username: str
    admin_id: int
    total: int
    complaint_id: int
    complaint_title: str
    complaint_description: str
    status: str
    created_at: Any
    updated_at: Any


class Database:

    def __init__(self):

        self.host = "localhost"
        self.port = 3306
        self.user = "root"

        # Apna MySQL password yahan set karo.
        self.password = "Shivansh1234@@"

        self.database_name = "student_complaint_db"

        self.create_database()

    # --------------------------------------------------
    # CREATE DATABASE AND TABLES
    # --------------------------------------------------

    def create_database(self) -> None:

        connection = None
        cursor = None

        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password
            )

            cursor = connection.cursor()

            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{self.database_name}`"
            )

            cursor.execute(
                f"USE `{self.database_name}`"
            )

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id VARCHAR(30) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    course VARCHAR(50) NOT NULL,
                    course_year INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    admin_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS complaints (
                    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id VARCHAR(30) NOT NULL,
                    complaint_title VARCHAR(150) NOT NULL,
                    complaint_description TEXT NOT NULL,
                    status ENUM(
                        'Pending',
                        'In Progress',
                        'Solved'
                    ) NOT NULL DEFAULT 'Pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id)
                        REFERENCES students(student_id)
                )
            """)

            connection.commit()

            print("Database and tables are ready!")

        except Error as error:
            print("Database Setup Error:", error)

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None and connection.is_connected():
                connection.close()

    # --------------------------------------------------
    # DATABASE CONNECTION
    # --------------------------------------------------

    def connect(self):

        try:
            return mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database_name
            )

        except Error as error:
            print("Database Connection Error:", error)
            return None

    # --------------------------------------------------
    # COMMON QUERY FUNCTION
    # --------------------------------------------------

    def execute_query(
        self,
        query: str,
        params: tuple[Any, ...] = (),
        fetch: Optional[str] = None
    ) -> Any:

        connection = self.connect()

        if connection is None:
            return None

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, params)

            if fetch == "one":
                result = cursor.fetchone()

                if result is None:
                    return None

                return cast(QueryRow, result)

            if fetch == "all":
                result = cursor.fetchall()
                return cast(list[QueryRow], result)

            connection.commit()

            return cursor.rowcount

        except Error as error:
            connection.rollback()
            print("Database Error:", error)
            return None

        finally:
            if cursor is not None:
                cursor.close()

            if connection.is_connected():
                connection.close()

    # --------------------------------------------------
    # CHECK ADMIN
    # --------------------------------------------------

    def admin_exists(self) -> Optional[bool]:

        result = self.execute_query(
            "SELECT COUNT(*) AS total FROM admins",
            fetch="one"
        )

        if result is None:
            return None

        total = result["total"]

        if not isinstance(total, int):
            return None

        return total > 0

    # --------------------------------------------------
    # CREATE ADMIN
    # --------------------------------------------------

    def create_admin(
        self,
        username: str,
        password_hash: str
    ) -> Any:

        return self.execute_query(
            """
            INSERT INTO admins (username, password_hash)
            VALUES (%s, %s)
            """,
            (username, password_hash)
        )

    # --------------------------------------------------
    # GET ADMIN
    # --------------------------------------------------

    def get_admin(self, username: str) -> Optional[QueryRow]:

        return self.execute_query(
            "SELECT * FROM admins WHERE username = %s",
            (username,),
            fetch="one"
        )

    # --------------------------------------------------
    # REGISTER STUDENT
    # --------------------------------------------------

    def create_student(
        self,
        student_id: str,
        name: str,
        password_hash: str,
        course: str,
        course_year: int
    ) -> Any:

        return self.execute_query(
            """
            INSERT INTO students (
                student_id,
                name,
                password_hash,
                course,
                course_year
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                student_id,
                name,
                password_hash,
                course,
                course_year
            )
        )

    # --------------------------------------------------
    # GET STUDENT
    # --------------------------------------------------

    def get_student(
        self,
        student_id: str
    ) -> Optional[QueryRow]:

        return self.execute_query(
            "SELECT * FROM students WHERE student_id = %s",
            (student_id,),
            fetch="one"
        )

    # --------------------------------------------------
    # GET ALL STUDENTS
    # --------------------------------------------------

    def get_all_students(self) -> Optional[list[QueryRow]]:

        return self.execute_query(
            """
            SELECT
                student_id,
                name,
                course,
                course_year,
                created_at
            FROM students
            ORDER BY created_at DESC
            """,
            fetch="all"
        )

    # --------------------------------------------------
    # SUBMIT COMPLAINT
    # --------------------------------------------------

    def create_complaint(
        self,
        student_id: str,
        title: str,
        description: str
    ) -> Any:

        return self.execute_query(
            """
            INSERT INTO complaints (
                student_id,
                complaint_title,
                complaint_description
            )
            VALUES (%s, %s, %s)
            """,
            (student_id, title, description)
        )

    # --------------------------------------------------
    # GET COMPLAINTS
    # --------------------------------------------------

    def get_complaints(
        self,
        student_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> Optional[list[QueryRow]]:

        query = """
            SELECT
                c.complaint_id,
                c.student_id,
                s.name,
                c.complaint_title,
                c.complaint_description,
                c.status,
                c.created_at,
                c.updated_at
            FROM complaints c
            JOIN students s
                ON c.student_id = s.student_id
        """

        conditions: list[str] = []
        params: list[Any] = []

        if student_id is not None:
            conditions.append("c.student_id = %s")
            params.append(student_id)

        if status is not None:
            conditions.append("c.status = %s")
            params.append(status)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY c.created_at DESC"

        return self.execute_query(
            query,
            tuple(params),
            fetch="all"
        )

    # --------------------------------------------------
    # UPDATE COMPLAINT STATUS
    # --------------------------------------------------

    def update_complaint_status(
        self,
        complaint_id: int,
        status: str
    ) -> Any:

        return self.execute_query(
            """
            UPDATE complaints
            SET status = %s
            WHERE complaint_id = %s
            """,
            (status, complaint_id)
        )