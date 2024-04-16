import math

camera_height = 4.5
speed = 35.0
dist_to_light = 120.0
# 0 = green, 1 = yellow, 2 = red
light = 1


def miles_to_km(miles):
    return miles * 1.609344


def calc_dist_to_inter(dist):
    return math.sqrt(camera_height**2 - dist**2)


def min_brake_dist_ft(speed):
    kmh = miles_to_km(speed)
    meters = kmh**2 / (250 * 0.8)
    # distance in feet
    return meters * 3.28084


def gentle_warning():
    print('warning 😀')


def strong_warning():
    print("WARNING 😬")


def brake_warning(speed):
    brake_dist = min_brake_dist_ft(speed)
    if (light > 0):
        if (brake_dist < dist_to_light):
            gentle_warning()
        else:
            strong_warning()


min_dist = min_brake_dist_ft(speed)
print(f'{min_brake_dist_ft(speed)} ft')

brake_warning(speed)
