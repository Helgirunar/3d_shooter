# 3d_shooter
Assignment05 for TGRA

REQ:
pip install numpy
pip install PodSixNet

To run this:
1. Run the server via the python server.py command
2. Run the client via the python Control3DProgram.py <players_team> <Players_name>

if you want to test the multiplayer function:
1. Press P while still in the first client, so the mouse is not glued to the window. Move the window to the side.
2. Launch the client again (With a new name).
Now you should be able to see the other player move on your first/second screen depending on which one you're controlling.

To Do:
1. Have orientation of the guns be server side, so enemy and friendly players can see where you're aiming
    1. Add value to the servers data to handle the orientation
    2. Pass that data from and to the server if it changed
2. Have bullets be serverside
3. Improve collision (slide)
4. Extra