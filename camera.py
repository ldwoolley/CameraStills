#!/user/bin/pythin
import time
from shutil import disk_usage

import picamera
from time import sleep, strftime

filePath = '/home/pi/camera'  # do not include the final "/"
imageInterval = 600           # in seconds

def cameraInit( camera ):     # Set the camera instant defaults
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

def cameraCapture(camera):
    # create the datetime label for the image
    dateText = strftime('%Y-%m-%d %H:%M:%S') 
    # set Project Specific Code
    camera.annotate_text = "Bird watch %s" % DateText
    camera.start_preview(alpha=255)  # between 0 and 255
    sleep(4)
    camera.capture('%s/image-%s.jpg' % filePath, dateText)
    camera.stop_preview()

def main():
    errorCounter = 0
    imageCounter = 0
    imageTimer = 0
    # Handle Errors and keep running.
    try:
        # Declare a camera
        camera = picamera.PiCamera()
        
        # Setup Sequence
        cameraInit ( camera )

	# Sequence until one fo the following has occured:
	# stop requested, disk is >90% full, 
	# max number of images or max time reached
	while (imageCounter < MAX_IMAGE_COUNT):
	    while (imageTimer < MAX_IMAGE_TIMER):
	        # Check disk usage
		if ( diskGreePct > MIN_DISK_FREE_PCT):
		    # still need to handle a stop request
                    cameraCapture ( camera )
                    imageCounter++
                    imageTimer = time.clock() - startTime
                    diskFreePct = disk_usage(filePath).free / 
                                  disk_usage(filePath).total
                    
                    # calculate time remaining to next interval
                    # to eliminate time drage from image processing time
                    sleep(imageInterval)
                else:
		    print('The disk space is nearly full,
		           %s MB free space' 
                           % str(disk_usage(filePath)/1024/1024)
		    break;
 

    except:
	print("We have encountered %i errros" % ++ErrorCount)
	raise
        if ErrorCount > ErrorLimit:
	    break

    else:

    finally:
        # close up the camera functions before exiting
	camera.close()
        # output basic parameters
        print('System ran for %s seconds' % str(imageTimer) )
        print('System took %s images' % str(imageCounter) )
        print('System free disk space is %s %' % str(diskFreePct) )

if __name__ == "__main__":
    main()
