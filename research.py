import re, csv

def do_research_work(que, askIIT, iit_exists):
    """
    Write DOCs
    """
    flag = 0
    answer = ''
    matchMax = re.compile(r'greates|max|highest|good|nice|maximum|top|high')
    getMax = matchMax.search(que)

    matchMin = re.compile(r'min|lowest|minimum|low|bad|worst')
    getMin = matchMin.search(que)

    temp = {}
    temp1 = {}
    nirfCSV = open('nirf1.csv', 'r')
    csvReader = csv.reader(nirfCSV)
    next(csvReader)
    for row in csvReader:
        temp.update({row[6]: row[1]})
    temp1 = sorted(temp.items(), key=lambda kv: kv[0], reverse=True)
    # print temp1

    if getMax != None:
        flag = 1
        # Remaining :  sort data according to percentage of placement
        answer += answer + "\n" + str(temp1[0][1]) + " has " + str(temp1[0][0]) + " percentage of publications and research areas."

    if getMin != None:
        flag = 1
        # Remaining :  sort data according to percentage of placement
        answer += answer + "\n" + str(temp1[len(temp1) - 1][1]) + " has " + str(temp1[len(temp) - 1][0]) + " percentage of publications and research areas."

    elif flag == 0 and askIIT != []:
        flag = 1
        for item in temp1:
            for i in askIIT:
                if i == item[1]:
                    answer += answer + "\n" + str(i) + " has " + str(item[0]) + " percentage of publications and research areas."
    elif iit_exists or flag == 0:
        answer += "Can you tell me that Publications or researches of which iit do you want to know?\nFor example...\nPublications of IIT Bombay"

    return answer