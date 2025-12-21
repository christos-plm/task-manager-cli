# Edge Case Experiments - [2025.12.21]

## Experiment 1: Empty Inputs
**What I did:** Tried to add a task with no description
**What happened:** Task creates with empty description
**Should we fix this?** Yes. It creates garbage

## Experiment 2: Very Long Descriptions
**What I did:** Tried to add a task with a description over 100 characters
**What happened:** Task displays properly
**Observations:** How long description would be TOO long?

## Experiment 3: Special Characters
**What I did:** Tried to enter emojis, quotes and apostrophes in task description
**What happened:** No error messages appeared
**Surprising results:** Task creates normally and displays properly

## Experiment 4: Invalid Menu Choices
**What I did:** Tried to enter letters instead of numbers, negative or very large numbers, empty
**What happened:** Error message appeared
**Are error messages clear?** Yes. Error message asks user to enter 1-6

## Experiment 5: Empty Database
**What I did:** Deleted tasks.db
**What happened:** Program loads and starts fresh
**User experience issues?** When trying to display or alter task attributes, a message informs the user that there are no tasks yet

## Experiment 6: Database Corruption
**What I did:** Added random text into tasks.db
**What happened:** Program did not load
**Does it recover gracefully?** No

## Experiment 7: Many Tasks
**What I did:** Entered 50 tasks
**What happened:** Program works normally
**Usability issues?** Menu scrolling becomes annoying 

## Potential Improvements Identified
1. Reject empty task description
2. Handle error when DB is corrupted

## Things That Work Well
1. Invalid menu choices handler
2. Tasks display
3. Scaling