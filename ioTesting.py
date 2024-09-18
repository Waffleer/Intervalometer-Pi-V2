from fastapi import FastAPI
import time
# import RPi.GPIO as GPIO
#python -m fastapi dev ioControllerAPI.py --host 127.0.0.1 --port 9000


picturesTaken = -1
pictureLength = -1
delayLength = -1
totalPictures = -1
shutterType = "s"
bulb = False
sequenceRunning = False

focus_relay_status = False
shutter_relay_status = False
led_1_status = False

# Settings
shutter_timer = .1
focus_timer = .1
shutter_standard_bulb_delay = .04
shutter_quiet_bulb_delay = .1

shutter_standard_delay = .3
shutter_quiet_delay = 1



app = FastAPI()
# GPIO.setmode(GPIO.BOARD)


#Set output pins
shutterPin = 18
focusPin = 16
led = 0

# GPIO.setup(shutterPin, GPIO.OUT)
# GPIO.setup(focusPin,GPIO.OUT)
print("GPIO Setup Done")


# take image sequence
# imputs
#   pictureLength
#   totalPictures
#Process
#   Takes pictures
#   Updates picturesTaken
# Returns
#   Success or Failure

# Standard Mode

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/imageSequence/pictureLength/{pictureLength_}/delayLength/{delayLength_}/totalPictures/{totalPictures_}/shutterType/{shutterType_}")
def imageSequence(pictureLength_: float, delayLength_: float, totalPictures_: int, shutterType_: str):
    global picturesTaken
    global pictureLength
    global delayLength
    global totalPictures
    global shutterType
    global bulb

    global focus_relay_status
    global shutter_relay_status

    global shutter_timer
    global focus_timer

    global shutter_standard_delay
    global shutter_quiet_delay

    global sequenceRunning

    if(sequenceRunning == True):
        return {
            "status" : False, 
            "Error": "another sequence was running (sequenceRunning = True)",
            }
    

    sequenceRunning = True
    bulb = False
    picturesTaken = 0
    pictureLength = pictureLength_
    delayLength = delayLength_
    totalPictures = totalPictures_
    shutterType = shutterType_

    addDelay = 0.0
    if shutterType == "q":
        addDelay = shutter_quiet_delay
    else:
        addDelay = shutter_standard_delay
    totalDelay = pictureLength+delayLength_+addDelay
        
    # Turn on focus
    # GPIO.output(focusPin, GPIO.HIGH)
    focus_relay_status = True

    # Focus delay
    time.sleep(focus_timer)

    # For each picture
    for picture in range(1, totalPictures):
        # Take picture / Toggle Shutter Relay
        # GPIO.output(shutterPin, GPIO.HIGH)
        time.sleep(shutter_timer)
        # GPIO.output(shutterPin, GPIO.LOW)
        # Count Picture
        picturesTaken = picturesTaken+1
        print(picturesTaken)
        #Picture Delay
        time.sleep(totalDelay)
    # Last Picture No Delay
    # GPIO.output(shutterPin, GPIO.HIGH)
    time.sleep(shutter_timer)
    # GPIO.output(shutterPin, GPIO.LOW)
    picturesTaken = picturesTaken+1
    print(picturesTaken)

    # Turn off Focus
    # GPIO.output(focusPin, GPIO.LOW)
    focus_relay_status = False
    sequenceRunning = False

    return {"status": True}

# Bulb Mode
@app.get("/imageSequenceBulb/pictureLength/{pictureLength_}/delayLength/{delayLength_}/totalPictures/{totalPictures_}/shutterType/{shutterType_}")
def imageSequenceBulb(pictureLength_: float, delayLength_: float, totalPictures_: int, shutterType_: str):
    global picturesTaken
    global pictureLength
    global delayLength
    global totalPictures
    global shutterType
    global bulb

    global focus_relay_status
    global shutter_relay_status

    global shutter_timer
    global focus_timer

    global shutter_standard_delay
    global shutter_standard_bulb_delay
    global shutter_quiet_delay
    global shutter_quiet_bulb_delay

    global sequenceRunning

    if(sequenceRunning == True):
        return {
            "status" : False, 
            "Error": "another sequence was running (sequenceRunning = True)",
            }

    sequenceRunning = True
    bulb = True
    picturesTaken = 0
    pictureLength = pictureLength_
    delayLength = delayLength_
    totalPictures = totalPictures_

    addDelay = 0.0
    if shutterType == "q":
        addDelay = shutter_quiet_delay + shutter_quiet_bulb_delay
    else:
        addDelay = shutter_standard_delay + shutter_standard_bulb_delay
    totalDelay = delayLength+addDelay

    
    # Turn on focus
    # GPIO.output(focusPin, GPIO.HIGH)
    focus_relay_status = True

    # Focus delay
    time.sleep(focus_timer)

    # For each picture
    for picture in range(1, totalPictures):
        # Take picture / Toggle Shutter Relay
        # GPIO.output(shutterPin, GPIO.HIGH)
        time.sleep(pictureLength)
        # GPIO.output(shutterPin, GPIO.LOW)
        # GPIO.output(focusPin,GPIO.LOW)
        # Count Picture
        picturesTaken = picturesTaken+1
        print(picturesTaken)
        time.sleep(totalDelay-focus_timer)
        # GPIO.output(focusPin, GPIO.HIGH)
        time.sleep(focus_timer)

    # Last Picture No Delay
    # Take picture / Toggle Shutter Relay
    # GPIO.output(shutterPin, GPIO.HIGH)
    time.sleep(pictureLength)
    # GPIO.output(shutterPin, GPIO.LOW)
    # Count Picture
    picturesTaken = picturesTaken+1
    print(picturesTaken)

    # Turn off Focus
    # GPIO.output(focusPin, GPIO.LOW)
    focus_relay_status = False
    sequenceRunning = False
    bulb = False

    return {"status": True}

