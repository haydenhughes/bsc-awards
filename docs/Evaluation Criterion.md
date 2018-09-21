# Evaluation Criterion

- Can mark attendance of students.
- Application will only use students that are present.
- Prompts the speaker to pause for applause after calling a reasonable amount of students onto stage.

# Acceptance testing
Does the solution meet the requirements of the SRS?
  Identify main requirements in the SRS and check that they are addressed in the final solution.

Does the solution produce accurate and expected results?
  Verify the information produced by the solution by manual checking and unit testing.

Is the interface intuitive to users?
  Interview users to gain feedback on the ease of use of the interface on multiple devices.
  
  
# Strategy to assess each solution evaluation criteria
1. Meet up with users of the final solution and ask about any problems with the solution.
2. Work out if the problems are caused by marking of attendance, using students that are absent or missing students that are present or too many and/or not enough students are on the stage at once.
   If user error then investigate ways to mitigate the user error.
3. Determine if the problems found in stage 2 can be replicated, if so then fix the errors, make sure unittests pass, merge into staging and release a update.

