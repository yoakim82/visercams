from camid import camID
import mqtt

#from picamera2 import Picamera2
#from picamera2.encoders import H264Encoder, Quality
#from picamera2.outputs import FfmpegOutput, FileOutput
from dummycamera import DummyCam, DummyEnc, FfmpegOutput
import time
import datetime


def setup_mqtt(broker):
    mq = mqtt.MqttInterface(broker_address=broker, port=1883, username=camID, password=camID)


    global runFlag
    runFlag = False
    if mq.connect():
        if mq.startLoop():
            print("MQTT connection established.")

    return mq


def setup_camera(device="picam2", width=1920, height=1080, bps=10000000):

    print("Record Video")

    if device=="picam2":

        # Picamera2 setup
        picam2 = Picamera2()
        video_config = picam2.create_video_configuration(main={"size": (width, height)})
        picam2.configure(video_config)
        encoder = H264Encoder(bitrate=bps)

        return picam2, encoder
    else:
        cam = DummyCam()
        enc = DummyEnc()
        return cam, enc

def get_timestamp():
    now = datetime.datetime.now()
    start_time = now
    format_str = "%Y-%m-%d_%H_%M_%S"
    nowtext = now.strftime(format_str)
    output = nowtext
    return output


def main(mq, cam, encoder):

    while mq.listen:
        while not mq.activeCapture and mq.listen:
            time.sleep(0.1) # wait for ON signal to arrive

        ts = get_timestamp()

        output = f"{ts}_{camID}.mp4"

        cam.start_recording(encoder, FfmpegOutput(output))
        print(f"Starting recording at {ts}")
        while mq.activeCapture and mq.listen:
            time.sleep(0.1) # wait for OFF signal to arrive
        end_time = get_timestamp()
        cam.stop_recording()
        print(f"Stopping recording at {end_time}")

if __name__ == '__main__':
    mq = setup_mqtt(broker="10.44.169.50") # Jocke's lenovo machine


    # Camera intrinsics
    width = 1920  # Replace with your image width in pixels
    height = 1080  # Replace with your image height in pixels
    fov_degrees = 90.0  # Replace with your desired FOV in degrees

    cam, enc = setup_camera(device="test", width=width, height=height, bps=10000000)
    main(mq, cam, enc)