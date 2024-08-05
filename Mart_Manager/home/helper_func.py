def checkAuth(uname, pasw):
    mainFlag = False
    userDet = [
            ["Glen", "2001"],
            ["Gladys", "1965"],
            ["Lenisha", "2006"],
            ["Lancy", "1960"]
        ]
    if uname or pasw in userDet:
        for user in userDet:
            if uname == user[0] and pasw == user[1]:
                mainFlag = True
            else:
                pass
    else:
        pass
    return mainFlag