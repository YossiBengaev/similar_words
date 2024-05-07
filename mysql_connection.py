import mysql.connector


class DatabaseConnection:

    def __init__(self, host, database, user, password):
        try:
            self.connection = mysql.connector.connect(
                host=host, database=database, user=user, password=password
            )
            self.cursor = self.connection.cursor()
            print("Database connection established successfully.")
        except mysql.connector.Error as e:
            print("Error connecting to database:", e)

    def create_table(self):
        try:
            # Check if the 'words' table exists
            self.cursor.execute("SHOW TABLES LIKE 'words'")
            table_exists = self.cursor.fetchone()
            if table_exists:
                print("The table 'words' already exists.")
                return False  # Table already exists, return False

            # Create the 'words' table if it doesn't exist
            query = """
            CREATE TABLE words (
                word VARCHAR(255) NOT NULL,
                sorted_word VARCHAR(255) NOT NULL
            );
            """
            self.execute(query)
            print("Table 'words' created successfully.")
            return True  # Table created successfully, return True
        except mysql.connector.Error as e:
            print("Error creating table:", e)
            return False  # Return False if there's an error

    def insert_words_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                words = file.readlines()
                for word in words:
                    word = word.strip()
                    sorted_word = ''.join(sorted(word))
                    self.execute("INSERT INTO words (word, sorted_word) VALUES (%s, %s)",
                                 (word, sorted_word))
                self.commit()
                print("Word and sorted words inserted into the database successfully.")
        except Exception as e:
            print("Error inserting words into the database:", e)

    def execute(self, query, params=None):
        try:
            self.cursor.execute(query, params)
        except mysql.connector.Error as e:
            print("Error executing query:", e)

    def fetchall(self):
        try:
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print("Error fetching data:", e)

    def fetchone(self):
        try:
            return self.cursor.fetchone()
        except mysql.connector.Error as e:
            print("Error fetching one row:", e)

    def commit(self):
        try:
            self.connection.commit()
        except mysql.connector.Error as e:
            print("Error committing transaction:", e)

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")
        except mysql.connector.Error as e:
            print("Error closing database connection:", e)