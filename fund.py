import re, csv

def do_fund_work(que, askIIT, iit_exists):
    """
    Write DOCs
    """
    answer = ''
    flag = 0
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
        temp.update({row[9]: row[1]})
    temp1 = sorted(temp.items(), key=lambda kv: kv[0], reverse=True)

    if getMax != None:
        flag = 1
        # Remaining :  sort data according to percentage of placement
        answer += answer + "\n" + str(temp1[0][1]) + " has " + str(
            temp1[0][0]) + " percentage of investors and fundings."

    if getMin != None:
        flag = 1
        # Remaining :  sort data according to percentage of placement
        answer += answer + "\n" + str(
            temp1[len(temp1) - 1][1]) + " has " + str(temp1[
                len(temp) - 1][0]) + " percentage of investors and fundings."

    elif flag == 0 and askIIT != []:
        flag = 1
        for item in temp1:
            for i in askIIT:
                if i == item[1]:
                    answer += answer + "\n" + str(i) + " has " + str(
                        item[0]) + " percentage of investors and fundings."
    elif iit_exists or flag == 0:
        answer += "Can you tell me that of investors or funding of which iit do you want to know?\nFor example...\nInvestors of IIT Bombay"
    return answer