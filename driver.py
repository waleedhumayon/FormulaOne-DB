import mysql.connector

'''
This function focuses on gathering user input about the password, username and host name in order to connect to the
database.
'''


def user_input():
    user_details = []
    username = input("Please enter your MYSQL username: ")
    password = input("Please enter your MYSQL password: ")
    host = input("Please enter your host: ")
    user_details.append(username)
    user_details.append(password)
    user_details.append(host)
    return user_details


def intro():
    print("\nWelcome to the Formula 1 Database (2000-2017). This program will allow you to extract critical data regarding"
          " Formula 1 races!\n")
    print("The program has three main modes:\n"
          "- Analyze: Where you extract information about different Formula 1 races and qualifying sessions, as well"
          " as drivers and their performance.\n"
          "- Create: Where you get to create your own records for races in the F1 Official Game.\n"
          "- Update/Remove: Where you can update or remove your records to reflect your progress!\n"
          " You can always exit the program at any time by pressing E\n")


'''
This function focuses on the UPDATE and REMOVE functionality from within the CRUD operations.
It calls different SQL queries and cleans the input from the user.

The primary goal for this function is to parse the user's input, and then run the queries required on the database.


'''


def update_remove(cnx):
    input_user = input("\n\nPlease select from the following commands:\n"
                       " (1) Remove Driver Profile: Enter RD\n"
                       " (2) Remove Race Record: Enter RR\n"
                       " (3) Update Race Speed: Enter US\n"
                       " (4) Update Fastest Lap: Enter UL\n"
                       " (5) Update Driver Code: Enter UC\n"
                       " (6) Check existing driver numbers: Enter C\n").upper()

    cursor = cnx.cursor()

    if input_user == "RD":  # Deals with where the user wants to REMOVE a driver profile:
        try:
            delete_driver = int(input("\nPlease enter the driver number for the driver profile you want to delete: \n"))
        except ValueError:
            print("You entered an invalid value, please try again\n")
            return

        try:
            cursor.execute("CALL removeUserDriver(%s);", (delete_driver,))
            cnx.commit()
            print("Rows removed: " + str(cursor.rowcount))
            cursor.close()
        except mysql.connector.Error:
            print("Could not remove your entry, please try again! Make sure the driver exists in the records\n")

    elif input_user == "RR":  # Deals with where the user wants to REMOVE a race record.
        delete_race = input("Please enter the driver number for the race records you want to delete: \n")
        delete_name = input("Please enter the name of the race you want to delete: \n")

        try:
            cursor.execute("CALL removeUserRace(%s, %s);", (delete_race, delete_name))
            cnx.commit()
            print("Rows removed: " + str(cursor.rowcount))
            cursor.close()
        except mysql.connector.Error:
            print("Could not remove your entry, please try again! Make sure the race exists in the records\n")

    elif input_user == "US":  # Deals with where the user wants to UPDATE race speed.
        try:
            user_number = int(input("Please enter the driver number: \n"))
        except ValueError:
            print("Error, The driver number must be a number\n")
            return
        update_race = input("Please enter the name of the race you want to update your speed for: \n")
        new_speed = input("Please enter your new speed: \n")

        try:
            cursor.execute("CALL updateRaceSpeed(%s ,%s, %s);", (user_number, update_race, new_speed))
            cnx.commit()
            print("Rows updated: " + str(cursor.rowcount))
            cursor.close()
        except mysql.connector.Error:
            print("Could not update your entry, please try again! Make sure the race exists in the records\n")

    elif input_user == "UL":  # Deals with where the user wants to UPDATE fastest lap.
        try:
            user_number = int(input("Please enter the driver number: \n"))
        except ValueError:
            print("Invalid value, please enter a number\n")
            return
        update_race = input("Please enter the name of the race you want to update your fastest lap for: \n")
        new_lap = input("Please enter your new fastest lap: \n")

        try:
            cursor.execute("CALL updateFastestLap(%s ,%s, %s);", (user_number, update_race, new_lap))
            cnx.commit()
            print("Rows updated: " + str(cursor.rowcount))
            cursor.close()
        except mysql.connector.Error:
            print("Could not update your entry, please try again! Make sure the race exists in the records\n")

    elif input_user == "UC":  # Deals with where the user wants to UPDATE the driver profile.
        try:
            driver_number = int(input("\nPlease enter the driver number for the driver profile you want to update: \n"))
        except ValueError:
            print("Invalid value, please enter a number\n")
            return
        new_code = input("Please enter your new code: \n")

        try:
            cursor.execute("CALL updateDriverCode(%s, %s);", (driver_number, new_code))
            cnx.commit()
            print("Rows Updated: " + str(cursor.rowcount))
            cursor.close()
        except mysql.connector.Error:
            print("Could not update the driver code, please try again! Make sure the driver exists in the records\n")

    elif input_user == "C": # User just wants to see which driver numbers are registered.
        print("The driver numbers stored in the database are: \n")
        cursor.execute("CALL getUserNumbers();")
        for each in cursor:
            print(each[0])
        print("Rows Read: " + str(cursor.rowcount))
        cursor.close()

    else:
        print("Invalid input, please try again\n")


