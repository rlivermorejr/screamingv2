# Screaming (A TWITTER CLONE!!!)

- Poetry was used as package manager
<pre>pyproject.toml</pre>
<pre>requirements.txt</pre>
<pre>dev-requirements.txt</pre>

- Dependencies are listed in each
<hr>

## <u>Table of Contents</u>
<p style="font-size: 14px">Apps:</p>


- <b>auth_app</b>
  * Holds everything to do with logging in/out (forms, models, views)
  * Contains the user model < Account >
  * Handles index page
- <b>notify_app</b>
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

