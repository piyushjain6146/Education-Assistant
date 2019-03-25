import re
import pandas as pd

# //RE
# re.compile(r'cutoff|last cutoff|cut off)

# //question
# last cut off of iit ________?
# cut off of last year in iit ______?
# last year cut off in iit_________?
# ****upar na ma branch pu6se k kai branch ma mnai to jo akhi iit ni badhi branch nu moklato hoy to m mokli deje ans ma
# last year / 2019 cutoff in computer engineering in iit _______?
# ****ama branch badli devani

def find_category(que):
    print('IN CATEGORY')
    matchCategory = re.compile(r'sebc|obc|open|sc|st|general')
    getCategory = matchCategory.search(que)
    try:
        return getCategory.group()
    except:
        return None


def do_cutoff_work(que, askIIT, iit_exists, dept_name):

    answer = ''
    category = find_category(que)
    print(category)
    print('CUTOFF')
    print(askIIT)
    print(iit_exists)
    print(dept_name)
    if (askIIT != []) and (not iit_exists) and (category != None) and (dept_name != []):
        print('IN IF')
        if category == 'sebc' or category == 'obc':
            print('IN OBC')
            data_frame = pd.read_csv('cutoff.csv', usecols=['iit_name','dept_name','obc_opening','obc_closing'])
        elif category == 'open' or category == 'general':
            print('IN OPEN')
            data_frame = pd.read_csv('cutoff.csv', usecols=['iit_name','dept_name','open_opening','open_closing'])
        elif category == 'sc':
            print('IN SC')
            data_frame = pd.read_csv('cutoff.csv', usecols=['iit_name','dept_name','sc_opening','sc_closing'])
        elif category == 'st':
            print('IN ST')
            data_frame = pd.read_csv('cutoff.csv', usecols=['iit_name','dept_name','st_opening','st_closing'])

        for i in askIIT:
            answer += "\n" + i + "..."
            for j in dept_name:
                temp = i.replace("Indian Institute of Technology", "IIT")
                temp_dept = j.title()
                answer += "\nOpening Rank : " +str(data_frame.loc[(data_frame['iit_name'] == temp) & (data_frame['dept_name'].str.contains(temp_dept))]).split()[-2] + "\nClosing Rank : " + str(data_frame.loc[(data_frame['iit_name'] == temp) & (data_frame['dept_name'].str.contains(temp_dept))]).split()[-1]
                print(answer)
        return answer
    
    elif (dept_name == []) and (askIIT != []) and (category != None):
        print('IN ELSE 1')
        answer += 'Can you please tell me of which department do you want to know cutoff. Such as Computer, Electrical, Chemical...\nYou can ask question like\nShow me cutoff of general category of Computer Department in IIT Bombay'
        return answer
    
    elif (category == None) and (askIIT != []) and (dept_name != []):
        print('IN ELSE 2')
        answer += 'Can you please tell me of which category do you want to know cutoff. Such as Open, SC, ST,...\nYou can ask question like\nShow me cutoff of general category of Computer Department in IIT Bombay'
        return answer
    
    elif (iit_exists) and (category != None) and (dept_name != []):
        print('IN ELSE 3')
        answer += 'Can you please tell me of which IIT do you want to know cutoff. Such as IIT Bombay, IIT Kanpur,...\nYou can ask question like\nShow me cutoff of general category of Computer Department in IIT Bombay'
        return answer
    else :
        answer += 'Can you please tell me of which IIT do you want to know cutoff. Such as IIT Bombay, IIT Kanpur,...\nYou can ask question like\nShow me cutoff of general category of Computer Department in IIT Bombay'
        return answer