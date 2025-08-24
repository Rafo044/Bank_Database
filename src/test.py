from database import DataBase
from insert_functions import insert_all
from time import process_time

# Create a database with the provided example data and print the time taken in seconds.

start_time = process_time()
insert_all()
print(f"Time taken: {process_time() - start_time} seconds")