import sqlite3

connection = sqlite3.connect("freshers.db")
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS faq (
        id INTEGER PRIMARY KEY,
        keywords TEXT,
        answer TEXT
    )
''')

connection.commit()
faq_entries = [
    ("bus transport unilink route", "Unilink is the University's own bus service. Key routes: U1 connects Southampton Airport Parkway, Highfield Campus, Portswood, Civic Centre, West Quay, Town Quay and NOCS. U2 connects Highfield Campus, Avenue Campus, Bassett Green and Southampton Central Station. U6 connects Southampton General Hospital, Boldrewood Campus, Highfield Campus, Portswood, Civic Centre and Southampton Central Station."),
    ("bus pass free halls unilink ticket", "Students living in University halls get a free Unilink bus pass included in their accommodation. Non-halls students can still buy discounted Unilink tickets, which also work on any Bluestar bus within the Southampton zone."),
    ("library hartley study hours", "The Hartley Library on Highfield Campus is the University's main library. It extends to 24-hour opening during peak weeks in term time, and stays open until at least midnight most of the rest of term. Exact current opening hours are posted at library.soton.ac.uk/opening, since they shift term to term."),
    ("halls catering dining meal plan food", "Highfield Hall is part-catered: on weekdays you get breakfast and a main meal, plus brunch on Saturday and lunch on Sunday, all usable at Campus Kitchen outlets around campus. A catered package costs around £60 a week. Non-catered students pay per meal using their student card at any catering outlet."),
    ("accommodation halls residence where live", "University of Southampton halls include Archers Road, City Gateway, Erasmus Park, Glen Eyre, Highfield Halls, and Wessex Lane. All halls contracts include utility bills, wifi, laundry access, contents insurance, and secure bike storage. First years are guaranteed a room offer if they apply by the University's stated deadline (1 July for main entry)."),
    ("kitchen cook own food self catered", "Even in part-catered halls like Highfield Hall, residents have access to a small shared kitchen to store and cook their own food outside of set meal times.")
]

cursor.executemany("INSERT INTO faq (keywords, answer) VALUES (?, ?)", 
faq_entries)
connection.commit()
connection.close()
