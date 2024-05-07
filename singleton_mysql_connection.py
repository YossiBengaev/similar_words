import mysql.connector


class MySQLConnection:
    _instance = None
    _connection = None

    def __new__(cls, host, database, user, db_password, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connect(host, database, user, db_password)
            cls._instance.create_table("words_s", "word VARCHAR(255) NOT NULL, sorted_word VARCHAR(255) NOT NULL")
            cls._instance.create_table("count_request", "counter INT NOT NULL")
            cls._instance.insert_words_from_file("./words_dataset.txt")
        return cls._instance

    def connect(self, host, database, user, db_password):
        if self._connection is None:
            self._connection = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=db_password
            )

        return self._connection

    def create_table(self, table_name, columns):
        try:
            cursor = self._connection.cursor()
            # Construct the CREATE TABLE query
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            cursor.execute(query)
            print(f"Table '{table_name}' created successfully.")
            cursor.close()
        except mysql.connector.Error as e:
            print("Error creating table:", e)

    def insert_words_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                words = file.readlines()
                cursor = self._connection.cursor()
                for word in words:
                    word = word.strip()
                    sorted_word = ''.join(sorted(word))
                    query = "INSERT INTO words_s (word, sorted_word) VALUES (%s, %s)"
                    cursor.execute(query, (word, sorted_word))
                self._connection.commit()
                print("Words inserted into the database successfully.")
        except Exception as e:
            print("Error inserting words into the database:", e)

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            