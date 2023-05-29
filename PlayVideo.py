import cv2
from ultralytics import YOLO
from Variables import camera1_monitor_regions, camera1_workstation_regions, camera2_monitor_regions, \
    camera2_workstation_regions, workstation_coordinates_camera1, workstation_coordinates_camera2, \
    camera1_monitor_variables, camera2_monitor_variables, camera1_monitor_isBusy, camera2_monitor_isBusy
import time
from datetime import datetime
import sqlite3


def insert_data(camera, monitor_variables):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for monitor, variables in monitor_variables.items():
        on_person = min(variables["On - Person"], 300)
        on_no_person = min(variables["On - No Person"], 300)
        off_person = min(variables["Off - Person"], 300)

        cur.execute('''INSERT INTO {} (timestamp, monitor, on_person, on_no_person, off_person)
                        VALUES (?, ?, ?, ?, ?)'''.format(camera), (timestamp, monitor, on_person, on_no_person, off_person))

    con.commit()

def calculateIou(bbox, roi):
    x1, y1, x2, y2 = bbox
    roi_x1, roi_y1, roi_x2, roi_y2 = roi

    # Calculate the coordinates of the intersection rectangle
    intersection_x1 = max(x1, roi_x1)
    intersection_y1 = max(y1, roi_y1)
    intersection_x2 = min(x2, roi_x2)
    intersection_y2 = min(y2, roi_y2)

    # Calculate the area of intersection
    intersection_area = max(0, intersection_x2 - intersection_x1 + 1) * max(0, intersection_y2 - intersection_y1 + 1)

    # Calculate the area of the bounding box and ROI
    bbox_area = (x2 - x1 + 1) * (y2 - y1 + 1)
    roi_area = (roi_x2 - roi_x1 + 1) * (roi_y2 - roi_y1 + 1)

    # Calculate the IoU percentage
    iou = intersection_area / float(bbox_area + roi_area - intersection_area)
    iou_percentage = iou * 100

    return iou_percentage

def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        coordinates = [x, y]
        print(coordinates)


# Used to get monitor status
def getMonitorStatus(frame):
    # Set default value to monitor is turned off
    is_monitor_on = False
    # Get average pixel intensity for Red, Green, Blue
    avgVal = cv2.mean(frame)
    print(avgVal)
    # Count the number of values greater than 80
    count = sum(val > 80 for val in avgVal)
    # If at least two values are greater than 80, set monitor to True
    if count >= 2:
        is_monitor_on = True
    return is_monitor_on


# Draw rectangles around monitors and add status circle
def drawRectanglesMonitors(frame, regions, color, statuses):
    for region, status in zip(regions, statuses):
        # Draw the rectangle
        cv2.rectangle(frame, (region[2], region[0]), (region[3], region[1]), color, 2)

        # Determine the color of the circle based on the monitor status
        circle_color = (0, 255, 0) if status else (0, 0, 255)  # Green for "on" and red for "off"

        # Calculate the coordinates for the circle
        circle_radius = 10
        circle_center = (region[3], region[0] + circle_radius + 5)

        # Draw the circle
        cv2.circle(frame, circle_center, circle_radius, circle_color, -1)

# Draw rectangles around workstations
def drawRectanglesWorkstations(frame, regions, color):
    for region in regions:
        cv2.rectangle(frame, (region[2], region[0]), (region[3], region[1]), color, 2)

# Connect to database
con = sqlite3.connect("timedata.db")
cur = con.cursor()

# Bounding box colors for detected objects
boundingBox_colors = [(140, 150, 160), (240, 150, 160)]
# Classes my model should predict (background class is here only as a filler class, it WILL NEVER BE DETECTED)
classes = ['Background', 'Person']

# Load YOLO model
model = YOLO("runs/detect/train31/weights/best.pt")

# Vals to resize video frames (we just resize the frame to be x2 smaller than default which is 1920x1080)
frame_wid = 960
frame_hyt = 540

# Used to find coordinates on frame for regions of interest (for example, to get coordinates for monitors)
#cv2.namedWindow('ObjectDetection1')
#cv2.namedWindow('ObjectDetection2')
#cv2.setMouseCallback('ObjectDetection1', POINTS)
#cv2.setMouseCallback('ObjectDetection2', POINTS)

# Real time video feed
#cap1 = cv2.VideoCapture('rtsp://admin:P@ssw0rd@192.168.1.21/1')
#cap2 = cv2.VideoCapture('rtsp://admin:P@ssw0rd@192.168.1.20/1')

# Pre-recorded videos
cap1 = cv2.VideoCapture("./camera1New.mp4")
cap2 = cv2.VideoCapture("./camera2New.mp4")

# Check video frames per second
fps = cap1.get(cv2.CAP_PROP_FPS)
print("Frames per second : {0}".format(fps))

frameCounter = 0

# Set the interval for saving frames (5 minutes = 300 seconds)
save_interval = 300
# Set the initial time
start_timer = time.time()

