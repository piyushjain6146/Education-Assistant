import re,csv
import pandas as pd

def do_faculty_work(que, askIIT, iit_exists):
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
        temp.update({row[5]: row[1]})
    temp1 = sorted(temp.items(), key=lambda kv: kv[0], reverse=True)

    # data_frame = pd.read_csv('nirf1.csv', usecols=['NAME','TLR'])
    # sorted_df = data_frame.sort_values(by='TLR')
    # length = len(data_frame)-1

    if getMax != None:
        flag = 1
        # Remaining :  sort data according to percentage of placement
        answer += answer + "\n" + str(temp1[0][1]) + " has " + str(temp1[0][0]) + " percentage of PhD Faculties."
        # answer += answer + "\n" + str(sorted_df.iloc[length:,0:1]) + " has " + str(sorted_df.iloc[length:,1:2]) + " percentage of PhD Faculties."

    if getMin != None:
        flag = 1
        # Remaining :  sort data according to percentage of placement
        answer += answer + "\n" + str(temp1[len(temp1) - 1][1]) + " has " + str(temp1[len(temp) - 1][0]) + " percentage of PhD Faculties."
        # answer += answer + "\n" + str(sorted_df.iloc[0:1,0:1]) + " has " + str(sorted_df.iloc[0:1,1:2]) + " percentage of PhD Faculties."

    elif flag == 0 and askIIT != []:
        flag = 1
        for item in temp1:
            for i in askIIT:
                if i == item[1]:
                    answer += answer + "\n" + str(i) + " has " + str(item[0]) + " PhD Faculties."
        # for i in askIIT:
        #     answer += answer + "\n" + str(i) + " has " + str(data_frame[data_frame['NAME'].str.match(i)].iloc[0:1,1:2]) + " PhD Faculties."
    elif iit_exists or flag == 0:
        answer += "Can you tell me that PhD Faculties of which iit do you want to know?\nFor example...\nPhD Faculties of IIT Bombay"
    return answer