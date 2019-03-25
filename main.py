# load all the libraries
"""
re		:	for regular expression
pymongo	:	for mongodb
spacy	:	nlp library
csv		: 	to read data from files having scraped data
"""
import re
import pymongo
import spacy
import csv
from flask import Flask
from flask import request
from pymongo import MongoClient
import json
from googletrans import Translator

import checkBranch
import branch
import fees
import fund
import faculty
import news
import placement
import research
import seats
import rank
import top
import detail

"""
queGlobal store previous questions for some cases
spacy.load loads language model
MongoClient for connection to mongodb
"""
queGlobal = ''
option = []

nlp = spacy.load('en_core_web_sm')
# nlp1 = spacy.load('MODEL1/')  # trained departmemnt model
client = MongoClient()
db = client.ea_project
iit_details_collection = db.iit_details
trans = Translator()

app = Flask(__name__)


@app.before_first_request
def do_something_only_once():
    # print("Before")

    with open('nirf1.csv', 'w') as f1:
        with open('nirf.csv', 'r') as f:
            data = f.readlines()
            f1.write(data[0])
            for i in range(1, len(data)):
                if data[i] != '' and "Indian Institute of Technology" in data[
                        i]:
                    f1.write(data[i])

@app.route('/GetName', methods=['POST', 'GET'])
def FindName():
    #this will work is you do name='my name is ..' and do not work if you do name="my name is..."
    name = request.args['name']
    name = name.replace("'", " ").title()
    if trans.detect(str(name)).lang == 'hi':
        flag =1
        name = trans.translate(str(name), dest='en').text
    doc = nlp(name)
    all_name_en = ""
    all_name_hi = ""

    for token in doc:
        if token.pos_ == 'PROPN':
            all_name_en += token.text + " "

    if all_name_en.strip() == "":
        all_name_en = "User"

    all_name_hi = trans.translate(str(all_name_en), src='en', dest='hi').text

    return json.dumps({'name': all_name_en, 'hi_name': all_name_hi})


@app.route('/GetAudio', methods=['POST', 'GET'])
def GetAudio():
    print("GETAUDIO")
    # recorded_audio = request.files['ringtone']
    # print(type(recorded_audio))

    # r = sr.Recognizer()
    # trans = Translator()

    # with sr.AudioFile(recorded_audio) as source:
    #     audio = r.record(source)

    # try:
    #     print('In Try')
    #     str1 = r.recognize_google(audio, language='hi')
    #     str2 = trans.translate(str1,dest='en')
    #     str2 = str2.text

    #     print("Text: " + str1)
    #     print("\nAfter Translation: " + str2)

    # except Exception as e:
    #     print("Exception occured : " + str(e))

    # return json.dumps({
    #     'name':'all_name'
    # })


