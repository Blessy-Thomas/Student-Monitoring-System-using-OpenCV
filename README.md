# Student-Monitoring-System-using-OpenCV
An Application that helps teachers to know whether students are paying attention during an online lecture.

Distant learning, a method of study where teachers and students do not meet in a classroom but use
the Internet, e-mail, mail, etc. to have classes. This methodology was not supposed to be the ideal
way of learning. This kind of teaching-learning process does not provide any assurance of whether
the students attending the classes are actually understanding the concepts being taught. The
teachers cannot rely on this method completely to check if the students are physically and mentally
present in the online class.
Though not the ideal method, it is the only way through which the teaching learning process can
take place during the Covid-19 Pandemic. Most of the universities and colleges have switched to
distant or the online mode of teaching when the Covid-19 virus was spreading all over the world.
The students have started attending their lectures and laboratory sessions from their homes while
the teachers are teaching them from their homes. The classroom environment is no longer a
necessity. Everyone has adapted themselves in this kind of communication for learning.
But the question of whether the complete knowledge provided by the professors or teachers is
really getting delivered to the students in this manner, still remains answered. Assuming students
to be attentive during the classes may be right for some of the students but to generalize it for all
students will not be right. Hence we tried developing a method which can be a solution to this
problem. This is an overview of the project ‘Student Monitoring System using OpenCV’.


Resources:
https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/

### Download
Visual studio Community 2019
https://visualstudio.microsoft.com/downloads/

### Code Requirements
The example code is in Python ([version 2.7](https://www.python.org/download/releases/2.7/) or higher will work). 

### Dependencies

1) import cv2
2) import imutils
3) import dlib
4) import scipy
5) import matplotlib
6) import mysql.connector

## Installing and Configuring dlib:
We need to create an enivronment in order to install dlib, as it cannot be directly installed using pip. So, follow this commands in order to install dlib into your system if you haven't installed it previously. Make sure you have Anaconda installed, as we will be doing everyting in Anaconda Prompt. 
### Step 1: Update conda 
```bash
conda update conda
```
### Step 2: Update anaconda 
```bash
conda update anaconda 
```
### Step 3: Create a virtual environment
```bash 
conda create -n env_dlib 
```
### Step 4: Activate the virtual environment 
```bash 
conda activate env_dlib
```
### Step 5: Install dlib 
```bash 
conda install -c conda-forge dlib 
```
If all these steps are completed successfully, then dlib will be installed in the virtual environment <b>env_dlib</b>. Make sure to use this environment to run the entire project. 

### Step to deactivate the virtual environment 
```bash 
conda deactivate 
```

## Running the system: 

### Step 1: 
Clone the repository into your system by: 
```bash 
git clone https://github.com/Blessy-Thomas/Student-Monitoring-System-using-OpenCV.git
```
Or directly download the zip.

### Step 2: 
Download the file <b>shape_predictor_68_face_landmarks.dat</b><a href = "https://drive.google.com/file/d/14weZIclFncz8BMOmrkLp9PadLIccbSBa/view?usp=sharing"> here.</a> Make sure you download it in the same folder. 

### Step 3: 
Install all the system requirments by:
```bash 
pip install -r requirements.txt
```
### Step 4: 
After the system has been setup. Run the command: 
```bash 
python focus_alert.py
```

### Step 5: 
Open your browser and in the search bar type: 
<b>localhost:8000</b> as this port is mostly used by flask. 
In case, this port is not available in your system, flask will try to use another port. The port number will be displayed in the command prompt.
So, type in the same port number in that case as: 
<b>localhost:<port_number></b>.
  
After all these steps have been completed successfully, you will see a web page opening up in the browser. Now you are free to explore the system.
  
### Contributors
  <ul>
    <li>Blessy Thomas</li>
    <li>Prajkta Ghorpade</li>
    <li>Ammu Attiyil</li>
    <li>Rhythm Negi</li>
  </ul>
