## To make me run:

- Change secrets.example to secrets. Replace the token in discord with the application secret you're using,
 and replace firebasekey.json with a private key generated at settings/serviceaccounts/adminsdk on the 
 firebase panel.

- Change info in instance.example/config.py to be correct for your usecase, and then rename folder to instance.

- Add the location of firebasekey.json to the enviroment as GOOGLE_APPLICATION_CREDENTIALS.

## What I have:
I've currently got a oauth handshake going, which creates a relevant record in the firebase database, and
updates it on each login. I've also included messages when errors occur during the process which would
hopefully be helpful, and a basic logout function. 
I also added a function before every request which tries to add a request.user object for future use.
Database functionality isn't really a thing yet.
