# EntrACE
#### Video Demo:  https://youtu.be/UcI8SKbdF6c
#### Description:
This is a flask app that helps users preparing for a competitive exam in India, called JEE, from which they will be getting admission into prestigious institute for engineering in the country for examples IIT, NIT, IIIT,[I got into one of then called NIT Silchar, so I know the pain of being consistent, thats why I ma building my final Project on this topic], to monitor there progress and know how much chapter is left to done.

Technologies used:

- Python
- HTML
- CSS
- bootstrap
- sqlite3
- other small libraries or packages

## How the webpage works?

For new users, we have to reach to the register page. During registration you need to enter these fields:

- Username
- Password
- Re-Enter Password for cross checking

Then it will check that is the username provided is unique or not, if not then it will go to an apology page that username already exists.
It will save the user's record in the user table in the data.db database

For existing users, they can login via there username and password and then they can explore the rest of its features.

## Features

When logined or registered then the user will be taken to the homepage of the site, there the user will see a message from me that to keep grinding to achieve there goals, i.e to be selected in either IITs, NITs or IIITs, there the user will also find a navbar containing physics, chemistry, maths, add task, leaderboard and about

I have deleberatily made that about so that I can thanks David J. Malan for this providing all the teaching through all this course, again Thanks for it.

### Physics

Here the user will be able to see his tasks of physics that is to be completed, he can also un-done his completed tasks if the user feels the need of revision.

### Chemistry

Similiar to Physics, here the user will be able to see his tasks of Chemistry that is to be completed, he can also un-done his completed tasks if the user feels the need of revision.

### Maths

Similiarly, here also the user will be able to see his tasks of maths that is to be completed, he can also un-done his completed tasks if the user feels the need of revision.

### Add Task

Here The student can add some more tasks if he feel the require that some more tasks should be present in respective subjects.

### Database

In the database there are 4 table built in, users, physics, chemistry and maths, the first stores the data of the user and the rest of them stores the task related to there respective names.
In Users the 

### About

Gives the decription of me, where I belong and a special thanks to David J. Malan and Harvard University for providing this course free of cost.

## Possible improvements

As all applications this one can also be improved. Possible improvements:

- Power to change account details
- Make Groups for group study
- Addition of time in the tasks
- Notification via email if any task remain unfinished during a inputed time.
