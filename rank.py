import re, csv

def do_rank_work(que,askIIT, iit_exists):
    """
    Write DOCs
    """
    answer = ''
    flag = 0
    temp = open('nirf1.csv', 'r')
    csvReader = csv.reader(temp)

    matchDigits = re.compile(r'(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tehnth|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen)')
    getDigits = matchDigits.search(que)
    if getDigits == None:
        if askIIT != []:
            flag = 1
            count = 0
            for row in csvReader:
                if count == 0:
                    count += 1
                else:
                    if row == []:
                        continue
                    else:
                        if row[1] in askIIT:
                            answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                            count += 1
        elif askIIT == [] and iit_exists:
            count = 0
            for row in csvReader:
                if count == 0:
                    count += 1
                else:
                    if row == []:
                        continue
                    else:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        count += 1
        elif not iit_exists or flag == 0:
            answer += "Can you tell me that rank of which iit do you want to know?\nFor example...\nRank of IIT Bombay"
    else:
        flag = 1
        count = 0
        for row in csvReader:
            if count == 0:
                count += 1
            else:
                if row == []:
                    continue
                else:
                    if ('first' in que) or ('one' in que) and count == 1:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        break
                    elif ('two' in que or 'second' in que) and count == 2:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        break
                    elif ('three' in que or 'third' in que) and count == 3:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        break
                    elif ('four' in que or 'fourth' in que) and count == 4:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        break
                    elif ('five' in que or 'fifth' in que) and count == 5:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        break
                    elif ('six' in que or 'sixth' in que) and count == 6:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        break
                    elif ('seven' in que or 'seventh' in que) and count == 7:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        break
                    elif ('eight' in que or 'eighth' in que) and count == 8:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        break
                    elif ('nine' in que or 'ninth' in que) and count == 9:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        break
                    elif ('ten' in que or 'tenth' in que) and count == 10:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        break
                    elif ('eleven' in que or 'eleventh' in que) and count == 11:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        break
                    elif ('twelve' in que or 'twelfth' in que) and count == 12:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        break
                    elif ('thirteen' in que or 'thirteenth' in que) and count == 13:
                        answer = answer + "\n" + "Rank of " + str(row[1]) + " is : " + str(row[0])
                        break
                    count += 1
    return answer