'''
The create function focuses on the CREATE portion of the CRUD operations.

It takes data from user input, verifies it, cleans it and then uses it to process queries on the database. It also
contains a read function that is useful when creating new tuples in the database, to know what data already exists.
'''


def create(cnx):
    create_input = input("\n\nPlease select from the following create commands:\n"
                         " (1) Create Driver Profile: Enter CP\n"
                         " (2) Create Race Record: Enter CR\n"
                         " (3) Check existing driver numbers in the database: Enter C\n").upper()

    cursor = cnx.cursor()

    if create_input == "CP":
        try:
            driver_number = int(input("\nPlease enter your driver number\n"))
        except ValueError:
            print("Invalid value, must be a number\n")
            return
        driver_name = input("Please enter your first name\n")
        driver_surname = input("Please enter your surname\n")
        driver_constructor = input(
            "Please enter the constructor name you drive for. This must be a valid constructor"
            "from the official Formula 1 game: e.g McLaren\n")
        driver_code = input("Please enter the driver code you have: e.g HAM\n")
        driver_nationality = input("Please enter your nationality\n")
        val = (driver_number, driver_name, driver_surname, driver_constructor, driver_code, driver_nationality)
        try:
            cursor.execute("CALL addUserDriver(%s, %s, %s, %s, %s, %s);", val)
            cnx.commit()
            print("Rows Added: " + str(cursor.rowcount))
            cursor.close()
        except mysql.connector.Error:
            print("Could not add your entry, please try again\n")

    elif create_input == "CR":
        try:
            driver_number = int(input("\nPlease enter your driver number\n"))
        except ValueError:
            print("Invalid value, must be a number\n")
            return
        race_name = input("Please enter the name of the race\n")
        final_position = input("Please enter your final position in the race\n")
        fastest_lap = input("Please enter your fastest lap\n")
        lap_speed = input("Please enter your fastest lap speed\n")
        val = (driver_number, race_name, final_position, fastest_lap, lap_speed)
        try:
            cursor.execute("CALL addUserRace(%s, %s, %s, %s, %s);", val)
            cnx.commit()
            print("Rows Added: " + str(cursor.rowcount))
            cursor.close()
        except mysql.connector.Error:
            print("Could not add your entry, please try again\n")

    elif create_input == "C":
        print("The driver numbers stored in the database are: \n")
        cursor.execute("CALL getUserNumbers();")
        for each in cursor:
            print(each[0])
        print("Rows Read: " + str(cursor.rowcount))
        cursor.close()

    else:
        print("\n Your input was invalid, please try again\n")


'''
This function tackles the READ portion of CRUD. It also takes in input so a more specialized version of the data can
be extracted and provided for the user.

It calls on a cursor to extract information form the database and then presents it to the user.
'''


