"""
Database Connection Module

This module provides functionality for connecting to and initializing an SQLite database
for storing experimental results. It creates a table structure for storing experiment types,
formulation IDs, and their corresponding calculated values.

Typical usage example:
    connection, cursor = connect_to_database("my_experiments.db")
    cursor.execute("INSERT INTO results VALUES (?, ?, ?)", ("experiment1", "form_A", 0.95))
    connection.commit()
    connection.close()

Dependencies:
    - sqlite3: Built-in Python module for SQLite database operations
"""

import sqlite3
import os

from typing import Tuple
from sqlite3 import Connection, Cursor

def connect_to_database() -> Tuple[Connection, Cursor]:
    """
    Establishes a connection to an SQLite database and initializes the results table.

    Databse path is fetched from LAB_APP_DB_PATH, defaulting to "results.db"

    This function performs the following operations:
    1. Creates a new SQLite database connection (or connects to existing database)
    2. Creates a cursor object for database operations
    3. Initializes a 'results' table if it doesn't exist
    4. Commits the table creation
    5. Returns the connection and cursor objects

    Returns:
        A tuple containing:
            - connection: SQLite database connection object
            - cursor: Database cursor object for executing SQL commands

    Table Schema:
        results:
            - experiment_type (TEXT): Type or category of the experiment
            - formulation_id (TEXT): Unique identifier for the formulation
            - calculated_value (REAL): Numerical result of the experiment

    Raises:
        sqlite3.Error: If there are issues connecting to the database or creating the table
        
    Example:
        >>> conn, cur = connect_to_database()
        >>> cur.execute("SELECT * FROM results")
        >>> results = cur.fetchall()
        >>> conn.close()
    """
    db = os.environ.get("LAB_APP_DB_PATH", "results.db")

    # Establish connection to the SQLite database
    connection: Connection = sqlite3.connect(db)
    
    # Create a cursor object to execute SQL commands
    cursor: Cursor = connection.cursor()
    
    # Create the results table if it doesn't exist
    # Using IF NOT EXISTS to prevent errors if table already exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results(
            experiment_type TEXT,    -- Type/category of experiment
            formulation_id TEXT,     -- Unique identifier for the formulation
            calculated_value REAL    -- Numerical result from the experiment
        )
    """)
    
    # Commit the table creation to save changes
    connection.commit()
    
    return (connection, cursor)