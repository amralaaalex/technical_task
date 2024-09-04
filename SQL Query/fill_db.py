import mysql.connector
from mysql.connector import errorcode

# Database connection configuration
config = {
    'user': 'root',
    'password': '0100xyz!@#COM',
    'host': 'localhost'
}

# Connect to MySQL Server
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Create Database
    cursor.execute("CREATE DATABASE IF NOT EXISTS InvoiceDB")
    cursor.execute("USE InvoiceDB")

    # Create Customers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerName VARCHAR(255) NOT NULL,
        ReferringCustomerID INT,
        FOREIGN KEY (ReferringCustomerID) REFERENCES Customers(CustomerID)
    )
    """)

    # Create Invoices table, allowing NULL in CustomerID
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Invoices (
        InvoiceID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerID INT,
        BillingDate DATE NOT NULL,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    )
    """)

    # Insert data into Customers table
    cursor.execute("INSERT INTO Customers (CustomerName, ReferringCustomerID) VALUES (%s, %s)", ('John Doe', None))
    cursor.execute("INSERT INTO Customers (CustomerName, ReferringCustomerID) VALUES (%s, %s)", ('Jane Smith', 1))
    cursor.execute("INSERT INTO Customers (CustomerName, ReferringCustomerID) VALUES (%s, %s)", ('Alice Johnson', None))
    cursor.execute("INSERT INTO Customers (CustomerName, ReferringCustomerID) VALUES (%s, %s)", ('Bob Brown', 3))
    cursor.execute("INSERT INTO Customers (CustomerName, ReferringCustomerID) VALUES (%s, %s)", ('Charlie White', None))

    # Insert data into Invoices table, including invoices with NULL CustomerID
    cursor.execute("INSERT INTO Invoices (CustomerID, BillingDate) VALUES (%s, %s)", (1, '2024-09-01'))
    cursor.execute("INSERT INTO Invoices (CustomerID, BillingDate) VALUES (%s, %s)", (2, '2024-09-02'))
    cursor.execute("INSERT INTO Invoices (CustomerID, BillingDate) VALUES (%s, %s)", (3, '2024-09-03'))
    cursor.execute("INSERT INTO Invoices (CustomerID, BillingDate) VALUES (%s, %s)", (4, '2024-09-04'))
    cursor.execute("INSERT INTO Invoices (CustomerID, BillingDate) VALUES (%s, %s)", (5, '2024-09-05'))

    # Invoices without a customer
    cursor.execute("INSERT INTO Invoices (CustomerID, BillingDate) VALUES (%s, %s)", (None, '2024-09-06'))
    cursor.execute("INSERT INTO Invoices (CustomerID, BillingDate) VALUES (%s, %s)", (None, '2024-09-07'))

    # Commit the transaction
    cnx.commit()

    print("Database, tables, and data created successfully, including invoices without customers.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    cursor.close()
    cnx.close()
