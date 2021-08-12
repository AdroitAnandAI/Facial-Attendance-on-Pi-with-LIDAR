# Facial-Attendance-on-Pi-with-LIDAR
Face Recognition based Attendance system deployable on Raspberry Pi, with Movidius NCS2 and RPLIDAR A1 to sense deptch to enable Door Access Control simulated with Pimoroni Blinkt

<<<MODIFY>>>
The face recognition models done in OpenVINO are deployed to RPi, integrated with a Pi Cam and LIDAR. If the person is identified and is sufficiently near to the door, then the door open event is triggered. If the person is not recognized and near to the door then a message should be pushed to the security's moble while keeping the door shut. This is simulated by flashing 'green' and 'red' lights respectively, on a Pimoroni Blinkt! controlled using  MQTT messages.

An input frame is processed by the face detection model to predict face bounding boxes. Then, face keypoints are predicted by the corresponding model. Face recognition model uses keypoints found to align the faces and the face gallery to match faces found on a video frame with the ones in the gallery.
<<</MODIFY>>>


The following pretrained OpenVINO models can be used:

* `face-detection-retail-0004` and `face-detection-adas-0001`, to detect faces and predict their bounding boxes
* `landmarks-regression-retail-0009`, to predict face keypoints
* `face-reidentification-retail-0095`, to recognize persons

The project has been tested using OpenVINO 2019 (models included in repo) on a Raspberry Pi 4 and Pi Cam with RPLIDAR A1 M8 and Intel Movidius NCS 2.

## How to Use?

First, clone this repo to a Raspberry Pi. Set up Intel Movidius NCS 2 so that you can run OpenVINO models in it.
This is enough to run the Face Recognition module. For LIDAR, install the required packages and connect a speaker after 'espeak' installation.


``` sh
pip install -r requirements.txt

python3 ./face_recognition_demo.py -m_fd OV2019-models/face-detection-retail-0004.xml -m_lm OV2019-models/landmarks-regression-retail-0009.xml -m_reid OV2019-models/face-reidentification-retail-0095.xml -d_fd MYRIAD -d_lm MYRIAD -d_reid MYRIAD --verbose -fg "Face_Gallery/"

```

Press 'n' to increment the date so that next day attendance registration can be demonstrated.

On the MQTT reception side:
If you want to start afresh, you need to create the table in mysql for attendance data insertion.
If not, then the database file is already there in this repo (attendance.db). 

``` sql
create table attendance (id INTEGER PRIMARY KEY,name TEXT,date_in,time_in DATE,time_out TIME)
```

Copy the files inside `mqtt-client-code` folder to the remote machine. Execute `mqtt-attendance.py` to receive messages to register attendance.
The twilio account details need to be filled in correctly in `send-sms.py` file in order to get alert messages on mobile.

``` sh
python3 mqtt-attendance.py
nano send-sms.py
```

To simulate door open or close events, connect a Pimoroni Blink! to the GPIO pins of RPi and execute `mqtt-blinkt.py`. The light would flash 'green' and 'red' for open and close events, based on the MQTT message. This is an optional step to demonstrate the access control function. In real deployment, it can be another control event communicated using MQTT.

