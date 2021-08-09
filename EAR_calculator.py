# Define the function for calculating the Eye Aspect Ratio(EAR)
from scipy.spatial import distance as dist 
import numpy as np

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of vertical eye landmarks (x, y)-coordinates
	# Vertical eye landmarks
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	# Horizontal eye landmarks 
	# compute the euclidean distance between the horizontal eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# The EAR Equation 
	EAR = (A + B) / (2.0 * C)
	return EAR

def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[13], mouth[19])
    B = dist.euclidean(mouth[14], mouth[18])
    C = dist.euclidean(mouth[15], mouth[17])
    D = dist.euclidean(mouth[12], mouth[16])
    MAR = (A + B + C) / (2.0 * D)
    return MAR


def cal_angle(a,b,c):
    v1 = np.array(a) - np.array(b)
    v0 = np.array(b) - np.array(c)

    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return np.degrees(angle)