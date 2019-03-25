import re, pymongo

def do_fees_work(que, askIIT, iit_exists, test_connection):
    """
    Write DOCs
    """
    flag = 0
    answer = ''
    matchMax = re.compile(
        r'max|highest|maximum|high|top|more|great|greater|(more|greater) than [0-9]+|above [0-9]+|\>(\=)? [0-9]+'
    )
    getMax = matchMax.search(que)
    matchMin = re.compile(
        r'min|lowest|minimum|low|less|lesser|less than [0-9]+|below [0-9]+|\<(\=)? [0-9]+'
    )
    getMin = matchMin.search(que)
    matchBetween = re.compile(
        r'between [0-9]+ and [0-9]+|above [0-9]+ and below [0-9]+|(greater|more) than [0-9]+ and less than [0-9]+| \>(\=)? [0-9]+ and \<(\=)? [0-9]+'
    )
    getBetween = matchBetween.search(que)
    matchacademic = re.compile(r'academic|eduation')
    getacademic = matchacademic.search(que)
    matchmess = re.compile(r'mess')
    getmess = matchmess.search(que)

    # to handle maximaum, more than like que.
    if getMax != None and getBetween == None:
        flag = 1
        temp = getMax.group()
        n1 = re.findall(r'\d+', temp)
        if len(n1) != 0:
            # print('In IF')
            n1 = int(' '.join(n1))
            cursor = test_connection.find({'academic': {
                '$gte': n1
            }}, {
                'name': 1,
                'academic': 1
            })
            try:
                # if data will not be there then this line will give exception
                # print('In TRY')
                if getacademic != None:
                    cursor = test_connection.find({'academic': {
                        '$gte': n1
                    }}, {
                        'name': 1,
                        'academic': 1
                    })
                    answer += "\n" + str(
                        cursor[0]['name']) + "\nAcademic Fees : " + str(
                            cursor[0]['academic'])
                elif getmess != None:
                    cursor = test_connection.find({'mess': {
                        '$gte': n1
                    }}, {
                        'name': 1,
                        'mess': 1
                    })
                    answer += "\n" + str(
                        cursor[0]['name']) + "\nMess Fees : " + str(
                            cursor[0]['mess'])
                elif len(cursor[0]) > 0:
                    for document in cursor:
                        answer += "\nName : " + str(
                            document['name']) + "\nAcademic Fees : " + str(
                                document['academic'])
            except Exception:
                answer += "\nNo Data available according to condition!"
        else:
            # print('In Else')
            try:
                if getacademic != None:
                    cursor = test_connection.find({}, {
                        'name': 1,
                        'academic': 1
                    }).sort('academic', -1).limit(1)
                    answer += "\n" + str(
                        cursor[0]['name']) + "\nAcademic Fees : " + str(
                            cursor[0]['academic'])
                elif getmess != None:
                    cursor = test_connection.find({}, {
                        'name': 1,
                        'mess': 1
                    }).sort('mess', -1).limit(1)
                    answer += "\n" + str(
                        cursor[0]['name']) + "\nMess Fees : " + str(
                            cursor[0]['mess'])
                else:
                    cursor = test_connection.find({}, {
                        'name': '1',
                        'academic': '1',
                        'mess': '1'
                    }).sort('academic', -1).limit(1)
                    answer += "\n" + str(
                        cursor[0]['name']) + "\nAcademic Fees : " + str(
                            cursor[0]['academic']) + "\nMess Fees : " + str(
                                cursor[0]['mess'])
            except Exception:
                answer += "\nNo Data available according to condition!"

    # to handle min, less than like que.
    elif getMin != None and getBetween == None:
        flag = 1
        temp = getMin.group()
        n1 = re.findall(r'\d+', temp)
        if len(n1) != 0:
            n1 = int(' '.join(n1))
            cursor = test_connection.find({'academic': {
                '$lte': n1
            }}, {
                'name': 1,
                'academic': 1
            })
            try:
                # if data will not be there then this line will give exception
                if getacademic != None:
                    cursor = test_connection.find({'academic': {
                        '$lte': n1
                    }}, {
                        'name': 1,
                        'academic': 1
                    })
                    answer += "\n" + str(
                        cursor[0]['name']) + "\nAcademic Fees : " + str(
                            cursor[0]['academic'])
                elif getmess != None:
                    cursor = test_connection.find({'mess': {
                        '$lte': n1
                    }}, {
                        'name': 1,
                        'mess': 1
                    })
                    answer += "\n" + str(
                        cursor[0]['name']) + "\nMess Fees : " + str(
                            cursor[0]['mess'])
                elif len(cursor[0]) > 0:
                    for document in cursor:
                        answer += "\nName : " + str(
                            document['name']) + "\nAcademic Fees : " + str(
                                document['academic'])
            except Exception:
                answer += "\nNo Data available according to condition!"
        else:
            try:
                if getacademic != None:
                    cursor = test_connection.find({}, {
                        'name': 1,
                        'academic': 1
                    }).sort('academic', +1).limit(1)
                    answer += "\n" + str(
                        cursor[0]['name']) + "\nAcademic Fees : " + str(
                            cursor[0]['academic'])
                elif getmess != None:
                    cursor = test_connection.find({}, {
                        'name': 1,
                        'mess': 1
                    }).sort('mess', +1).limit(1)
                    answer += "\n" + str(
                        cursor[0]['name']) + "\nMess Fees : " + str(
                            cursor[0]['mess'])
                else:
                    cursor = test_connection.find({}, {
                        'name': '1',
                        'academic': '1',
                        'mess': '1'
                    }).sort('academic', +1).limit(1)
                    answer += "\n" + str(
                        cursor[0]['name']) + "\nAcademic Fees : " + str(
                            cursor[0]['academic']) + "\nMess Fees : " + str(
                                cursor[0]['mess'])
            except Exception:
                answer += "\nNo Data available according to condition!"

    # to handle between like que.
    elif getBetween != None:
        flag = 1
        temp = getBetween.group()
        # print('In Between')
        n1, n2 = re.findall(r'\d+', temp)
        n1 = int(n1)
        n2 = int(n2)
        n1, n2 = max(n1, n2), min(n1, n2)
        # print(n1,n2)
        cursor = test_connection.find({'academic': {
            '$lte': n1,
            '$gte': n2
        }}, {
            'name': 1,
            'academic': 1
        })
        try:
            if getacademic != None:
                # print('In Academic')
                cursor = test_connection.find(
                    {'academic': {
                        '$lte': n1,
                        '$gte': n2
                    }}, {
                        'name': 1,
                        'academic': 1
                    })
                for document in cursor:
                    answer += "\nName : " + str(
                        document['name']) + "\nAcademic Fees : " + str(
                            document['academic'])
            elif getmess != None:
                # print('In MESS')
                cursor = test_connection.find(
                    {'mess': {
                        '$lte': n1,
                        '$gte': n2
                    }}, {
                        'name': 1,
                        'mess': 1
                    })
                for document in cursor:
                    answer += "\nName : " + str(
                        document['name']) + "\nMess Fees : " + str(
                            document['mess'])
            # if data will not be there then this line will give exception
            elif len(cursor[0]) > 0:
                # print('In LENGTH')
                for document in cursor:
                    answer += "\nName : " + str(
                        document['name']) + "\nAcademic Fees : " + str(
                            document['academic'])
        except Exception:
            answer += "\n" + "No Data available according to condition!"
    elif getacademic != None and flag == 0:
        # print('In ACA')
        flag = 1
        for i in askIIT:
            cursor = test_connection.find({'name': str(i)}, {'academic': 1})
            answer += "\n" + "Fees Details of " + str(
                i) + "\nAcademic Fees : " + str(cursor[0]['academic'])
    elif getmess != None and flag == 0:
        flag = 1
        # print('In MESS')
        for i in askIIT:
            cursor = test_connection.find({'name': str(i)}, {'mess': 1})
            answer += "\n" + "Fees Details of " + str(
                i) + "\nMess Fees : " + str(cursor[0]['mess'])
    elif flag == 0 and askIIT != []:
        flag = 1
        # print('In NONE')
        for i in askIIT:
            cursor = test_connection.find({'name': str(i)}, {
                'academic': 1,
                'mess': 1
            })
            answer += "\n" + "Fees Details of " + str(
                i) + "\nAcademic Fees : " + str(
                    cursor[0]['academic']) + "\nMess Fees : " + str(
                        cursor[0]['mess'])
    elif flag == 0 or iit_exists:
        flag = 1
        answer += "Can you tell me that fees of which iit do you want to know?\nFor example...\n Fees of IIT Bombay"

    return answer