@app.route('/EducationAssistant', methods=['POST', 'GET'])
def EducationAssistant():
    
    try:
        answer = ''

        # assigns question got from user
        question = request.args.get('question')
        status = request.args.get('status')

        """
        for seprating sentences and works same as shown below
        question = question.replace('.','. ')
        question = question.replace('?','? ')
        question = question.replace('!','! ')
        question = question.replace(',',', ')

        """
        question = question.replace('.', '. ').replace('?', '? ').replace('!', '! ')

        flag = 0
        print(trans.detect(str(question)).lang)
        if trans.detect(str(question)).lang == 'hi' or trans.detect(str(question)).lang == 'himr':
            print("IF")
            question = trans.translate(str(question),src='hi', dest='en').text
            flag = 1

        # process question one by one by sentence tokenization
        doc = nlp(question)
        for que in doc.sents:
            que = str(que).lower().replace('iits', 'iit')
            que = str(que).lower().replace('iit-', 'iit ')
            que = str(que).replace('mumbai', 'bombay').strip()

            # for better performace of NER just do upper IIT names
            matchIITs = re.compile(r'iit [a-zA-Z]')
            getIIT = matchIITs.findall(que)
            if getIIT != None:
                for i in getIIT:
                    nameIIT = i.upper()
                    que = que.replace((nameIIT).lower(), nameIIT)

            #for shortcuts like iitb, iitd,...
            list_iit = {
                'iitkgp': 'IIT Kharagpur',
                'iitb': 'IIT Bombay',
                'iitm': 'IIT Madras',
                'iitk': 'IIT Kanpur',
                'iitd': 'IIT Delhi',
                'iitg': 'IIT Guwahati',
                'iitrpr': 'IIT Ropar',
                'iitr': 'IIT Roorkee',
                'iitbbs': 'IIT Bhubaneswar',
                'iitgn': 'IIT Gandhinagar',
                'iith': 'IIT Hyderabad',
                'iitj': 'IIT Jodhpur',
                'iitp': 'IIT Patna',
                'iiti': 'IIT Indore',
                'iitmandi': 'IIT Mandi',
                'iit (bhu)': 'IIT Varanasi',
                'iitbhu': 'IIT Varanasi',
                'iit Bhu': 'IIT Varanasi',
                'iitpkd': 'IIT Palakkad',
                'iittp': 'IIT Tirupati',
                'iit (ism)': 'IIT Dhanbad',
                'iitism': 'IIT Dhanbad',
                'iit Ism': 'IIT Dhanbad',
                'iitbh': 'IIT Bhilai',
                'iitgoa': 'IIT Goa',
                'iitjm': 'IIT Jammu',
                'iitdh': 'IIT Dharwad'
            }
            list_iit.values()
            for key, value in list_iit.items():
                que = que.replace(key, value)
            que = ' '.join(que.split())

            #Gave some defaults to variables
            departments = []
            temp = []
            yes_no_department = None
            temp_que = (' '.join(que.split())).title()

            # Start process for fetching departments from question.
            list_departments = [
                'Software', 'Drafting and Design', 'Mechanical', 'Aerospace',
                'Biomedical', 'Biomechanical', 'Automotive', 'Civil', 'Structural',
                'Architectural', 'Computer', 'Electrical', 'Electronics',
                'Mechatronics', 'Robotics', 'Microelectronic', 'Environmental',
                'Chemical', 'Materials Science', 'Agricultural', 'Paper',
                'Sustainability Design', 'Engineering Management', 'MBA',
                'Industrial', 'Systems', 'Manufacturing', 'Petroleum',
                'Geological', 'Nuclear', 'Marine', 'Engineering Physics',
                'Physics', 'Photonics', 'Nanotechnology', 'Mining', 'Ceramics',
                'Metallurgical', 'Geomatics', 'Project Management'
            ]
            for i in list_departments:
                if i in temp_que:
                    departments.append(i.lower())

            if departments != [] and ''.join(departments).strip() != '':
                yes_no_department = True
            else:
                yes_no_department = False

            # to diffrentiate ORINAL(1st,2nd,...) and CARDINAL(1,2,...)
            doc = nlp(que)
            iit = []
            ordinal = ' '
            cardinal = ' '
            for ent in doc.ents:
                if ent.label_ == 'CARDINAL':
                    cardinal = ' '.join(ent.text)
                if ent.label_ == 'ORDINAL' or ent.label_ == 'DATE':
                    ordinal = ' '.join(ent.text)
                if ent.label_ == 'ORG':
                    iit.append(ent.text)
            
            '''Some iits such as IIT Mandi is not recognized as whole so it just recognize iit in it.
            So to check if these are iits which are not recognized we go through all to check.'''
            askIIT = []
            for i in range(len(iit)):
                if 'IIT Hyderabad' in que:
                    askIIT.append("IIT Hyderabad")
                elif 'IIT Mandi' in que:
                    askIIT.append("IIT Mandi")
                elif 'IIT Patna' in que:
                    askIIT.append("IIT Patna")
                elif 'IIT Varanasi' in que:
                    askIIT.append("IIT Varanasi")
                elif 'IIT Dhanbad' in que:
                    askIIT.append("IIT Dhanbad")
                elif 'IIT Bhilai' in que:
                    askIIT.append("IIT Bhilai")
                elif 'IIT Goa' in que:
                    askIIT.append("IIT Goa")
                elif 'IIT Dharwad' in que:
                    askIIT.append("IIT Dharwad")
                elif 'IIT' in iit[i]:
                    askIIT.append(iit[i])

            # Check if 'iit' is written in question or not
            iit_exists = None
            if ('IIT' in que or 'iit' in que) and askIIT == []:
                iit_exists = True
            else:
                iit_exists = False

            # mongodb have full forms of IITs so...
            if askIIT != None:
                for i in range(len(askIIT)):
                    askIIT[i] = askIIT[i].replace("IIT", "Indian Institute of Technology")

            # refers to global variable queGlobal
            global queGlobal
            global option

            if status == '0':
                option = []
                queGlobal = ''
            elif status == '1':
                if flag == 1:
                    temp = queGlobal.replace('"', "") + " by " + que.replace('"', "")
                    print(temp)
                    que = trans.translate(str(temp), dest='en').text
                else:
                    que = queGlobal.replace('"', "") + " by " + que.replace('"', "")

            print("Que : ", que)
            with open('Questions.txt', 'a') as que_file:
                que_file.write(que + '\n')

            # for ques. having not in them
            matchNot = re.compile(r'(opening (rank|cutoff)( of)?|closing (rank|cutoff)( of)?|(last )?cutof(f)?( of)?|cut of(f)?|detail|details|list|lists|phd (faculties|faculty)|placement(s)?|branch(es|s)?|field(s)?|seat(s)?|fseat(s)?|department(s)?|(all( IIT)?|(top|peak)|best)?)? (.*)? not ')
            getNot = matchNot.search(que)
            if getNot == None:

                # Find Specific Branch in Specific IIT
                matchBranches_and_IIT = re.compile(r'([a-zA-Z]* IIT [a-zA-Z]* (offer(s)?|have|has|contains(s)?|available) [a-zA-Z]+)|([a-zA-Z]+ (available|there) (in)? IIT [a-zA-Z]*)')
                getBranches_and_IIT = matchBranches_and_IIT.search(que)
                if getBranches_and_IIT != None and 'cutoff' not in que:
                    if yes_no_department:
                        answer += checkBranch.do_check_branch_work(que, departments,yes_no_department, askIIT, iit_details_collection)
                    else:
                        answer += "\nSorry, Mention department is not available."
                # to get branch details
                elif getBranches_and_IIT == None and 'cutoff' not in que:
                    matchBranch = re.compile(r'branch(es|s)?|field(s)?|department(s)?|course(s)?')
                    getBranch = matchBranch.search(que)
                    if getBranch != None:
                        answer += branch.do_branch_work(que, askIIT, iit_exists, iit_details_collection)

                # to get fees details mess fees and academic fees
                matchFee = re.compile(
                    r'fee(s)?|tution fee(s)?|fee structure|expense(s)?')
                getFee = matchFee.search(que)
                if getFee != None:
                    answer += fees.do_fees_work(que, askIIT, iit_exists, iit_details_collection)

                # to get details of available seats
                matchSeat = re.compile(r'(f)?seat(s)?')
                getSeat = matchSeat.search(que)
                if getSeat != None:
                    answer += seats.do_seats_work(que, askIIT, iit_exists ,iit_details_collection)

                # to get list of IITs
                matchTop = re.compile(r'all (IIT)?|top( iit)?|best( iit)?|peak( iit)?')
                getTop = matchTop.search(que)
                if getTop != None:
                    temp_answer = top.do_top_work(que, askIIT, cardinal, ordinal, iit_exists, option, queGlobal)
                    answer += temp_answer[0]
                    queGlobal = temp_answer[1]
                    option = temp_answer[2]

                # to get rank of specific IIT
                matchRank = re.compile(r'rank( of)?|position( of)?|number( of)?')
                getRank = matchRank.search(que)
                if getRank != None:
                    answer += rank.do_rank_work(que,askIIT, iit_exists)

                # to get iit which has highest placement, research area, resource, Perception, teaching , learning & resources
                matchplacement = re.compile(r'placement(s)?|job(s)?')
                getplacement = matchplacement.search(que)
                if getplacement != None:
                    answer += placement.do_placement_work(que, askIIT, iit_exists)

                # No. of phd faculty
                matchFaculties = re.compile(r'phd (faculty|faculties|professor(s)?|teacher(s)?)')
                getFaculties = matchFaculties.search(que)
                if getFaculties != None:
                    answer += faculty.do_faculty_work(que, askIIT, iit_exists)

                # No. of publications
                matchresearch = re.compile(r'publication(s)?|research area(s)?')
                getresearch = matchresearch.search(que)
                if getresearch != None:
                    answer += research.do_research_work(que, askIIT, iit_exists)

                # No. of phd faculty
                matchFund = re.compile(r'investor(s)?|funding(s)?')
                getFund = matchFund.search(que)
                if getFund != None:
                    answer += fund.do_fund_work(que, askIIT, iit_exists)

                # List of iit
                matchList = re.compile(r'list(s)?|list(s)? (iit|IIT)?|(iit|IIT)? list(s)?|list(s)? of (iit|IIT)|(iit|IIT) [A-Za-z0-9]* list(s)?|list(s)? [A-Za-z0-9]* (iit|IIT)')
                getList = matchList.search(que)
                if getList != None:
                    answer += 'List of IITs...'
                    for n, key in enumerate(list_iit):
                        answer += "\n" + str(n + 1) + ". " + list_iit[key]

                # Details of iit
                matchDetails = re.compile(r'detail(s)?|detail(s)? (iit|IIT)?|(iit|IIT)? detail(s)?|detail(s)? of (iit|IIT)?|(iit|IIT)? [A-Za-z0-9]* detail(s)?|detail(s)? [A-Za-z0-9]* (iit|IIT)?')
                getDetails = matchDetails.search(que)
                if getDetails != None:
                    answer +=  detail.do_detail_work(que, askIIT, iit_details_collection)

                # Cutoff of IIT
                matchCutoff = re.compile(r'cutof(f)?( of)?|opening rank|closing rank|opening number|closing number|opening cutof(f)?|closing cutof(f)?')
                getCutoff = matchCutoff.search(que)
                if getCutoff != None:
                    answer += cutoff.do_cutoff_work(que, askIIT, iit_exists, departments)

            # to handle que. having 'not'
            else:
                answer = answer + "Sorry! We can not understand this type of question!\n But we can handle...\n" + que.replace('not', ' ')

            # to handle unrelated or yet not handled que
            if answer == '':
                answer = answer + 'Sorry,We can not understand your question!'
                answer = answer + news.do_news_work(list_iit)

            answer = answer.replace("Indian Institute of Technology", "IIT")
            if flag == 1 :
                if '1234567890' not in answer:
                    answer = trans.translate(str(answer),src='en', dest='hi').text
                temp_option = []
                for i in option:
                    temp_option.append(trans.translate(str(i),src='en', dest='hi').text)
                answer = answer.replace('IIT', 'आईआईटी')
                option = []
                option.extend(temp_option)

        # to clear option list
        temp = list(option)
        option = []
    
    # return response to user if exception occured
    except Exception as e:
        print(e)
        return json.dumps({
        'report' : 1,
    })

    # return response to user if exception not occured
    else:
        return json.dumps({
            'answer': str(answer),
            'option': temp,
            'uri' : "https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fiitcareerplus.files.wordpress.com%2F2010%2F02%2F014.jpg&f=1",
            'uri_show' : 0,
            'report' : 0
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)