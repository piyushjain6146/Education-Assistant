import re, pymongo

def do_seats_work(que, askIIT, iit_exists, test_connection):
    """
    Write DOCs
    """
    flag = 0
    answer = ""
    matchfseat = re.compile(r'fseats(s)?|[f|female]seat(s)?|[f|female]place(s)?|female|woman|women|girl(s)?')  # For female Seats
    getfseat = matchfseat.search(que)

    # matchmseat = re.compile(
    #     r'[m|male]seat(s)?|[m|male]place(s)?|male|man|woman|boy(s)?') # For male Seats
    # getmseat = matchmseat.search(que)

    if getfseat != None:
        flag = 1
        for i in askIIT:
            cursor = test_connection.find({'name': str(i)}, {'departments': 1})
            for document in cursor:
                for dept in document['departments']:
                    answer = answer + "\n" + str(dept['name']) + " : " + str(
                        dept['fseats'])
            answer = answer + "\n" + "Total Female seats in " + str(
                i) + " are : " + answer

    # elif getmseat != None and getfseat == None:
    #     cursor = test_connection.find(
    #         {'name': askIIT}, {'departments': 1})

    #     for document in cursor:
    #         for dept in document['departments']:
    #             answer = answer+"\n" + str(dept['name']) + " : " + str(int(dept['seats']) - int(dept['fseats']))
    #     answer = "Total Male seats in "+askIIT + " are : "+answer

    elif askIIT != [] and getfseat == None:
        flag = 1
        for i in askIIT:
            cursor = test_connection.find({'name': str(i)}, {'departments': 1})

            for document in cursor:
                for dept in document['departments']:
                    answer = answer + "\n" + str(dept['name']) + " : " + str(
                        dept['seats'])

            answer = answer + "\n" + "Total Seats in " + str(
                i) + " are : " + answer
    elif not iit_exists or flag == 0:
        answer += "Can you tell me that seats of which iit do you want to know?\nFor example...\nSeats of IIT Bombay"
    return answer