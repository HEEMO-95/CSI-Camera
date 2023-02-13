
import cv2


def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=640,
    display_height=360,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_camera():
    window_pi = "CSI Camera"
   # window_eye = "PS3 EYE"


    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    picam  = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    outVid = cv2.VideoWriter('videos/mycam.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (640, 360))
   # ps3eye = cv2.VideoCapture(1)  #PS EYE Camea
    if picam.isOpened():
        try:
            window_handle = cv2.namedWindow(window_pi, cv2.WINDOW_AUTOSIZE)
            while True:
                ret_val, frame0 = picam.read()
               # ret_val, frame1 = ps3eye.read()

                #workspace:
               # outVid.write(frame0)

                if cv2.getWindowProperty(window_pi, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_pi, frame0)
                   # cv2.imshow(window_eye, frame1)
                    cv2.moveWindow(window_pi, 1 , 1)
                   # cv2.moveWindow(window_eye, 0 ,550)
                else:
                    break 
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
           # ps3eye.release()
            picam.release()
            cv2.destroyAllWindows()
            outVid.release()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    show_camera()
