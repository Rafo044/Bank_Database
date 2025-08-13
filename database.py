import sqlite3
import os
import os.path
from string import ascii_letters

class DataBase():

    def __init__(self, name: str = "example.db"):
        """Create a new database."""

        self.name = name
        self.check_existance()
        self.__db = sqlite3.connect(name)

    def create_tables(self):
        """Create all the tables of the database."""

        self.__db.executescript("""
                                
            CREATE TABLE Example
            (
                id          INTEGER PRIMARY KEY,
                number      INTEGER,
                string      TEXT                    
            );
                                """)

    def check_existance(self):
        """Check whether a database exists with the given filename."""

        if os.path.exists(self.name):
            os.remove(self.name)

class Query():

    def __init__(self, db: DataBase):
        """Run queries on a database."""

        self.__db = sqlite3.connect(db.name)

    def add_test(self,number: int, string: str):
        """Add testing."""

        query = """
        INSERT INTO Example(number, string) VALUES (?,?)
        """
        id = self.__db.execute(query,[number,string])
        return id

    def query_test(self):
        """Query testing."""

        query = """
        SELECT * FROM Example
        """
        results = self.__db.execute(query).fetchall()
        return results

if __name__ == "__main__":
    
    db = DataBase()
    db.create_tables()
    q = Query(db)

    for i, letter in enumerate(ascii_letters):
        q.add_test(int((i+1)*10),letter)

    print(q.query_test())