while True:
    start_time = time.time()

    # Capture each frame from both cameras
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    frameCounter += 1

    # Recapture frame if there was a problem for camera 1
    while ret1 == False:
       cap1.release()
       cap1 = cv2.VideoCapture('rtsp://admin:P@ssw0rd@192.168.1.21/1')
       ret1, frame1 = cap1.read()

    # Recapture frame if there was a problem for camera 2
    while ret2 == False:
       cap2.release()
       cap2 = cv2.VideoCapture('rtsp://admin:P@ssw0rd@192.168.1.20/1')
       ret2, frame2 = cap2.read()
    if frameCounter == fps:
        # Resize frames for camera 1 and camera 2
        frame1 = cv2.resize(frame1, (frame_wid, frame_hyt))
        frame2 = cv2.resize(frame2, (frame_wid, frame_hyt))
        # All monitor status which are used in camera 1
        camera1Monitor1On = getMonitorStatus(frame1[431:485, 340:425])
        camera1Monitor2On = getMonitorStatus(frame2[366:401, 298:419])
        camera1Monitor3On = getMonitorStatus(frame1[386:420, 495:586])
        camera1Monitor4On = getMonitorStatus(frame1[350:378, 495:560])
        camera1Monitor5On = getMonitorStatus(frame1[364:400, 587:670])
        camera1Monitor6On = getMonitorStatus(frame1[340:360, 565:626])

        # Draw rectangles for monitor and workstation regions for camera 1
        #drawRectanglesMonitors(frame1, camera1_monitor_regions, (0, 255, 0),[camera1Monitor1On, camera1Monitor3On, camera1Monitor4On, camera1Monitor5On, camera1Monitor6On])
        #drawRectanglesWorkstations(frame1, camera1_workstation_regions, (255, 0, 0))  # Workstation rectangles (blue)

        # All monitor status which are used in camera 2
        camera2Monitor1On = getMonitorStatus(frame2[415:495,205:365])
        camera2Monitor2On = getMonitorStatus(frame2[420:448,800:913])
        camera2Monitor3On = getMonitorStatus(frame2[330:346,481:561])
        camera2Monitor4On = getMonitorStatus(frame2[376:397,738:824])
        camera2Monitor5On = getMonitorStatus(frame2[350:365,683:765])
        camera2Monitor6On = getMonitorStatus(frame2[329:341,653:722])

        # Draw rectangles for monitor and workstation regions for camera 2
        #drawRectanglesMonitors(frame2, camera2_monitor_regions, (0, 255, 0), [camera2Monitor1On, camera2Monitor2On, camera2Monitor3On, camera2Monitor4On, camera2Monitor5On, camera2Monitor6On, camera1Monitor2On])
        #drawRectanglesWorkstations(frame2, camera2_workstation_regions, (255, 0, 0))  # Workstation rectangles (blue)

        # Use YOLO model to make a prediction on frame
        # Conf - Detect objects only above a certain confidence threshold (0.5 in this case)
        # Device - 0 (GPU used)
        # Source - Frame / Image the prediction is done for
        # Save - Save prediction results (in a video format in this case)
        detection1 = model.predict(source=[frame1], save=False, conf=0.5, device=0)
        detection2 = model.predict(source=[frame2], save=False, conf=0.5, device=0)

        # For camera 1
        for monitor in range(1, 7):
            on_status = locals()[f"camera1Monitor{monitor}On"]
            no_person_count = camera1_monitor_variables[f"Monitor {monitor}"]["On - No Person"]

            if len(detection1[0]) == 0 and on_status and not camera1_monitor_isBusy[monitor]:
                no_person_count += 1
                camera1_monitor_isBusy[monitor] = True

            camera1_monitor_variables[f"Monitor {monitor}"]["On - No Person"] = no_person_count

        # For camera 2
        for monitor in range(1, 7):
            on_status = locals()[f"camera2Monitor{monitor}On"]
            no_person_count = camera2_monitor_variables[f"Monitor {monitor}"]["On - No Person"]

            if len(detection2[0]) == 0 and on_status and not camera2_monitor_isBusy[monitor]:
                no_person_count += 1
                camera2_monitor_isBusy[monitor] = True

            camera2_monitor_variables[f"Monitor {monitor}"]["On - No Person"] = no_person_count
        # Iterate through all the detections made for frame
        for i in range(len(detection1[0])):
            # Get all bounding boxes from detection
            boxes = detection1[0].boxes
            # Select the i-th box
            box = boxes[i]
            # Get class ID of detected object
            clsID = box.cls.cpu().numpy()[0]
            # Get confidence score of detected object
            conf = box.conf.cpu().numpy()[0]
            # Get bounding box coordinates of detected object
            bb = box.xyxy.cpu().numpy()[0]
            # Iterate over the workstation coordinates and update the monitor variables
            for x, workstation_coords in enumerate(workstation_coordinates_camera1, start=1):
                iou = calculateIou(bb, workstation_coords)
                monitor_name = f"Monitor {x}"
                on_status = locals()[f"camera1Monitor{x}On"]

                if on_status and iou > 5 and not camera1_monitor_isBusy[x]:
                    camera1_monitor_variables[monitor_name]["On - Person"] += 1
                    camera1_monitor_isBusy[x] = True

                elif on_status and iou == 0 and not camera1_monitor_isBusy[x]:
                    camera1_monitor_variables[monitor_name]["On - No Person"] += 1
                    camera1_monitor_isBusy[x] = True

                elif not on_status and iou > 5 and not camera1_monitor_isBusy[x]:
                    camera1_monitor_variables[monitor_name]["Off - Person"] += 1
                    camera1_monitor_isBusy[x] = True


            # Use cv2 to draw a rectangle around detected object
            cv2.rectangle(
                frame1,
                (int(bb[0]), int(bb[1])),
                (int(bb[2]), int(bb[3])),
                boundingBox_colors[int(clsID)],
                3,
            )
            # Add text with class and confidence score to bounding box
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(
                frame1,
                classes[int(clsID)] + " " + str(round(conf, 2)),
                (int(bb[0]), int(bb[1]) - 10),
                font,
                1,
                (255, 255, 255),
                2,
            )
        # Iterate through all the detections made for frame
        for i in range(len(detection2[0])):
            # Get all bounding boxes from detection
            boxes = detection2[0].boxes
            # Select the i-th box
            box = boxes[i]
            # Get class ID of detected object
            clsID = box.cls.cpu().numpy()[0]
            # Get confidence score of detected object
            conf = box.conf.cpu().numpy()[0]
            # Get bounding box coordinates of detected object
            bb = box.xyxy.cpu().numpy()[0]
            for y, workstation_coords in enumerate(workstation_coordinates_camera2, start=1):
                iou = calculateIou(bb, workstation_coords)
                monitor_name = f"Monitor {y}"
                on_status = locals()[f"camera2Monitor{y}On"]

                if on_status and iou > 5 and not camera2_monitor_isBusy[y]:
                    camera2_monitor_variables[monitor_name]["On - Person"] += 1
                    camera2_monitor_isBusy[y] = True

                elif on_status and iou == 0 and not camera2_monitor_isBusy[y]:
                    camera2_monitor_variables[monitor_name]["On - No Person"] += 1
                    camera2_monitor_isBusy[y] = True

                elif not on_status and iou > 5 and not camera2_monitor_isBusy[y]:
                    camera2_monitor_variables[monitor_name]["Off - Person"] += 1
                    camera2_monitor_isBusy[y] = True



            # Use cv2 to draw a rectangle around detected object
            cv2.rectangle(
                frame2,
                (int(bb[0]), int(bb[1])),
                (int(bb[2]), int(bb[3])),
                boundingBox_colors[int(clsID)],
                3,
            )
            # Add text with class and confidence score to bounding box
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(
                frame2,
                classes[int(clsID)] + " " + str(round(conf, 2)),
                (int(bb[0]), int(bb[1]) - 10),
                font,
                1,
                (255, 255, 255),
                2,
            )
        # Print camera 1 monitor variables
        print("Camera 1 Monitor Variables:")
        for monitor, statuses in camera1_monitor_variables.items():
            print(f"{monitor}:")
            for status, count in statuses.items():
                print(f"  {status}: {count}")

        # Print camera 2 monitor variables
        #print("Camera 2 Monitor Variables:")
        for monitor, statuses in camera2_monitor_variables.items():
            print(f"{monitor}:")
            for status, count in statuses.items():
                print(f"  {status}: {count}")

        frameCounter = 0
        # Reset the flags for camera 1
        for monitor in camera1_monitor_isBusy:
            camera1_monitor_isBusy[monitor] = False

        # Reset the flags for camera 2
        for monitor in camera2_monitor_isBusy:
            camera2_monitor_isBusy[monitor] = False

        # Display frame
        cv2.imshow("ObjectDetection1", frame1)
        cv2.imshow("ObjectDetection2", frame2)

        # Terminate runtime on "Q" press
        if cv2.waitKey(1) == ord("q"):
            break

        if time.time() - start_timer >= save_interval:
            insert_data("CameraOneMonitors", camera1_monitor_variables)
            insert_data("CameraTwoMonitors", camera2_monitor_variables)
            start_timer = time.time()
            # Reset the variables to 0
            for monitor, variables in camera1_monitor_variables.items():
                variables["On - Person"] = 0
                variables["On - No Person"] = 0
                variables["Off - Person"] = 0

            for monitor, variables in camera2_monitor_variables.items():
                variables["On - Person"] = 0
                variables["On - No Person"] = 0
                variables["Off - Person"] = 0

        if(1.0 - time.time() + start_time > 0):
            time.sleep(1.0 - time.time() + start_time)  # Sleep for 1 second minus elapsed time

# Release capture and destroy windows when complete
cap1.release()
cap2.release()
cv2.destroyAllWindows()
con.close()

