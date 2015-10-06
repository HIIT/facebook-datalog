from AppConfiguration import *

# create header
header = "Content-Type: text/html"
print(header)
print()

# create response content
print('''
<html>
    <title>fbalog Login</title>
    <body>
        <a href="https://www.facebook.com/dialog/oauth?clientd_id='''+APP_ID+"""&redirect_url="""+REDIRECT_URL'''&response_type=code&scope=user_likes,user_posts,user_status">Login to facebook</a>
    </body>
</html>
''')