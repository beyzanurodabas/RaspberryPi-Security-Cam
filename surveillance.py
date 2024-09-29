# We need the following four modules to send emails from Raspberry Pi:
from email.mime.base import MIMEBase  # Multipurpose Internet Mail Extensions (MIME) for simple email, smtplib is sufficient
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
# The smtplib package allows us to set up the Gmail server
import smtplib, email, os, glob
from picamera import PiCamera
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO
import time
import RPi.GPIO as GPIO #for fire sensor

#***********************************************GPIO setup *************************************************
# The GPIO package helps control the GPIO pins of our Raspberry Pi
GPIO.setwarnings(False)  # Any GPIO warnings should be ignored
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.IN)  # Read output from PIR motion sensor

# For fire sensor
channel=7
#GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

#*********************************************** Email parameters *************************************************
subject = 'Security Alert: Motion Detected'
bodyText = """
Hello,
Motion was detected in your room.
Please check the attachment sent from the Raspberry Pi security system."""
# PASSWORD PARAMETER MUST BE ENTERED TO RUN THE PROJECT
fromaddr = 'beyzanur.odabas@ogr.sakarya.edu.tr'  # USERNAME - SENDER_GMAIL_ADDRESS
PASSWORD = ''  # Password of the email sender
toaddr = 'beyzanurodabas555@gmail.com'  # RECEIVER_EMAIL

#*********************************************** Video finename and path *************************************************
# We can set the directory path and file prefix for saving images:
filename_part1 = "surveillance"
file_ext = ".mp4"
now = datetime.now()
current_datetime = now.strftime("%d-%m-%Y_%H:%M:%S")
filename = filename_part1 + "_" + current_datetime + file_ext
filepath = "/home/raspberry/Desktop/"  # Path where images will be saved


def send_email():
    mail=MIMEMultipart()  #message
    mail["From"]=fromaddr
    mail["To"]=toaddr
    mail["Subject"]=subject

    mail.attach(MIMEText(bodyText, 'plain'))
    attachment=open(filepath+filename, "rb")

    part=MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())

    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " +filename)

    mail.attach(part)
    text=mail.as_string()

    server=smtplib.SMTP('smtp.gmail.com',587) #gmail server installed
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(fromaddr, PASSWORD)
    server.sendmail(fromaddr,toaddr, text)
    server.quit()
    print("Email sent")

def capture_video():
 #data= time.strftime("%d_%b_%Y|%H:%M:%S")
    camera.start_preview() 
    camera.start_recording('/home/raspberry/Desktop/video.h264') #start video recording
    camera.wait_recording(10) #10sn
    camera.stop_recording()
    camera.stop_preview()

#Removes all video files created by code
def remove_file():
    files_to_remove = [
        "/home/raspberry/Desktop/video.h264",
        filepath + filename
    ]
    for file in files_to_remove:
        try:
            os.remove(file)
            print(f"Removed: {file}")
        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"Error removing {file}: {e}")

#for fire sensor
def callback(channel):
    print("flame detected")
   
GPIO.add_event_detect(channel,GPIO.BOTH,bouncetime=300)
GPIO.add_event_callback(channel,callback)


#*************************************************** Camera Settings**************************************************************************
camera = PiCamera()
camera.resolution = (900, 600)  # Camera resolution
# camera.framerate = 15  # You need to set the frame rate to 15 to enable maximum resolution
camera.rotation = 180  # Rotation if the camera is upside down
camera.awb_mode = 'sunlight'  # Automatic white balance adjustment
camera.brightness = 55  # Brightness
camera.start_preview(alpha=200)  # We made the preview transparent so we can see if errors occur in your program

#*************************************************** MAIN ********************************************************************
while True:
    i = GPIO.input(26)  # Input will be read from pin 26
    if i == 1:  # When the output from the motion sensor is high
        print("Motion Detected")
        capture_video()
        sleep(2)
        res = os.system("MP4Box -add /home/raspberry/Desktop/video.h264 /home/raspberry/Desktop/video.mp4")
        os.system("mv /home/raspberry/Desktop/video.mp4 " + filepath + filename)
        send_email()
        sleep(2)
        remove_file()
        time.sleep(1)