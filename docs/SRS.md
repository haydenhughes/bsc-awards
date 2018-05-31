# Software Development 2017

# Software Requirements Specification Version 1, 2 and 3
# for BSC-Awards

1. Introduction
  1. Purpose and Users Characteristics'
      The software being developed is a front end and backend for a database of
      the awards and people for the BSC awards night. The only people using the
      software will be the award presenter to be calling out the awards from their
      device. Teachers shall be marking attendance using the attendance tracker.

2. Scope
  1. Items within Scope
    - Print out the attendance list by year level.
    - Only show students that have attended.
    - Dux award should not appear but will be in database.
    - Attendance Tracker button on main page.
    - Prompt reader to stop for applause after a certain amount of people.
    - Make the GUI responsive and touch friendly.
    - Show the name and home group of the inputted student code in the attendance tracker.

  2. Operating Environment
      The operating environment will in a stage setting with various devices including
      tablets and PCs forcing the design must be responsive. The operating systems
      and browser will vary depending on the make and model of the device and the users'
      preference so the application will need to be robust and flexible to be able to be used
      across devices.

3. Requirements
    - V1:
      - A database SQL connection to read and write data. (functional)
      - Award grouping. (functional)
      - Attendance tracking backend. (functional)
      - Functional unit testing. (non-functional)

    - V2:
      - A sass based css build system using libsass (non-functional)
      - Use the nord color scheme (non-functional)
      - A functional GUI to display the information from the database using Bootstrap. (functional)
      - Functional authentication. (functional)
      - Attendance tracking GUI. (non-functional)

    - V3:
      - Show image of student on attendance tracking page (non-functional)
      - Able to print attendance. (functional)

4. Constraints
    - Must be coded in Python.
    - Must use the Flask micro framework.
    - Must be able to read data from a SQL compatible database.
    - Time span.
    - Workforce.
    - Skills.

5. Use Case
    - UC1: Presenting the awards.
    - UC2: Marking attendance.
     NOTE: Both use cases are on the same diagram 

6. Appendix
  1. Data Collection
      - Interview people who will use the solution: This will provide opinions of how effective the software solution is from the people that use it.
