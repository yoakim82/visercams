import time
import datetime

# camid should define the camera id text string
from camid import camID

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput, FileOutput
    
    
print("Record Video")

# Picamera2 setup
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size":(1920,1080)})
picam2.configure(video_config)
encoder = H264Encoder(bitrate=10000000)


while True:

    # some "UI" to help you start the camera at the same time
    now = datetime.datetime.now()
    start_time = now
    format_str = "%Y-%m-%d_%H_%M_%S"
    nowtext = now.strftime(format_str)
    output = nowtext
    delay = 20-(now.second % 10)

    start_time_1 = (now + datetime.timedelta(seconds=delay)).replace(microsecond=0)
    start_time_1_text = start_time_1.strftime(format_str)
    start_time_2 = (now + datetime.timedelta(seconds=delay+10)).replace(microsecond=0)
    start_time_2_text = start_time_2.strftime(format_str)
    start_time_3 = (now + datetime.timedelta(seconds=delay+20)).replace(microsecond=0)
    start_time_3_text = start_time_3.strftime(format_str)
    print("\n\nCurent time:", nowtext)
    print("1:", start_time_1_text)
    print("2:", start_time_2_text)
    print("3:", start_time_3_text)
    res = input("[1, 2, 3]+Enter to select a time: ")
    if res == '1':
        print("\nStart time  set to:", start_time_1_text)
        output = start_time_1_text+"_"+camID+".mp4"
        start_time = start_time_1
    elif res == '2':
        print("\nStart time  set to:", start_time_2_text)
        output = start_time_2_text+"_"+camID+".mp4"
        start_time = start_time_2
    elif res == '3':
        print("\nStart time set to:", start_time_3_text)
        output = start_time_3_text+"_"+camID+".mp4"
        start_time = start_time_3
    else:
        print("\nNo time selected exit without recording.\n")
        break
    delay = (start_time-datetime.datetime.now()).total_seconds()
    if (delay > 0):
        time.sleep(delay)
        
        # the actaul recording part ot the code
        record = True
        picam2.start_recording(encoder, FfmpegOutput(output))
        while record:
            res = input("\nPress e+Enter to stop recording: ")
            if res == 'e':
                record = False
        end_time = datetime.datetime.now()
        picam2.stop_recording()

        print("\nRecording done. Recording time:", end_time-start_time, "\n")
        break
    else:
        print("\n Selected time alredy pased.")
