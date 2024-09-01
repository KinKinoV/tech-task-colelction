# Improvement plan for the flaskExample application

Developed application ([link](https://github.com/KinKinoV/cloudfresh-test-task)) in the first part of this technical task is very simple and consists of only one index page and authentication system. This makes flaskExample application something akin wet clay that can become anything, result depends only from the creator.

It also has several flaws in the form of absense of form validation and using raw SQL while working with acquired user data. TO remove these flaws I propose doing this:

## Form validation

To implement form validation I would like to use [WTForms](https://wtforms.readthedocs.io/en/3.1.x/) Python library that will allow to effortlessly validate all of the fields in POSTed forms from the users. 
This improvement will drastically improve security of the application by denying any improperly inputed data from the user in forms.

## Raw SQL

To simplify and secure usage of the raw sql from the project I would like to use [SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) Python library. This library has powerfull tools that allows to abstract from much of the SQL and write all interactions with the DB almost by using only Python programing language.
This improvement will allow to write much more secure code for the DB interactions and also it will automatically validate all data before pushing it into the database.

# New features for the flaskExample

Personally, I would've liked to make flaskExmaple a simple blog with post, comment and notification systems. Implementing them wouldn't require use of any new tools or libraries, I will just need to create new logic for the application required for the mentioned features. 
- For posts I will need to create new table in the DB and will show all posts to the user on their homepage.
- For comments, I will need to do the same thing, as for the post system.
- For notification system I can send new information about the blog to the user's e-mail address.
