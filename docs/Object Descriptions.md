# Object: DatabaseController
  Attributes:
    db_file: A string of the relative file path to the database.
    conn: A sqlite3 database connection object.
    cursor: A sqlite3 database cursor object.

  Methods:
    __len__: Get amount to tables in database
    __getitem__: Get table via index
    __getattr__: Get table via name using an attribute


# Object: Table
  Attributes:
    name: A string of the name of the table in the database.
    cursor: A cursor object for the database connection.

  Methods:
    __len__: Get amount of rows in table
    __getitem__: Get row object via index


# Object: Flask
  Attributes:
    import_name: The name of the application package.
    static_folder: A string of the path to the folder for static files.
    template_folder: A string of the path to the folder for HTML templates.

  Methods:
    logger: Create a python logger for the app.
    run: Creates a web server for testing during development.
    route: Used as a decorator to specify the url path.
