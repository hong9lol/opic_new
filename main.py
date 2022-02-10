import json
import os
import random
import shutil

import pandas as pd
from flask import Flask, render_template, request

from TTS import create_audio
from config import sources_path_role_play, sources_path_selected_topic, sources_path_random_topic, audio_path

questions = []
current_question_index = 0

app = Flask(__name__)


@app.route('/')
def home():
    # Reset
    try:
        shutil.rmtree(audio_path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    os.mkdir(audio_path)
    init_source()
    return render_template('index.html')


@app.route('/opic')
def opic():
    return render_template('opic.html')

@app.route('/next', methods=['GET'])
def next_question():
    global questions
    global current_question_index
    print("current question index: " + str(current_question_index))
    
    if current_question_index > 13:
        print("마지막 문제")
        return "None"
        
    
    title = "Question " + str(current_question_index + 2)
    question = str(questions[current_question_index][1])
    hint = str(questions[current_question_index][2])
    answer = str(questions[current_question_index][3])
    
    create_audio(title, question)    

    current_question_index += 1

    return json.dumps({"title": title, "question": question, "hint": hint, "answer": answer})

def get_specific_questions(set_cnt, sources):
    questions = []
    if set_cnt == 0: # set1
        q2 = list(filter(lambda x: str(x[0]) == "2,5,8", sources))
        q3 = list(filter(lambda x: str(x[0]) == "3", sources))
        q4 = list(filter(lambda x: str(x[0]) == "4,6,9", sources))
        rand_num = random.randrange(len(q2))
        questions.append(q2[rand_num])
        if len(q3) > rand_num:
            questions.append(q3[rand_num])
        else:
            questions.append(random.choice(q3))
        if len(q4) > rand_num:
            questions.append(q4[rand_num])
        else:
            questions.append(random.choice(q4))
    elif set_cnt == 1 or set_cnt == 2: # set2, 3
        q5q8 = list(filter(lambda x: str(x[0]) == "2,5,8", sources))
        q6q9 = list(filter(lambda x: str(x[0]) == "4,6,9", sources))
        q7q10 = list(filter(lambda x: str(x[0]) == "7,10", sources))
        rand_num = random.randrange(len(q5q8))
        questions.append(q5q8[rand_num])
        if len(q6q9) > rand_num:
            questions.append(q6q9[rand_num])
        else:
            questions.append(random.choice(q6q9))
        if len(q7q10) > rand_num:
            questions.append(q7q10[rand_num])
        else:
            questions.append(random.choice(q7q10))
    elif set_cnt == 3: # set4 roll palying
        q11 = list(filter(lambda x: str(x[0]) == "11", sources))
        q12 = list(filter(lambda x: str(x[0]) == "12", sources))
        q13 = list(filter(lambda x: str(x[0]) == "13", sources))
        rand_num = random.randrange(len(q11))
        questions.append(q11[rand_num])
        if len(q12) > rand_num:
            questions.append(q12[rand_num])
        else:
            questions.append(random.choice(q12))
        if len(q13) > rand_num:
            questions.append(q13[rand_num])
        else:
            questions.append(random.choice(q13))
    elif set_cnt == 4: # set5 
        q14 = list(filter(lambda x: str(x[0]) == "14", sources))
        q15 = list(filter(lambda x: str(x[0]) == "15", sources))
        rand_num = random.randrange(len(q14))
        questions.append(q14[rand_num])
        if len(q15) > rand_num:
            questions.append(q15[rand_num])
        else:
            questions.append(random.choice(q15))
    return questions 
   
def get_sheet_names(path, cnt):
    question_sheet_names = pd.ExcelFile(path).sheet_names 
    num_of_question_types = len(question_sheet_names)
    qeustion_set_index_list = random.sample(range(0, num_of_question_types), cnt)
    l = []
    for i in qeustion_set_index_list:
        l.append([path, question_sheet_names[i]])
    return l

def init_source():    
    # init questions
    global questions
    global current_question_index
    questions = [] 
    current_question_index = 0
    question_sheet_names = []

    question_sheet_names += get_sheet_names(sources_path_selected_topic , 2)
    question_sheet_names += get_sheet_names(sources_path_random_topic , 2)
    random.shuffle(question_sheet_names)
    role_play_question_sheet_names = get_sheet_names(sources_path_role_play , 1)
    question_sheet_names.insert(3, role_play_question_sheet_names[0])
    
    # set questions in order
    set_cnt = 0
    print(question_sheet_names)
    for n in question_sheet_names:
        print("question set " + str(set_cnt + 1) + ": " + n[1])
        question_sources = pd.read_excel(n[0], sheet_name=n[1]).values.tolist()
        questions += get_specific_questions(set_cnt, question_sources)
        set_cnt += 1

    print("Question List: " + str(questions))
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
