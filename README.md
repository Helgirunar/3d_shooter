# 3d_shooter
Assignment05 for TGRA

REQ:
pip install numpy
pip install PodSixNet

To run this:
1. Run the server via the python server.py command
2. Run the client via the python Control3DProgram.py

if you want to test the multiplayer function:
1. Press P while still in the first client, so the mouse is not glued to the window. Move the window to the side.
2. Change your name and team in lines 33 and 34 and launch the client again.
Now you should be able to see the other player move on your first/second screen depending on which one you're controlling.

To Do:
1. Have orientation of the guns be server side, so enemy and friendly players can see where you're aiming
    1. Add value to the servers data to handle the orientation
    2. Pass that data from and to the server if it changed
2. Model for the player?
3. Have bullets be serverside
4. Tweak the respawn
    1. Currently, the spawns are weird, I noticed that red respawned on blue's spot.
5. Add walls and boxes
6. Extra