

def runStatement(statement):
    #run the sql statement
    try:
        result = ""
        return result
    except:
        #probably log the error here
        return False

def checkIfNameIsTaken(name):
    statement = f"""
SELECT Username
From Players
WHERE Username = {name}
"""
    return len(runStatement())===0#check that this is what I need to do here when the runstatement() function is implemented.

def getActiveCosmetic(username):
    statement = f"""
        SELECT Cosmetics.CosmeticValue
FROM Cosmetics
INNER JOIN Players
ON Players.ActiveCosmetic = Cosmetics.CosmeticID
WHERE Player.Username = “{username}”;
    
        """
    return runStatement(statement)

def verifyPassword(username, password):
    statement = f"""
SELECT Password
FROM Players
WHERE Username = “{username}”;
"""
    return password == runStatement(statement)

def getUnlockedCosmetics(username):
    statement = f"""
SELECT CosmeticID
FROM UnlockedCosmetics
WHERE Username = “{username}”;

"""
    return runStatement(statement)

def getLeaderboard(numPlayers):
    statement = f"""
Select Username
FROM Players
ORDERBY Points DESC 
LIMIT {numPlayers};
"""
    return runStatement(statement)

def addNewUser(username, password):
    statement = f"""
INSERT INTO Players 
VALUES (“{username}”, “{password}”, 0, 0);
"""
    return runStatement(statement) != False

def changeActiveCosmetic(username, newCosmeticID):
    statement = f"""
UPDATE Players
SET ActiveCosmetic = “{newCosmeticID}”
WHERE Username = “{username}”;
"""
    return runStatement(statement) != False

def unlockNewCosmetic(username, cosmeticID):
    statement = f"""
INSERT INTO UnlockedCosmetics
VALUES(“{username}”, “{cosmeticID}”);
"""
    return runStatement(statement) != False


def createTables():
    statement = """
CREATE TABLE Players (
Username VARCHAR(30) NOT NULL,
Password VARCHAR(100) NOT NULL,
Points BIGINT(255) NOT NULL,
activeCosmetic INT(255) NOT NULL,
PRIMARY KEY (Username)
);

CREATE TABLE Cosmetics(
CosmeticID INT(255) NOT NULL,
CosmeticValue VARCHAR(100) NOT NULL,
PRIMARY KEY (CosmeticID)
);

CREATE TABLE UnlockedCosmetics(
Username VARCHAR(30) NOT NULL,
CosmeticID INT(255) NOT NULL,
PRIMARY KEY (Username)
);

    """
    return runStatement(statement) != False


