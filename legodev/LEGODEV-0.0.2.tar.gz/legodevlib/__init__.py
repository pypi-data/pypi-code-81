# Function to move the robot forward a certain distance 
def forward_movement(distance=155, speed=30, time=1):
 
    # Travel distance over 1 sec @ 30 speed: 155mm
    reference_dst = {"distance": 155, "speed": 30 , "time": 1}
 
    # Distance ratio calculation between given distance and reference distance
    distance_ratio = distance / reference_dst["distance"]
 
    # Speed ratio calculation between given distance and reference distance
    speed_ratio = speed / reference_dst["speed"]
 
    # Time needed to reach given distance with given speed 
    new_time = time * distance_ratio * speed_ratio
 
    # Ev3dev2 function call for simultaneous wheel movement
    steering_drive.on_for_seconds(0, speed, new_time)

# Function to move the robot backward a certain distance
def backward_movement(distance=155, speed=30, time=30):
 
    # Travel distance over 1 sec @ 30 speed: 155mm
    reference_dst = {"distance": 155, "speed": 30 , "time": 1}
 
    # Distance ratio calculation between given distance and reference distance
    distance_ratio = distance / reference_dst["distance"]
 
    # Speed ratio calculation between given distance and reference distance
    speed_ratio = speed / reference_dst["speed"]
 
    # Time needed to reach given distance with given speed 
    new_time = time * distance_ratio * speed_ratio
 
    # Ev3dev2 function call for simultaneous wheel movement
    steering_drive.on_for_seconds(0, -(speed), new_time)
 
 
# Function to turn the robot right on the spot
def right_turn_on_spot(angle=90, speed=30, time=0.83):
 
    # Turn angle over 0.5 sec @ 30 speed: 90 degrees
    reference_ast = {"angle": 90, "speed": 30, "time": 0.83}
 
    # Angle ratio calculation between given angle and reference angle
    angle_ratio = angle / reference_ast["angle"]
 
    # Speed ratio calculation between given distance and reference distance
    speed_ratio = speed / reference_ast["speed"]
 
    # Time needed to reach given turn angle with given speed 
    new_time = time * angle_ratio * speed_ratio
 
    # Ev3dev2 function call for on spot angular movement
    steering_drive.on_for_seconds(100, speed, new_time)
 
 
 
# Function to turn the robot left on the spot
def left_turn_on_spot(angle=90, speed=30, time=0.83):
 
    # Turn angle over 0.5 sec @ 30 speed: 90 degrees
    reference_ast = {"angle": 90, "speed": 30, "time": 0.83}
 
    # Angle ratio calculation between given angle and reference angle
    angle_ratio = angle / reference_ast["angle"]
 
    # Speed ratio calculation between given distance and reference distance
    speed_ratio = speed / reference_ast["speed"]
 
    # Time needed to reach given turn angle with given speed 
    new_time = time * angle_ratio * speed_ratio
 
    # Ev3dev2 function call for on spot angular movement
    steering_drive.on_for_seconds(-100, speed, new_time)
 
 
# Function to utilize the simple clothespin lift mechanism
def simple_clothespin(direction):
 
    # If direction parameter is "up", the pickup mechanic for the simple  clothespin lift will commence
    if direction == "up":
        largemotor.on_for_rotations(SpeedRPM(25), -0.8)
 
    # If direction parameter is "down", the dropoff mechanic for the simple clothespin lift will commence
    if direction == "down":
        largemotor.on_for_rotations(SpeedRPM(25), 0.8)
  
# Function to utilize the simple grab and lift mechanism
def simple_grablift(direction):
 
    # If direction parameter is "up", the pickup mechanic for the simple grab and lift claw will commence
    if direction == "up":
        largemotor.on_for_rotations(SpeedRPM(25), -0.8)
 
    # If direction parameter is "down", the dropoff mechanic for the simple grab and lift claw will commence
    if direction == "down":
        largemotor.on_for_rotations(SpeedRPM(25), 0.8)
 
 
# Function to utilize the simple forklift mechanism
def simple_forklift(direction):
 
    # If direction parameter is "up", the pickup mechanic for the simple forklift will commence
    if direction == "up":
        medmotor.on_for_rotations(SpeedRPM(100), -4) 
 
    # If direction parameter is "down", the dropoff mechanic for the simple forklift will commence
    if direction == "down":
        medmotor.on_for_rotations(SpeedRPM(100), 4) 
 
 
# Function to utilize the simple rake mechanism
def simple_rake(direction):
 
    # If direction parameter is "up", the lifting of the rake will commence
    if direction == "up":
        medmotor.on_for_rotations(SpeedRPM(25),0.4) 
 
    # If direction parameter is "down", the dropping of the rake will commence
    if direction == "down":
        medmotor.on_for_rotations(SpeedRPM(25), -0.4) 
 
# Function to utilize the simple claw mechanism
def simple_claw(action):
 
    # If action parameter is "close", the closing of the claw will commence
    if action == "close":
        medmotor.on_for_rotations(SpeedRPM(100), -8) 
 
    # If action parameter is "open", the opening of the claw will commence
    if action == "open":
        medmotor.on_for_rotations(SpeedRPM(100), 8) 
#Fucntion to return color based on sensor input
def determine_color(color_input):
    # If statements to categorize color by overall rgb values
    if color_input = 0:
        return None
    else if color_input = 1:
        return "black"
    else if color_input = 2:
        return "blue"
    else if color_input = 3:
        return "green"
    else if color_input = 4:
        return "yellow"
    else if color_input = 5:
        return "red"
    else if color_input = 6:
        return "white"
    else if color_input = 7:
        return "brown"


 
