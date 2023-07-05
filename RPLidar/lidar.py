from rplidar import RPLidar
lidar = RPLidar('COM11')

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

for i, measurement in enumerate(lidar.iter_measures()):
    print('Angle: {} degrees'.format(int(measurement[2])))
    print('Distance {} mm'.format(measurement[3]))
    if i > 100:
        break
while True: 
    lidar.stop()
    lidar.stop_motor()
# lidar.disconnect()