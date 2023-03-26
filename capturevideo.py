import cv2
import time
import os

live_url = "rtsp://admin:sp77343488@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"

#setting video format

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D') #目前mjpg decode 方式有bug 改用 XVID 輸出 .avi
width = 1920
height = 1080
points = (width, height)

#path setting
def get_Month():
    ct = time.ctime().split()
    return ct[1]

def get_Date():
    ct = time.ctime().split()
    return ct[2]

def get_Time():
    ct = time.ctime().split()
    return ct[3]

def makedir():
    folder_path = os.getcwd() +"\\videos"
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    folder_path += "\\" + str(get_Month()) 
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
    
    folder_path += "\\" + str(get_Date()) 
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    folder_path +=  "\\" + str(get_Time().split(':')[0]) 
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    return folder_path

def save_video():
    cap = cv2.VideoCapture(live_url)
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    output = None
    frames = 0
    while True:
        retval, frame = cap.read()
        if not retval:
            raise IOError("Camera is not open")
        if frames / 12000 ==0:  #20fps 10分鐘分段
            if output is not None:
                output.release()
            folder_path = makedir()
            file_name = f'{folder_path}+{time.time()}.avi'
            print(file_name)
            output = cv2.VideoWriter(f'{file_name}', fourcc, 20, points)
        output.write(frame)
        frames += 1
        print(frames)
        time.sleep(0.05)
        if frames / 12000 ==1:
            break
    cap.release()
    if output is not None:
        output.release()

if __name__ == "__main__":
    try:
        while True:
            print("call")
            save_video()
    except KeyboardInterrupt:
        pass
    
