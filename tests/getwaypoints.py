import os

listeWayPoint = [ f for f in os.listdir('../test_4.walk/waypoint_snapshots') if os.path.isfile(os.path.join('../test_4.walk/waypoint_snapshots',f)) ]
del listeWayPoint[0]
print(listeWayPoint)