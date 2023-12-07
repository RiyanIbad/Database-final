import sqlite3
import pandas as pd

def print_table(cursor):
    print()
    print()
    # Extract column names from cursor
    column_names = [row[0] for row in cursor.description]
    # Fetch data and load into a pandas dataframe
    table_data = cursor.fetchall()
    df = pd.DataFrame(table_data, columns=column_names)
    # Examine dataframe
    print(df)
    print(df.columns)

def del_tables(table):
    query = " Drop table if exists " + table
    cursor.execute(query)
def del_views(view):
    query = " Drop view if exists " + view
    cursor.execute(query)
def del_database():
    query = "PRAGMA foreign_keys = OFF;"
    cursor.execute(query)
    del_tables("Usage")
    del_tables("Hired")
    del_tables("Client")
    del_tables("Equipment")
    del_tables("Employee")
    del_tables("Requirement")
# Connects to an existing database file in the current directory
# If the file does not exist, it creates it in the current directory
db_connect = sqlite3.connect('finalproject.db')

# Instantiate cursor object for executing queries
cursor = db_connect.cursor()
del_database()
query = "PRAGMA foreign_keys = ON;"
cursor.execute(query)

#DO WE NEED A CONSTRAINT FOR NUMBER OF DIGITS ON PHONE NUMBER?
query = """
    CREATE TABLE Client(
    ClientNum INT NOT NULL,
    fName VARCHAR(50),
    lName VARCHAR(50),
    address VARCHAR(100),
    number VARCHAR(10),
    PRIMARY KEY(ClientNum)
    );
    """
#ON DELETE CASCADE will delete all of the children of the main tables
# Execute query, the result is stored in cursor
cursor.execute(query)

query = """
    CREATE TABLE Equipment(
    eqID INT,
    description VARCHAR(500),
    usage INT NOT NULL,
    cost FLOAT,
    CONSTRAINT AllowedCost CHECK (cost >= 0)
    CONSTRAINT TimesUsed CHECK (usage >= 0)
    PRIMARY KEY (eqID)
    );
    """
cursor.execute(query)

#CONSTRAINT FOR PHONE NUMBER BEING 10 DIGITS?
query = """
    CREATE TABLE Employee(
    staffNum INT,
    fName VARCHAR(50),
    lName VARCHAR(50),
    address VARCHAR(100),
    salary FLOAT CHECK(salary > 0),
    number INT,
    PRIMARY KEY(staffNum)
    );
    """
cursor.execute(query)
## DOES REQUIREMENT HAVE CLIENTNUM FOREIGN KEY HERE LIKE ER DIAGRAM??
query = """
    CREATE TABLE Requirement(
    reqID INT, 
    startD DATE,
    startT TIME,
    duration TIME,
    clientNum INT,
    comments VARCHAR(500),
    PRIMARY KEY (reqID)
    FOREIGN KEY (clientNum) REFERENCES Client(clientNum)
    );
    """
cursor.execute(query)

query = """
    INSERT INTO Employee
    VALUES 
        (1, 'Alice', 'Johnson', '789 Oak St', 30000, 3456789012),
        (2, 'Bob', 'Williams', '101 Pine St', 32000, 4567890123),
        (3, 'John', 'Ronaldo', '134 Po St', 35000, 4566960123),
        (4, 'Lionel', 'Messi', '563 Po St', 33000, 6566960123),
        (5, 'Lebron', 'James', '431 Spruce St', 31000, 4566966423);
    """
cursor.execute(query)

query= """
    INSERT INTO Equipment
    VALUES 
        (1, 'Vacuum Cleaner', 20, 150.00),
        (2, 'Mop', 9, 20.00),
        (3, 'Broom', 26, 25.00),
        (4, 'Duster', 11, 50.00),
        (5, 'Plunger', 32, 20.00);
"""
cursor.execute(query)

query = """
    INSERT INTO Client
    VALUES
        (1, 'John', 'Doe', '123 Main St', 1234567890),
        (2, 'Jane', 'Smith', '456 Elm St', 2345678901),
        (3, 'Anne', 'Wolf', '573 Palm Dr', 3057836721), 
        (4, 'Maria', 'Wolf', '7025 89th St', 3055312756), 
        (5, 'Carly', 'Hess', '562 45th Pl', 7864539877); 
"""
cursor.execute(query)

query = """
    INSERT INTO Requirement
    VALUES 
        (1, '2024-01-03', '10:30:00', 'Clean bathroom', 4 , 5),
        (2, '2023-12-02', '09:00:00', 'Wash windows', 2, 4),
        (3, '2023-10-02', '07:00:00' ,'Wash floor', 2 , 3),
        (4, '2022-10-22', '05:00:00', 'Clean Kitchen', 1 , 2),
        (5, '2023-05-16', '11:15:00', 'Clean floor tile', 3 , 1); 
"""
cursor.execute(query)
query = """
    SELECT * 
    FROM Client
"""
cursor.execute(query)
print_table(cursor)
query = """
    SELECT *
    FROM Employee

"""
cursor.execute(query)
print_table(cursor)
query = """
    SELECT *
    FROM Requirement

"""
cursor.execute(query)
print_table(cursor)
query = """
    SELECT *
    FROM Equipment

"""
cursor.execute(query)
print_table(cursor)


#Retrieve Client Name with Their Cleaning Start Date and Time
query = """
    SELECT Client.fName, Client.lName, Requirement.StartD, Requirement.startT
    FROM Client
    JOIN Requirement ON Client.clientNum = Requirement.clientNum;
 """
cursor.execute(query)
print_table(cursor)

#calculate total salary expense for all employees
query = """
SELECT SUM(E.salary) AS TotalSalaryExpense
FROM Employee E;
   """
cursor.execute(query)
print_table(cursor)

#retrieve all requirements along with client information
query = """
    SELECT 
        R.reqID,
        R.startD,
        R.startT,
        R.duration,
        R.comments,
        C.fName AS ClientFirstName,
        C.lName AS ClientLastName
    FROM Requirement R
    JOIN Client C ON R.ClientNum = C.ClientNum;
"""
cursor.execute(query)
print_table(cursor)

#Find clients with no cleaning requirements
query = """
SELECT 
    C.ClientNum,
    C.fName,
    C.lName
FROM Client C
LEFT JOIN Requirement R ON C.ClientNum = R.ClientNum
WHERE R.reqID IS NULL;
"""
cursor.execute(query)
print_table(cursor)

#Number of services scheduled in 2024
query =    """
SELECT  * 
    FROM Requirement r
    WHERE startD LIKE '%2024%';
"""
cursor.execute(query)
print_table(cursor)






