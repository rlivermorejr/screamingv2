# Screaming (A TWITTER CLONE!!!)

- Poetry was used as package manager
<pre>pyproject.toml</pre>
<pre>requirements.txt</pre>
<pre>dev-requirements.txt</pre>

- Dependencies are listed in each
<hr>

### TO START:

<span><i>
1. If in VSCode, rightclick readme file and click 'open preview'
2. Click terminal/open terminal and install dependencies, I used poetry so for example 'poetry install' will install all dependencies in pyproject.toml
  2a. If you do not have poetry then there is a requirements.txt you can use to install the dependencies
3. After the install, run 'python manage.py runserver'
4. In your web browser type '127.0.0.1:8000' in the address bar and you can now create a profile and access the site
</i></span>

<hr>

## <u>Table of Contents</u>

<p style="font-size: 16px">Folder Tree:</p>

- <b>auth_app</b>
  * Holds everything to do with logging in/out (forms, models, views)
  * Contains the user model < Account >
  * Handles index page
- <b>notification_app</b>
  * Contains all views for creating notifications
  * Those views are called in other apps as needed
  * Contains the notification model < Notification >
- <b>post_app</b>
  * Contains everything needed for posting
  * Holds the post model < ScreamModel > and the model for comments < CommentModel >
  * Has the forms needed for posting < ScreamForm > and commenting < CommentForm >
  * All views for posting and commenting
- <b>user_app</b>
  * This app handles editing user profile, getting data from the user model, following other users, and comments
  * Contains edit profile form < EditProfile > and search form < SearchProfile >

## Features not yet implemented
 - Search for other users
 - <b><u>Everything is set up to connect to MongoDB, I just have it all commented out while I am still editing the models.</u></b>

## Currently working on:
- insensitive username logic
- Upload different profile image

