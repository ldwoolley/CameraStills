#!/user/bin/python
import time
import sys
from shutil import disk_usage

import picamera
from time import sleep, strftime

filePath = '/home/pi/camera/'  # do not include the final "/"
imageInterval = 10          # in seconds
MAX_IMAGE_COUNT = 5
MAX_IMAGE_TIMER = 60*60*24*30
MIN_DISK_FREE_PCT = 0.1
cameraInitErrors = 0
cameraCaptureErrors = 0
dateText = ""
sensorTime = 4
jobText = "Bird Watch"

def cameraInit( camera ):     # Set the camera instant defaults
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
        print('Camera initialized')
        return True
    except:
        print('An exception occured during camera initialization.')
        # rase the exception so that we can keep track of what really happenedraise
        raise
        # return boolean FALSE if the code failed to initialize correctly.
        return False

def cameraCapture( Camera, SensorTime, JobText, DateText, FilePath):
    try:
        # set Project Specific Code
        Camera.annotate_text = (JobText + " " + DateText)
        #print('The image was annotated with %s' % (camera.annotate_text) )
        Camera.start_preview(alpha=100)  # between 0 and 255
        sleep(SensorTime)
        Camera.capture(FilePath + DateText+'.jpg') 
        Camera.stop_preview()
        # return something if the code ran clean.
        return True
    
    except:
        print('An exception occured during image capture.')
        # rase the exception so that we can keep track of what really happenedraise
        raise
        # return boolean FALSE if the code failed to initialize correctly.
        return False

def captureDateTime(interval):
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
        return dateText
    
    except:
        print('An exception occured during DateTime setting.')
        # rase the exception so that we can keep track of what really happenedraise
        raise
        # return boolean FALSE if the code failed to initialize correctly.
        return False
        
def main():
    errorCounter = 0
    imageCounter = 0
    imageTimer = 0
    diskFreePct = -999
    # Handle Errors and keep running.
    try:
        # Declare a camera
        camera = picamera.PiCamera()
        
        # Setup the camera
        startTime = time.time()
        nextTime = startTime
        cameraInit(camera)
        dateText = captureDateTime(imageInterval)
        print('The images will be annoated with %s.' % (jobText + ' ' + dateText) )
        print('The images will be stored with the pattern %s.' % (filePath + dateText + '.jpg') )
        # Sequence until max number of images or max time reached
        while (imageTimer < MAX_IMAGE_TIMER and imageCounter < MAX_IMAGE_COUNT):
            # Check disk usage and if acceptable before capturing an image.
            diskFreePct = disk_usage(filePath).free / disk_usage(filePath).total
            if ( diskFreePct > MIN_DISK_FREE_PCT):
                # Collect the date and time
                dateText = captureDateTime(imageInterval)
                if( len(dateText) > 1 ):
                    if( cameraCapture ( camera, sensorTime, jobText, dateText, filePath ) ):
                        imageCounter += 1
                    else:
                        print('The camera capture failed for some reason')
                        break
                else:
                    print('The time date failed for some reason')
                    break
            else:
                print('The disk space is nearly full:', 
                       disk_usage(filePath)/1024/1024 ,
                      'MB free space')
                break

            #sleep( nextTime-time.time() )
            nextTime = nextTime + imageInterval
            while nextTime > time.time():
                message = 'Captured {0:5d} images. Next image in {1:5.0f} s.'.format(imageCounter, (nextTime - time.time()))
                print( message, end='\r', flush=True )
                sleep(1)
            #print('\n')
            # Calculate the sleep to take the next picture on time.
            #sleepTime = nextTime - time.time()
            #print('The next time will be %i ' % (nextTime) )
            #print('The capture interval is %i ' % (imageInterval) )
            #print('the current time is %i ' % ( time.time() ) )
            #print('The sleep time will be %i .' % (sleepTime) )
            #print('The new next time will be %i ' % (nextTime + imageInterval ) )
        print('\n')
        print('Program has completed running')
        
    except (KeyboardInterrupt, SystemExit):
        camera.close()
        print('You provided a KeyboardInterrupt or computer sent a SystemExit and the program will clean up.')
        raise

    except:
        camera.close()
        print('The program encountered and unkown exception, and will clean up.')
        raise

    finally:
        # close up the camera functions before exiting
        camera.close()
        # output basic parameters
        print('Program ran for %i minuts.' % ((time.time() - startTime)/60) )
        print('Program captured %i images.' % (imageCounter) ) 
        print('System free disk space stands at %2.0f percent.' % (diskFreePct*100) )

if __name__ == "__main__":
    main()
