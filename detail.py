import pymongo

def do_detail_work(que, askIIT, test_connection):
    answer = ''
    if askIIT != []:
        for i in askIIT:
            cursor = test_connection.find({'name': str(i)}, {
                '_id': 0,
                'academic': 1,
                'mess': 1,
                'state': 1,
                'web': 1
            })
            answer += "\n" + "Fees Details of " + str(i) + "\nAcademic Fees : " + str(cursor[0]['academic']) + "\nMess Fees : " + str(cursor[0]['mess']) + "\nState : " + str(cursor[0]['state']) + "\nWebsite : " + str(cursor[0]['web'])
    elif 'IIT' in que and askIIT == []:
        answer += "Can you tell me that details of which iit do you want to know?\nFor example...\nDetails of IIT Bombay"
    return answer