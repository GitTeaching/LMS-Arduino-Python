# LMS-Arduino-Python

#### Library Management System using RFID MFRC522, Arduino, Python Tkinter, and MySQL.

In this project, RFID-RC522 is interfaced with Arduino and then RFID data is sent to Tkinter GUI and MySQL database using Python.

#### Project Demos : 
- https://www.youtube.com/watch?v=t5eLQYGKfPs
- https://www.youtube.com/watch?v=dDuIIZxRO4I

#### Components and software used :

##### Arduino Part :

**1 -** Arduino Uno and its Arduino IDE : https://www.arduino.cc/en/Main/Software

- Arduino code .ino file : https://github.com/GitTeaching/LMS-Arduino-Python/blob/master/arduino_rfid_sensor/arduino_rfid_sensor.ino

**2 -** RFID MFRC522 with tags and cards : 

![alt text](https://github.com/GitTeaching/LMS-Arduino-Python/blob/master/screenshots%20%26%20circuits/rfid.jpg?raw=true)

- RFID Circuit Diagram :

![alt text](https://github.com/GitTeaching/LMS-Arduino-Python/blob/master/screenshots%20%26%20circuits/diagram%20circuit.jpg?raw=true)

- RFID RC522 Library : install and include library. Donwload from : https://github.com/miguelbalboa/rfid

**3 -** Piezo / buzzer for the sound on Arduino digital PIN 2 anf GND.

**4 -** Final result :

<img src="https://github.com/GitTeaching/LMS-Arduino-Python/blob/master/screenshots%20%26%20circuits/20200825_212922.jpg" width="700">

<img src="https://github.com/GitTeaching/LMS-Arduino-Python/blob/master/screenshots%20%26%20circuits/20200825_212922.jpg" width="700">

##### Python Part :

**1 -** Python, Tkinter for logic and GUI.

**2 -** Python pyserial for communication : (pip install pyserial) https://pypi.org/project/pyserial/ 

**3 -** WAMP Server for MySQL Database storage. MySQL Connector Python library (pip install mysql-connector-python).

**4 -** MySQL Database - Table Name : Book(bui, rfid_id, title, authors, description, status, issued_by)

**5 -** GUI Screenshots :

<img src="https://github.com/GitTeaching/LMS-Arduino-Python/blob/master/screenshots%20%26%20circuits/screenshot%201.png" width="700">

<img src="https://github.com/GitTeaching/LMS-Arduino-Python/blob/master/screenshots%20%26%20circuits/screenshot%202.png" width="700">

<img src="https://github.com/GitTeaching/LMS-Arduino-Python/blob/master/screenshots%20%26%20circuits/screenshot%203.png" width="700">

<img src="https://github.com/GitTeaching/LMS-Arduino-Python/blob/master/screenshots%20%26%20circuits/screenshot%204.png" width="700">

#### Instructions :

- Load arduino_rfid_sensor.ino code to Arduino
- Install all python libraries
- Run app.py
