from tkinter import *
from flask import Flask,redirect, url_for,render_template,request
import os

def d_dtcn(user_id):
	root = Tk()
	root.configure(background = "white")

	def function1(): 
		os.system("python focus_alert.py --shape_predictor shape_predictor_68_face_landmarks.dat %d" % user_id)
		exit()

	
	root.title("STUDENT MONITORING SYSTEM")
	Label(root, text="STUDENT MONITORING SYSTEM",font=("times new roman",20),fg="black",bg="aqua",height=3).grid(row=3,rowspan=3,columnspan=60,sticky=N+E+W+S,padx=6,pady=10)
	Button(root,text="Run using web cam",font=("times new roman",20),bg="#0D47A1",fg='white',command=function1).grid(row=6,columnspan=60,sticky=W+E+N+S,padx=6,pady=6)
	Button(root,text="Exit",font=("times new roman",20),bg="#0D47A1",fg='white',command=root.destroy).grid(row=10,columnspan=60,sticky=W+E+N+S,padx=6,pady=6)

	root.mainloop()