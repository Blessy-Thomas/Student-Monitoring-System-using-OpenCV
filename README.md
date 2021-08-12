# Student-Monitoring-System-using-OpenCV
An Application which helps teachers to know whether students are paying attention during an online lecture.

Resources:
https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/

Installing and Configuring dlib:
We need to create an enivronment in order to install dlib, as it cannot be directly installed using pip. So, follow this commands in order to install dlib into your system if you haven't installed it previously. Make sure you have Anaconda installed, as we will be doing everyting in Anaconda Prompt.

Step 1: Update conda
conda update conda
Step 2: Update anaconda
conda update anaconda 
Step 3: Create a virtual environment
conda create -n env_dlib 
Step 4: Activate the virtual environment
conda activate env_dlib
Step 5: Install dlib
conda install -c conda-forge dlib 
If all these steps are completed successfully, then dlib will be installed in the virtual environment env_dlib. Make sure to use this environment to run the entire project.

Step to deactivate the virtual environment
conda deactivate 
Running the system:
Step 1:
Clone the repository into your system by:

git clone https://github.com/Blessy-Thomas/Student-Monitoring-System-using-OpenCV.git
Or directly download the zip.

Step 2:
Download the file shape_predictor_68_face_landmarks.dat here. Make sure you download it in the same folder.

Step 3:
Install all the system requirments by:

pip install -r requirements.txt
