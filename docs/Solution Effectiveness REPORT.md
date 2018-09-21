# Solution Effectiveness REPORT

A list of solution requirements and how they are implemented.

- A database SQL connection to read and write data.
  - Implemented with `flask-sqlalchemy` in `get_awards` and `StudentManager`

- Award grouping.
  - Managing how people get grouped on stage is the job of `GroupManager` and is
    displayed using `MainView`'s `applause` screen.

- Attendance tracking backend.
  - Anything and everything student data related is managed by `StudentManager`
    including attendance.

- Functional unittesing.
  - All the unittests are in the `test` folder.

- A sass based css build system using libsass.
  - Yes I do have a sass build system although I'm using `gulp.js` as it is 
    a better solution then libsass. (using libsass wasn't really a requirement anyway)

- Use the nord color scheme.
  - This shouldn't really have be a requirement and I think the boostrap default color scheme
    works better in this case.

- A functional GUI to display the information from the database using Bootstrap.
 - Check. That is what the entire solution is.

- Attendance tracking GUI
 - Implemented by the `AttendanceView` using `StudentManager` as a database interface.

- Function authentication.
 - `LoginView` covers this using flask's `session` cookie. All the views first check
   to make sure your logged in before you can access the view.
   
- Able to print attendace.
 - Done with `PrintView` as well as `get_awards` to well.. get the awards, as well as
   `StudentManger` to get the students.
