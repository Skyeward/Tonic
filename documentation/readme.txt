pymysql is the only required installation:
pip install pymysql

run the app with: 
python -m tonic_app

The app only takes input from Twitch. In the TwitchData class, the socket information
will need to be updated to your Twitch account settings.

An auth key will need to be requested from Twitch via their website. This is
free and instantly obtainable.

Currently, the bot will time out if no commands are received for a certain period
(~1 minute). At this point, the app will be unresponsive and can only be closed
by force quitting the terminal.