import re, csv

def do_top_work(que, askIIT, cardinal, ordinal, iit_exists, option, queGlobal):
    """
    Write DOCa
    """
    answer = ''
    temp = open('nirf1.csv', 'r')
    csvReader = csv.reader(temp)
    count = 0
    matchNum = re.compile(r'[0-9]+')
    getNum = matchNum.search(que)

    if getNum == None:
        # save current que in queGlobal and send static response for another que.
        if queGlobal == '':
            option = list([
                "Default", "Score", "Teaching,Learning and Resources",
                "Research and Professional Practice", "Graduation Outcomes",
                "Outreach and Inclusivity", "Perception"
            ])
            answer = answer + '1234567890'
            queGlobal = que
        else:
            matchCategory = re.compile(
                r'score|default|teaching|learning|resources|research and professional practice|graduation outcomes|outreach and inclusivity|perception'
            )
            # print(que)
            getCategory = matchCategory.search(str(que))
            criteria = getCategory.group()
            queGlobal = ''
            option = []
            # create a counter variable and remove nirf rank
            for row in csvReader:
                if count == 0:
                    count += 1
                else:
                    if row == []:
                        continue
                    else:
                        if ('default' == criteria):
                            answer = answer + "\n" + str(row[0]) + ":" + str(
                                row[1])
                        elif ('score' == criteria):
                            answer = answer + "\n" + str(row[0]) + ":" + str(
                                row[1]) + ":" + str(row[4])
                        elif ('tlr' == criteria or 'teaching' in criteria
                              or 'learning' in criteria):  # TLR is not working
                            answer = answer + "\n" + str(row[0]) + ":" + str(
                                row[1]) + ":" + str(row[5])
                        elif ('rpc' == criteria or
                              'research and professional practice' == criteria
                              or
                              'research & professional practice' == criteria):
                            answer = answer + "\n" + str(row[0]) + ":" + str(
                                row[1]) + ":" + str(row[6])
                        elif ('go' == criteria
                              or 'graduation outcomes' == criteria):
                            answer = answer + "\n" + str(row[0]) + ":" + str(
                                row[1]) + ":" + str(row[7])
                        elif ('oi' == criteria
                              or 'outreach and inclusivity' == criteria
                              or 'outreach & inclusivity' == criteria):
                            answer = answer + "\n" + str(row[0]) + ":" + str(
                                row[1]) + ":" + str(row[8])
                        elif ('pr' == criteria or 'perception' == criteria):
                            answer = answer + "\n" + str(row[0]) + ":" + str(
                                row[1]) + ":" + str(row[9])

    # handels questions like top 10th IIT or top 10 IIT
    else:
        n = int(getNum.group())
        for row in csvReader:
            if count == 0:
                count += 1
            else:
                if cardinal != ' ':
                    if row == []:
                        continue
                    else:
                        if count <= n:
                            # if "Indian Institute of Technology" in str(row[1]):
                            answer = answer + "\n" + str(row[1]) + ":" + str(
                                row[4])
                            count += 1
                if ordinal != ' ':
                    if row == []:
                        continue
                    else:
                        if n == count:
                            # if "Indian Institute of Technology" in str(row[1]):
                            answer = answer + "\n" + str(row[1]) + ":" + str(
                                row[4])
                        # if "Indian Institute of Technology" not in str(row[1]):
                        count += 1
    return answer, queGlobal, option