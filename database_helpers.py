import sqlite3
def connect_to_database(db = "results.db"):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS results(experiment_type TEXT, formulation_id TEXT, calculated_value REAL)")
    connection.commit()
    return (connection, cursor)
