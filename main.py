from tkinter import *
import tkinter.messagebox

import nltk

nltk.download('stopwords')
import warnings

warnings.filterwarnings('ignore')
from pyresparser import ResumeParser

import spacy
spacy.load("en_core_web_sm")
# import pandas as pd
import csv
import fitz

nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import glob

resume_list = glob.glob("resume/*")


def extract_resume():
    for i in range(0, len(resume_list)):
        try:
            resume_data = ResumeParser(resume_list[i]).get_extracted_data()

            fields = ['Location', 'Name', 'Email', 'Mobile_number', 'Experience', 'Total_experience', 'Degree', 'Skills']

            #name = resume_data['name']
            name =resume_list[i][7:-4]
            name = " ".join(re.split("[^a-zA-Z]*", name))

            email = resume_data['email']
            mobile_number = resume_data['mobile_number']
            experience = resume_data['experience']
            total_experience = resume_data['total_experience']
            degree = resume_data['degree']
            skills = resume_data['skills']

            rows = [resume_list[i], name, email, mobile_number, experience, total_experience, degree, skills]
            filename = "resume_data_extract.csv"

            if i == 0:
                with open(filename, 'a', encoding='utf-8') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerow(rows)
            elif i > 0:
                with open(filename, 'a', encoding='utf-8') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(rows)
        except Exception as err:
            pass

    tkinter.messagebox.showinfo('Extract Resume','Your work is done please check resume_data_extract.csv file')
#    work_done = Label(root, text="Your work is done please check resume_data_extract.csv file ")
#    work_done.pack()


def extract_custom_skills_data():
    msg = "Required Skill Set is : " + e.get()
    unbunked_label4 = Label(root, text=msg)
    unbunked_label4.pack()

    for i in range(0, len(resume_list)):
        try:
            resume_data = ResumeParser(resume_list[i]).get_extracted_data()
            cust_skill = word_tokenize(e.get())
            cust_skill = map(lambda q: q.lower(), cust_skill)
            custom_skill = list(cust_skill)

            fname = resume_list[i]
            doc = fitz.open(fname)
            text = ""
            for page in doc:
                text = text + str(page.getText())
                tx = " ".join(text.split('\n'))

            tokenizer = RegexpTokenizer(r'\w+')
            tokenized_sent = tokenizer.tokenize(text)

            words = []
            for word in tokenized_sent:
                words.append(word.lower())

            stop_words = set(stopwords.words('english'))
            filtered_sentence = [word for word in words if word not in stop_words]

            req_skills = []
            for x in range(0, len(custom_skill)):
                if any(custom_skill[x] in word for word in filtered_sentence):
                    req_skills.append(custom_skill[x])
                else:
                    pass

            # field names
            fields = ['Location', 'Name', 'Email', 'Mobile_number', 'Experience', 'Total_experience', 'Degree', 'Skills',
                      'Required_skill']

            name = resume_data['name']
            email = resume_data['email']
            mobile_number = resume_data['mobile_number']
            experience = resume_data['experience']
            total_experience = resume_data['total_experience']
            degree = resume_data['degree']
            skills = resume_data['skills']

            rows = [resume_list[i], name, email, mobile_number, experience, total_experience, degree, skills, req_skills]
            filename = "custom_skill_resume_extract.csv"

            if i == 0:
                with open(filename, 'a', encoding='utf-8') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerow(rows)
            elif i > 0:
                with open(filename, 'a', encoding='utf-8') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(rows)

        except Exception as err:
            pass

    tkinter.messagebox.showinfo('Extract Custom Resume', 'Your work is done please check custom_skill_resume_extract.csv file')
#    work_done1 = Label(root, text="Your work is done please check custom_skill_resume_extract.csv file ")
#    work_done1.pack()


root = Tk()
root.title("Unbunked Resume Extract App")
root.iconbitmap('unbunkedicon.ico')

Unbunked_label = Label(root, text="Welcome to Unbunked Resume Extract App")
Unbunked_label.pack()

Unbunked_label1 = Label(root, text="Click On Below Button To Extract All Resume Information Into CSV File")
Unbunked_label1.pack()

ResumeData_extract = Button(root, text="Extract All Data", command=extract_resume)
ResumeData_extract.pack()

Unbunked_label2 = Label(root,
                        text="Click On Below Button To Match Your Given Skill Set To Resume And Convert Information "
                             "Into CSV File")
Unbunked_label2.pack()

Unbunked_label3 = Label(root, text="Write Skills Which You Want")
Unbunked_label3.pack()

e = Entry(root, width=50)
e.pack()

Custom_ResumeData_extract = Button(root, text="Extract Custom Skills Data", command=extract_custom_skills_data)
Custom_ResumeData_extract.pack()

root.mainloop()
