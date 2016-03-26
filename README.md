dou6le6
=======

Run "python main.py" to start the webserver. To access the page, go to the url provided within the terminal after running main.py. To read the contents of a game, go to "/game/<game_id>" and the corresponding info will show up. If any packages are missing, please be sure to install them:

sudo pip install python-firebase

sudo pip install Flask



USEFUL FOR SETTING UP SERVER!
====

http://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/



Try it out!
====

For example, try out:

http://localhost:5000/game/1056787448

(Assuming your webserver is running on port 5000)



IMPORTANT:
====

If you plan on using this code, three edits need to be made:

1) templates/game.html   

Need to find the 2 occurrences of “ENTER-SERVER-IP-HERE” and replace them with your server IP.


2,3) test.py & dou6le6.py

Need change the CAPS string entries to actual firebase values relevant to your account.

firebase_url = 'https://ENTER-ACCOUNT-NAME-HERE.firebaseio.com/'

firebase_db = '/ENTER-DB-NAME-HERE'

