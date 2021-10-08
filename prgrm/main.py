import argparse
import csv
import sys
from time import time
import bosdyn.client.util
import argparse
import sys
import bosdyn.client
import bosdyn.client.estop
import bosdyn.client.lease
import bosdyn.client.util
from libs.circle import circle
from libs.takephoto import takePhoto
from libs.navigate_robot import move_robot



# args : 
#   - username
#   - password
#   - upload filepath
def main(argv):
    """Run the command-line interface."""
    parser = argparse.ArgumentParser(description=__doc__)
    bosdyn.client.util.add_common_arguments(parser)
    options = parser.parse_args(argv)

    # Setup and authenticate the robot.
    sdk = bosdyn.client.create_standard_sdk('MyClient')
    robot = sdk.create_robot(options.hostname)
    robot.authenticate(options.username, options.password)
    robot.time_sync.wait_for_sync()

    #listePoints = [[-1,0,0], [0, 1, 45]]
    listePoints = [[0.75, 1.5, 30]]
    i = 0

    for points in listePoints :
        # Se rend au waypoint
        if i == 0 :
            move_robot(robot, points[0], points[1], points[2], True)
        else :
            move_robot(robot, points[0], points[1], points[2], False)


        # Prend une photo 
        #takePhoto()
        #x, y = circle("../images/image.png")
        x = 0
        y = 0
        # S'il trouve un cercle il s'y rend
        if x != 0 and y != 0 :
            print("Circle was found, the robot will correct its position to be above the circle")
            # Ajuste sa position pour se mettre au dessus du cercle
            move_robot(robot, x, y, 0, False)
            # Marque une pause
            print("Faire relevé")
            time.sleep(10)
            # Reviens en arrière
            move_robot(robot, -x, -y, 0, False)

        else :
            print("No circle were found, the robot will continue its road")

        # Poursuis son chemin et va au point suivant 
         

    print("The robot has finished its road, it will now power off")

if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)