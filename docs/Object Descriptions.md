# Object: DatabaseController
## Properties:
  File: dbtools.py
  Called via context manager

## Methods:
  __len__: Get amount to tables in database
  __getitem__: Get table via index
  __getattr__: Get table via name using an attribute
  cursor: return cursor object for database connection

# Object: Table
## Methods:
  __len__: Get amount of rows in table
  __getitem__: Get row object via index
