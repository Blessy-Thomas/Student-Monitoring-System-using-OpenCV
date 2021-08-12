# Student-Monitoring-System-using-OpenCV
An Application which helps teachers to know whether students are paying attention during an online lecture.

Resources:
https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/

### Code Requirements
The example code is in Python ([version 2.7](https://www.python.org/download/releases/2.7/) or higher will work). 

### Dependencies

1) import cv2
2) import imutils
3) import dlib
4) import scipy
5) import matplotlib
6) 

Installing and Configuring dlib:
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
git clone https://github.com/fear-the-lord/Drowsiness-Detection.git
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
