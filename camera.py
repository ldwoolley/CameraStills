#!/user/bin/python
import time
from shutil import disk_usage

import picamera
from time import sleep, strftime

filePath = '/home/pi/camera'  # do not include the final "/"
imageInterval = 600           # in seconds
MAX_IMAGE_COUNT = 10000
MAX_IMAGE_TIMER = 60*60*24
MIN_DISK_FREE_PCT = 0.1
cameraInitErrors = 0
cameraCaptureErrors = 0
dateText = ""
sensorTime = 4

def cameraInit(self, camera ):     # Set the camera instant defaults
    try:
        # set all the default camera settings to reduce surprises.
        camera.sharpness = 0
        camera.contrast = 0
        camera.brightness = 50
        camera.saturation = 0
        camera.ISO = 0
        camera.video_stabilization = False
        camera.exposure_compensation = 0
        camera.exposure_mode = 'auto'
        camera.meter_mode = 'average'
        camera.awb_mode = 'auto'
        camera.image_effect = 'none'
        camera.color_effects = None
        camera.rotation = 0
        camera.hflip = False
        camera.vflip = False
        camera.crop = (0.0, 0.0, 1.0, 1.0) 
        camera.rotation = 0               # 0, 90, 180, 270
        camera.resolution = (1920, 1080)  # 64x64 to 2592x1944
        # return something if the code ran clean.
        return True
    except:
        # count up the number of errors that have occured initializing the camera.
        self.cameraInitErrors += 1
        print('Sorry! but there have been %i errors initializing the camera') % self.cameraInitErrors
        # rase the exception so that we can keep track of what really happenedraise
        raise
        # return boolean FALSE if the code failed to initialize correctly.
        return False
    

def cameraCapture(camera, sensorTime, JobText, DateText):
    try:
        # set Project Specific Code
        camera.annotate_text = "%s %s" % JobText, DateText
        camera.start_preview(alpha=255)  # between 0 and 255
        sleep(sensorTime)
        camera.capture('%s/image-%s.jpg') % filePath, dateText 
        camera.stop_preview()
        # return something if the code ran clean.
        return True
    except:
        # count up the number of errors that have occured.
        self.cameraCaptureErrors += 1
        print('Sorry! there have been %i errors capturing images with the camera') 
              % self.cameraInitErrors
        # rase the exception so that we can keep track of what really happenedraise
        raise
        # return boolean FALSE if the code failed to initialize correctly.
        return False

def captureDateTime(interval, dateText):
    try:
        # create the datetime label for the image based on interval in (s)
        if (interval < 60):
            dateText = strftime('%Y-%m-%d %H:%M:%S')
        elif (interval < 60*60):
            dateText = strftime('%Y-%m-%d %H:%M')
        elif (interval < 60*60*24):
            dateText = strftime('%Y-%m-%d %H')
        elif (interval < 60*60*24*30):
            dateText = strftime('%Y-%m-%d')
        elif (interval < 60*60*24*30*12):
            dateText = strftime('%Y-%m')
        else:
            dateText = strftime('%Y')
     
        return True
    except:
        # count up the number of errors that have occured.
        self.dateErrors += 1
        print('Sorry! there have been %i errors setting the date.') 
              % self.dateErrors
        # rase the exception so that we can keep track of what really happenedraise
        raise
        # return boolean FALSE if the code failed to initialize correctly.
        return False
        

def main():
    errorCounter = 0
    imageCounter = 0
    imageTimer = 0
    # Handle Errors and keep running.
    try:
        # Declare a camera
        camera = picamera.PiCamera()
        
        # Setup the camera
        startTime = time.clock()
        nextTime = startTime + imageInterval
        cameraInit(camera)
        # Sequence until max number of images or max time reached
        while (imageTimer < MAX_IMAGE_TIMER && imageCounter < MAX_IMAGE_COUNT):
            # Check disk usage and if acceptable before capturing an image.
            diskFreePct = disk_usage(filePath).free / disk_usage(filePath).total
            if ( diskFreePct > MIN_DISK_FREE_PCT):
                # Collect the 
                if( captureDateTime(imageInterval, dateText) ):
                    pass
                else:
                    print('The time date failed for some reason')
                if( cameraCapture ( camera, sleepTime, JobText, DateText ) ):
                    imageCounter++
                else:
                    print('The camera capture failed for some reason')
            else:
                print('The disk space is nearly full, %s MB free space') 
                           % str(disk_usage(filePath)/1024/1024)
                break
            # Calculate the sleep to take the next picture on time.
            sleep( nextTime-time.clock)
            nextTime = nextTime + imageInterval
        
    except:
        print("We have encountered %i errros") % ++ErrorCount
        raise
        if ErrorCount > ErrorLimit:
            break

    finally:
        # close up the camera functions before exiting
        camera.close()
        # output basic parameters
        print('System ran for %s seconds') % str(imageTimer)
        print('System took %s images') % str(imageCounter)
        print('System free disk space is %s %') % str(diskFreePct)

if __name__ == "__main__":
    main()
