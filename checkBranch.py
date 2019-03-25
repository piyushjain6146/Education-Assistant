import pymongo

def do_check_branch_work(que, departments, yes_no_department, askIIT, test_connection):
    """
    Write Docs
    """
    answer = ''

    for i in askIIT:
        for j in departments:
            cursor = test_connection.find({
                'name': i,
                "departments.name": {
                    '$regex': j,
                    '$options': "$i"
                }
            }, {
                "departments.seats": 1,
                "departments.fseats": 1
            })
            try:
                if len(
                        cursor[0]
                ) > 0:  # if data will not be there then this line will give exception
                    for _ in cursor:
                        # print document
                        answer += "\nYes, " + j + " department is available in " + i
                        # break
            except Exception:
                answer += "\nNo, " + j + " department is not available in " + i
    return answer
