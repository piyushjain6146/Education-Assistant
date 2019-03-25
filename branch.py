import re, pymongo

def do_branch_work(que, askIIT, iit_exists, test_connection):
    """
    Write DOCs
    """
    answer = ''
    flag = 0
    matchfield = re.compile(r'count|how many|total')
    getfield = matchfield.search(que)
    if getfield != None:
        flag = 1
        count = 0
        for i in askIIT:
            cursor = test_connection.find({'name': str(i)}, {'departments': 1})
            for document in cursor:
                for dept in document['departments']:
                    count += 1
                    # answer += "\n" + str(dept['name'])
            answer += "\n" + " Total Departments of " + str(i) + " are " + str(count)
    elif askIIT != [] and getfield == None:
        flag = 1
        for i in askIIT:
            answer += "\n" + "Departments of " + str(i) + " are as follows: "
            cursor = test_connection.find({'name': str(i)}, {'departments': 1})
            for document in cursor:
                for dept in document['departments']:
                    answer += "\n" + str(dept['name'])
    elif iit_exists or flag == 0:
        answer += "Can you tell me that departments of which iit do you want to know?\nFor example...\nDepartments of IIT Bombay"
    return answer