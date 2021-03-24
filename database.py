import sqlite3
import mylogging

@mylogging.log
def runStatement(statement):
    #run the sql statement
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.execute(statement)
        conn.commit()
        #conn.close()
        return list(cursor)
    except Exception as e:
        print(e)
        #probably log the error here
        return False

@mylogging.log
def runStatements(statements):
    #run the sql statement
    try:
        conn = sqlite3.connect('data.db')
        results = []
        for statement in statements:
            cursor = conn.execute(statement)
            conn.commit()
            print(list(cursor))
            results.append(list(cursor)[0])
        return results
    except Exception as e:
        print(e)
        #probably log the error here
        return False

@mylogging.log
def checkIfNameIsTaken(name):
    statement = f"""
SELECT Username
From Players
WHERE Username = '{name}'
    """
    return len(runStatement(statement))==0#check that this is what I need to do here when the runstatement() function is implemented.

@mylogging.log
def getActiveCosmetic(username):
    statement = f"""
        SELECT Cosmetics.CosmeticValue
FROM Cosmetics
INNER JOIN Players
ON Players.ActiveCosmetic = Cosmetics.CosmeticID
WHERE Player.Username = '{username}';
    
        """
    return runStatement(statement)[0][0]

@mylogging.log
def verifyPassword(username, password):
    statement = f"""
SELECT Password
FROM Players
WHERE Username = '{username}';
"""
    print(runStatement(statement))
    return password == runStatement(statement)[0][0]

@mylogging.log
def getUnlockedCosmetics(username):
    statement = f"""
SELECT CosmeticID
FROM UnlockedCosmetics
WHERE Username = '{username}';

"""
    return runStatement(statement)[0]



@mylogging.log
def getLeaderboard(numPlayers):
    statement = f"""
Select Username
FROM Players
ORDERBY Points DESC 
LIMIT {numPlayers};
"""
    return runStatement(statement)[0]

@mylogging.log
def addNewUser(username, password):
    statement = f"""
INSERT INTO Players (Username, Password, Points, activeCosmetic)
VALUES ('{username}', '{password}', 0, 0);
"""

    return  runStatement(statement) != False

@mylogging.log
def changeActiveCosmetic(username, newCosmeticID):
    statement = f"""
UPDATE Players
SET ActiveCosmetic = '{newCosmeticID}'
WHERE Username = '{username}'';
"""
    return runStatement(statement) != False

@mylogging.log
def unlockNewCosmetic(username, cosmeticID):
    statement = f"""
INSERT INTO UnlockedCosmetics
VALUES('{username}', '{cosmeticID}');
"""
    return runStatement(statement) != False

@mylogging.log
def createTables():
    statements = ["""
CREATE TABLE Players (
Username VARCHAR(30) NOT NULL,
Password VARCHAR(100) NOT NULL,
Points BIGINT(255) NOT NULL,
activeCosmetic INT(255) NOT NULL,
PRIMARY KEY (Username)
);""",
"""
CREATE TABLE Cosmetics(
CosmeticID INT(255) NOT NULL,
CosmeticValue VARCHAR(100) NOT NULL,
PRIMARY KEY (CosmeticID)
);""",
"""
CREATE TABLE UnlockedCosmetics(
Username VARCHAR(30) NOT NULL,
CosmeticID INT(255) NOT NULL,
PRIMARY KEY (Username)
);

    """]
    return runStatements(statements) != False


