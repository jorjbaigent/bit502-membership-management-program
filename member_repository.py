#------------------------------------------
#BIT502 Assessment 3, Jorj Baigent, 5132617
#------------------------------------------
"""Database access for the supplied Appendix C membership schema"""

#------------------------------------------
#IMPORTS
#------------------------------------------
import sqlite3

from member_options import (
    EXTRAS,
    MEMBERSHIP_PLANS, 
    MEMBERSHIP_PRICES,
    PAYMENT_PLANS
)

#------------------------------------------
#VARIABLES
#------------------------------------------
DATABASE_PATH = "aurora_archive.db"

#Holds extra columns and corresponding database columns
EXTRAS_COLUMNS = {
    "Book Rental": "Extra_Book_Rental",
    "Private Area Access": "Extra_Private_Area",
    "Monthly Booklet": "Extra_Booklet",
    "Online ebook Rental": "Extra_Ebook_Rental"
}


#------------------------------------------
#MAIN CODE
#------------------------------------------
class MemberRepository:
    """Retrieves members using the provided database"""

    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path
        self.initialize()

    #Tries to connect to database
    def initialize(self):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()

        #Creates the table if it does not exist
        try:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS Memberships (
                    MemberID INTEGER PRIMARY KEY NOT NULL,
                    First_Name TEXT NOT NULL,
                    Last_Name TEXT NOT NULL,
                    Address TEXT NOT NULL,
                    Mobile TEXT NOT NULL,
                    Membership_Plan TEXT NOT NULL,
                    Payment_Plan TEXT NOT NULL,
                    Extra_Book_Rental BOOLEAN NOT NULL,
                    Extra_Private_Area BOOLEAN NOT NULL,
                    Extra_Booklet BOOLEAN NOT NULL,
                    Extra_Ebook_Rental BOOLEAN NOT NULL,
                    Has_Library_Card BOOLEAN NOT NULL,
                    Library_Card_Number TEXT
                )"""
            )
            connection.commit()

        #Closes the cursor and connection when finished
        finally:
            cursor.close()
            connection.close()

    #Adds member to the database
    def add_member(self, details):

        #Gets the extra values from user input and saves in list
        selected_extras = set(details["extras"])
        extras_values = [
            int(name in selected_extras) for name in EXTRAS_COLUMNS
        ]

        #Gets values from user input in register_member.py
        values = (
            details["first_name"],
            details["last_name"],
            details["address"],
            details["mobile"],
            details["membership_plan"],
            details["payment_plan"],
            *extras_values,
            int(details["has_library_card"]),
            details["library_id"] if details["has_library_card"] else ""
        )

        #Connection to database
        connection = sqlite3.connect(self.database_path)

        #Cursor
        cursor = connection.cursor()

        #Tries to add member to database
        try:
            cursor.execute(
                """INSERT INTO Memberships (
                    First_Name,
                    Last_Name,
                    Address,
                    Mobile,
                    Membership_Plan, 
                    Payment_Plan,
                    Extra_Book_Rental,
                    Extra_Private_Area,
                    Extra_Booklet,
                    Extra_Ebook_Rental,
                    Has_Library_Card,
                    Library_Card_Number
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )""", values
            )

            member_id = cursor.lastrowid

            #Commits new member to database
            connection.commit()

            return member_id
        finally:
            #Closes cursor and connection
            cursor.close()
            connection.close()

    #Searches database for members
    def search_members(self, member_id=None, last_name="", membership_plan=None, payment_plan=None, partial=False):

        #Creates empty lists for conditions and parameters
        conditions = []
        parameters = []

        #Checks whether an id parameter has been provided and adds it to the conditions and parameters lists
        if member_id not in (None, ""):

            conditions.append("MemberID = ?")
            parameters.append(int(member_id))

        #Checks whether a last name parameter has been provided and adds it to the conditions and parameters lists.
        if last_name:

            if partial: #Allows partial search if the checkbox has been selected

                conditions.append("Last_Name LIKE ? COLLATE NOCASE")
                parameters.append(f"%{last_name}%")

            else: #Only allows full match if the checkbox is left unselected

                conditions.append("Last_Name = ? COLLATE NOCASE")
                parameters.append(last_name)

        #Checks whether a membership plan parameter has been provided and adds it to the conditions and parameters lists.
        if membership_plan:

            conditions.append("Membership_Plan = ?")
            parameters.append(membership_plan)

        #Checks whether a payment plan parameter has been provided and adds it to the conditions and parameters lists.
        if payment_plan:

            conditions.append("Payment_Plan = ?")
            parameters.append(payment_plan)

        #Putting together the where clause
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        #Putting together the query
        query = f"""SELECT 
                MemberID, 
                First_Name,
                Last_Name,
                Address,
                Mobile,
                Membership_Plan,
                Payment_Plan,
                Extra_Book_Rental,
                Extra_Private_Area,
                Extra_Booklet,
                Extra_Ebook_Rental,
                Has_Library_Card,
                Library_Card_Number
                FROM Memberships {where_clause} ORDER BY Last_Name COLLATE NOCASE, First_Name COLLATE NOCASE, MemberID"""

        #Connects to the database and saves it to a variable
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        #Creates a cursor and saves it to a variable
        cursor = connection.cursor()

        #Tries to execute the search query 
        try:
            cursor.execute(query, parameters)

            #Saves all rows selected
            rows = cursor.fetchall()

            return [dict(row) for row in rows]
        
        finally:
            #Closes cursor and connection
            cursor.close()
            connection.close()

    #Gets information about member for View More box
    def get_member(self, member_id):

        members = self.search_members(member_id=member_id)
        return members[0] if members else None

    #Gets membership statistics
    def get_statistics(self):
        #Creates a connection to the database and saves it to variable
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        #Creates a cursor and saves it to a variable
        cursor = connection.cursor()

        #Tries to execute the queries to select membership statistics
        try: 
            #Gets total count from memberships
            cursor.execute(
                "SELECT COUNT(*) AS total FROM Memberships"
            )

            #Gets total member count
            total = cursor.fetchone()["total"]

            #Gets total counts for each membership plan
            membership_counts = {plan: 0 for plan in MEMBERSHIP_PLANS}

            #Updates membership counts
            membership_counts.update({
                row["Membership_Plan"]: row["total"]
                for row in self._fetch_all(
                    cursor,
                    """SELECT Membership_Plan, COUNT(*) AS total FROM Memberships GROUP BY Membership_Plan"""
                )
            })

            #Gets total counts for each payment plan
            payment_counts = {plan: 0 for plan in PAYMENT_PLANS}

            #Updates payment plan counts
            payment_counts.update({
                row["Payment_Plan"]: row["total"]
                for row in self._fetch_all(
                    cursor,
                    """SELECT Payment_Plan, COUNT(*) AS total FROM Memberships GROUP BY Payment_Plan"""
                )
            })

            #Gets counts for each extra and for no extras selected
            extras_counts = {}
            for name, column in EXTRAS_COLUMNS.items():
                cursor.execute(f"SELECT COUNT(*) FROM Memberships WHERE {column} = 1")
                extras_counts[name] = cursor.fetchone()[0]
            cursor.execute(
                """SELECT COUNT(*) FROM Memberships WHERE Extra_Book_Rental = 0 AND Extra_Private_Area = 0 AND Extra_Booklet = 0 AND Extra_Ebook_Rental = 0"""
            )
            extras_counts["None"] = cursor.fetchone()[0]

            #Gets counts for members with library cards
            cursor.execute("SELECT COUNT(*) FROM Memberships WHERE Has_Library_Card = 1")
            library_cards = cursor.fetchone()[0]

        finally:
            #Closes cursor and connection
            cursor.close()
            connection.close()

        #Rows for the expected income table
        income_rows = [
            (f"{plan} Plan", MEMBERSHIP_PRICES[plan], membership_counts[plan]) for plan in MEMBERSHIP_PLANS
        ]
        income_rows.extend(
            (name, EXTRAS[name], extras_counts[name]) for name in EXTRAS
        )

        return {
            "total": total,
            "membership_counts": membership_counts,
            "payment_counts": payment_counts,
            "extras_counts": extras_counts,
            "library_cards": library_cards,
            "income_rows": [
                (option, cost, count, cost * count) for option, cost, count in income_rows
            ]
        }
    @staticmethod
    def _fetch_all(cursor, query):
        cursor.execute(query)
        return cursor.fetchall()

        
