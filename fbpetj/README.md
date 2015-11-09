FBPETJ fetches facebook events and public pages

How to use:

1. make sure you have python installed (it doesn't matter whether it's python2 or python3, both work)

2. make sure you have a facebook account to use with the program. You need to:
    1. Like the pages you want to get
    2. Mark the events you want to get either by 'going' to them or clicking the 'interested' button

3. Go to https://developers.facebook.com/docs/apps/register and do the 'create developer account' part.

4. Go to https://developers.facebook.com/tools/explorer
    1. Go to Get Token -> Get User Access Token
    2. Allow these permissions: user_likes user_events

5. In the input field there is by default written '/me?friends=id,name'. You need to:
    1. replace this with 'me/events?fields=id,name'. This is how you get ids for the events. if there's a next-link at the end of the list, click it tosee more of the events.
    2. In the folder where the code is located, find the file event_ids.txt. Put all the event id's you want to this file. NOTE: one id per one line. Nothing else! No empty lines!
    3. let's do the same for pages. In the input field, put 'me/likes?fields=id,name'
    4. Paste the id's to file page_ids.txt

6. Run the code by executing the file fetchEvents.py

7. When the code asks for access token, go back to https://developers.facebook.com/tools/explorer and copy-paste the code in the 'Access token' field

8. when the code finishes one page/event (this can take a lot of time, even several days if there's a lot of data), it creates a json file for it. Those can be safely used once they are created.

9. in case of errors, the program prints the error messages to console. In many cases they are not fatal, but if you think you are missing some data, you want to check them.



In case of comments, feedback, ideas, problems etc. feel free to contact me at jesper.hjorth@hiit.fi