def analyze(cnx):
    analyze_input = input("\n\nPlease select from the following analysis commands:\n"
                          " (1) Most Podiums by a Driver: Enter DP\n"
                          " (2) Most Podiums by a Constructor: Enter CP\n"
                          " (3) Most Wins by a Driver: Enter DW\n"
                          " (4) Most Wins by a Constructor: Enter CW\n"
                          " (5) Get fastest lap by a driver in a specific race: Enter FL\n"
                          " (6) Get fastest lap speed by a driver in a specific race: Enter FS\n").upper()

    cursor = cnx.cursor()
    years = []
    for i in range(10):
        years.append("200" + str(i))
    for i in range(10, 18):
        years.append("20" + str(i))

    if analyze_input == "DP":
        query = "CALL MostPodiumsDriver();"
        cursor.execute(query)
        podium_data = []
        for rows in cursor.fetchall():
            podium_data.append(rows)
        for each in podium_data:
            print("Name: " + each[0] + " |" " Podiums: " + str(each[1]) + "\n")
        print("Rows read: " + str(cursor.rowcount))
        cursor.close()

    elif analyze_input == "CP":
        query1 = "CALL MostPodiumsConstructor();"
        cursor.execute(query1)
        cpodium_data = []
        for rows in cursor.fetchall():
            cpodium_data.append(rows)
        for each in cpodium_data:
            print("Name: " + each[0] + " |" " Podiums: " + str(each[1]) + "\n")
        print("Rows read: " + str(cursor.rowcount))
        cursor.close()

    elif analyze_input == "DW":
        driver_wins_query = "CALL MostWinsDriver();"
        cursor.execute(driver_wins_query)
        dwins_data = []
        for rows in cursor.fetchall():
            dwins_data.append(rows)
        for each in dwins_data:
            print("Name: " + each[0] + " |" " Wins: " + str(each[1]) + "\n")
        print("Rows read: " + str(cursor.rowcount))
        cursor.close()

    elif analyze_input == "CW":
        constructor_wins_query = "CALL MostWinsConstructor();"
        cursor.execute(constructor_wins_query)
        cwins_data = []
        for rows in cursor.fetchall():
            cwins_data.append(rows)
        for each in cwins_data:
            print("Name: " + each[0] + " |" " Wins: " + str(each[1]) + "\n")
        print("Rows read: " + str(cursor.rowcount))
        cursor.close()

    elif analyze_input == "FL":
        surname = input("Please enter the drivers surname: \n").capitalize()
        first_name = input("Please enter the driver's first name: \n").capitalize()
        race_name = input(
            "Please enter the name of the race (without Grand Prix) e.g Monaco, Australian: \n").capitalize()
        full_race_name = race_name + " Grand Prix"
        race_year = input("Please enter the year the race took place: \n")
        if race_year not in years:
            print("Invalid year. Try again\n")
            return
        var = (surname, first_name, full_race_name, race_year)
        try:
            cursor.execute("SELECT FastestLapInRace(%s,%s,%s,%s)", var)
            for each in cursor.fetchall():
                if each[0] is not None:
                    print("Fastest Lap: ")
                    print(each[0])
                else:
                    print("The driver did not set a fastest lap in this race\n")
            print("Rows read: " + str(cursor.rowcount))
            cursor.close()
        except mysql.connector.Error:
            print("Could not find a fastest lap record for that driver/race combination\n")

    elif analyze_input == "FS":
        surname = input("Please enter the drivers surname: \n").capitalize()
        first_name = input("Please enter the driver's first name: \n").capitalize()
        race_name = input(
            "Please enter the name of the race (without Grand Prix) e.g Monaco, Australian: \n").capitalize()
        full_race_name = race_name + " Grand Prix"
        race_year = input("Please enter the year the race took place: \n")
        if race_year not in years:
            print("Invalid year. Try again\n")
            return
        var = (surname, first_name, full_race_name, race_year)
        try:
            cursor.execute("SELECT FastestSpeed(%s,%s,%s,%s)", var)
            for each in cursor.fetchall():
                print("Fastest Speed: ")
                print(each[0])
            print("Rows read: " + str(cursor.rowcount))
            cursor.close()
        except mysql.connector.Error:
            print("Could not find a fastest lap record for that driver/race combination\n")


'''
This is the main portion of the program that establishes a connection with the database. It allows the user to enter 
input and functions as the main menu. It further delegates performing specific actions to the much larger functions 
above. 

Upon getting an exit prompt, it terminates the connection to the database and exits the program with a message.
'''


def program(cnx):
    while True:
        config = {'host': input_data[2], 'port': 3306, 'database': 'saeedwproject', 'user': input_data[0],
                  'password': input_data[1], 'charset': 'utf8', 'use_unicode': True, 'get_warnings': True, }
        cnx = mysql.connector.connect(**config)

        input_u = input("\nPlease select from the options below\n"
                        " 1. Analyze: Enter A\n"
                        " 2. Create: Enter C\n"
                        " 3. Update/Remove: Enter U or R\n"
                        " 4. Exit: Enter E\n").upper()
        if input_u == "E":
            print("\nConnection to the database closed. Exiting the program!")
            cnx.close()
            break
        elif input_u == "A":
            analyze(cnx)

        elif input_u == "C":
            create(cnx)

        elif input_u == "U" or input_u == "R":
            update_remove(cnx)
        else:
            print("The input was invalid, please try again\n")


if __name__ == "__main__":
    input_data = user_input()
    configuration = {'host': input_data[2], 'port': 3306, 'database': 'saeedwproject', 'user': input_data[0],
                     'password': input_data[1], 'charset': 'utf8', 'use_unicode': True, 'get_warnings': True, }
    try:
        cnx = mysql.connector.connect(**configuration)
        print("Connection Successful")
    except mysql.connector.errors.ProgrammingError:
        print("Invalid user_name and password, please try again")
        exit()

    intro()
    program(cnx)