# Clicking mode
@app.get("/click/bulb/{bulb_}")
def imageSequence(bulb_: int):
    global bulb

    global focus_relay_status
    global shutter_relay_status

    global shutter_timer
    global focus_timer

    global shutter_standard_delay
    global shutter_quiet_delay

    if(sequenceRunning == True):
        return {
            "status" : False, 
            "Error": "another sequence was running (sequenceRunning = True)",
            }        
        
    # Turn on focus
    # GPIO.output(focusPin, GPIO.HIGH)
    focus_relay_status = True
    # Focus delay
    time.sleep(focus_timer)

    # Picture No Delay
    # Non bulb mode
    # GPIO.output(shutterPin, GPIO.HIGH)
    time.sleep(shutter_timer)
    # GPIO.output(shutterPin, GPIO.LOW)

    # Turn off Focus
    # GPIO.output(focusPin, GPIO.LOW)
    focus_relay_status = False

    return {"status": True}


#Return picturesTaken
@app.get("/return/picturesTaken")
def returnPicturesTaken():
    global picturesTaken
    return {"picturesTaken": picturesTaken}

@app.get("/return/sequenceInfo")
def returnSequenceInfo():
    global pictureLength
    global delayLength
    global totalPictures
    global shutterType
    global bulb
    return {
        "pictureLength": pictureLength,
        "delayLength": delayLength,
        "totalPictures": totalPictures,
        "shutterType": shutterType,
        "bulb": bulb,
    }











# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

#Activate Relay 1 (Shutter)
#Deactivate Relay 1 (Shutter)
#Click Relay 1 (on -> off)
#Return Relay 1 Status

#Activate Relay 2 (Focus)
#Deactivate Relay 2 (Focus)
#Click Relay 2 (on -> off)
#Return Relay 2 Status

#Activate Led 1 (on)
#Activate Led 1 (off)
#Return Led 1 Status

# #Return picturesTaken
# @app.get("/return/picturesTaken")
# def returnPicturesTaken():
#     global picturesTaken
#     return {"picturesTaken": picturesTaken}

# #Return pictureLength
# @app.get("/return/pictureLength")
# def returnPictureLength():
#     global pictureLength
#     return {"pictureLength": pictureLength}

# #Return totalPictures
# @app.get("/return/totalPictures")
# def returnTotalPictures():
#     global totalPictures
#     return {"totalPictures": totalPictures}

# #Return picturesTaken pictureLength totalPictures
# @app.get("/return/picturesTaken-pictureLength-totalPictures")
# def returnTotalPictures():
#     global picturesTaken
#     global pictureLength
#     global totalPictures
#     return {
#         "picturesTaken": picturesTaken,
#         "pictureLength": pictureLength,
#         "totalPictures": totalPictures,
#         }

# #Return bulb

# #Set picturesTaken
# @app.get("/set/picturesTaken/{picturesTaken_}")
# def setPicturesTaken(picturesTaken_: int):
#     global picturesTaken
#     try:
#         picturesTaken = picturesTaken_
#     except:
#         return {"status": False}
#     return {"status": True}

# #Set pictureLength
# @app.get("/set/pictureLength/{pictureLength_}")
# def setPictureLength(pictureLength_: int):
#     global pictureLength
#     try:
#         pictureLength = pictureLength_
#     except:
#         return {"status": False}
#     return {"status": True}

# #Set totalPictures
# @app.get("/set/totalPictures/{totalPictures_}")
# def setTotalPictures(totalPictures_: int):
#     global totalPictures
#     try:
#         totalPictures = totalPictures_
#     except:
#         return {"status": False}
#     return {"status": True}

# #Set picturesTaken, pictureLength, totalPictures
# @app.get("/set/picturesTaken-pictureLength-totalPictures/{picturesTaken_}/{pictureLength_}/{totalPictures_}")
# def setPicturesTaken_pictureLength_totalPictures(picturesTaken_: int, pictureLength_: int, totalPictures_: int):
#     global picturesTaken
#     global pictureLength
#     global totalPictures
#     try:
#         picturesTaken = picturesTaken_
#         pictureLength = pictureLength_
#         totalPictures = totalPictures_
#     except:
#         return {"status": False}
#     return {"status": True}

