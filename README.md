# game
simple multiplayer game using pygame

### To run a server:

Have **banned.json** in the same folder as **server.py**
**banned.json** should be a list of IPs to block  
Run `python3 server.py`
The server will start on port 38491

### To run a server in a Docker container:

Run `docker compose up`

### To use a server:

Click on player names on the left to kick them  
Click on text on the right to clear lists if they get too big  
To close the server, close the window:  
- A warning will be sent in the server's chat immediately  
- After 1 second, the game logic will stop and all players will be kicked  
- after another 0.5 seconds, the server and any remaining connections will close  

### To run the client:

There are two ways to run the client, although the launcher is easiest

1) You can run `python3 launcher.py` to graphically change your config and connect to a server

2) Alternatively you can modify **config.json** directly and then run `python3 client.py` To do this you must have **config.json** in the same folder as **client.py**
**config.json** should look like this:  
`{`  
`    "HOST": "host IP",`  
`    "PORT": 38491 unless specified otherwise`  
`    "NAME": "your username"`  
`}`

  

Bear in mind, If **config.json** is not present in the same folder as **client.py**, it will be automatically created.
  
### To use the client:

WASD to move  
Click to shoot  
T to chat  
- ENTER to send  
- ESC to cancel  

Health is in the top left  
Rainbow squares are power-ups  
ESC to quit