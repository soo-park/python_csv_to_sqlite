""" Generates ayasdi_assignment.csv and ayasdi_assignment.db """
import random
import math
# import csv
# import sqlite3
# from sqlite3 import Error


def generate_column(label, values, previous_table):
    """Generate a column with given label and values"""

    if not previous_table:
        result = []
        result.append([label])
        for i in range(0, len(values)):
            result.append([values[i]])
    else:
        result = previous_table
        for i in range(0, len(previous_table)):
            current_item = previous_table[i]
            for j in range(0, len(values)):
                current_item.append(values[j])
    return result


# Generating CSV file
def generate_1st_column():
    """
        labeled as col1
        the index column where the values are 1 to 1 million
    """

    result = generate_column('col1', [1, 2, 3], None)
    return "1st column generated: ", result


def generate_2nd_10th_column():
    """
        The next 9 columns (2 to 10) contain randomly distributed gaussian data
        and are labelled col2_x ... col10_x where 'x' is the mean of the gaussian distribution.
        For example, if you chose means of 10, 20, 30, 40, 50, 60, 70, 80 for col2 through col10,
        the labels are col2_10, col3_20, col4_30 and etc.
        You can choose whatever mean and variance you would like for each column.
    """

    return "2nd - 10th column generated"


def get_random_num_10per_null(max_number):
    """
        add 10% up of the number existing
        if the number is over index, generate null
    """

    tenup = int(math.floor(max_number * 1.1))
    random_location = random.randint(0, tenup)

    if random_location > max_number:
        return None
    else:
        return random_location


def get_random_word_10per_null():
    """
        returns word with 10% possiblity of returning null
    """

    # word_dic = open('wordlist.txt', 'w')
    word_dic = file('wordlist.txt').read().split()
    word_dic_length = len(word_dic)
    random_word_location = get_random_num_10per_null(word_dic_length)
    if random_word_location:
        return word_dic[random_word_location]
    else:
        return None


# English word list downloaded from the following link
# http://www-01.sil.org/linguistics/wordlists/english/
def generate_11th_19th_column():
    """
        Columns 11 to 19 are labelled as col11...col19,
        where each column has random strings selected from the English Dictionary.
        10% randomly distributed nulls in this column as well.
    """

    word = get_random_word_10per_null()

    if word:
        return "11th - 19th column generated with:", word
    else:
        return "11th - 19th column generated with: ", "You got None"


def generate_20th_column():
    """
        Column 20 has random dates selected between January 1, 2014 to December 31, 2014.
        No nulls in this column.
    """

    return "20th column generated"


def run_all():
    """
    run all functions that generates the table
    """

    first = generate_1st_column()
    second_10th = generate_2nd_10th_column()
    eleventh_19th = generate_11th_19th_column()
    twentiesth = generate_20th_column()

    print first, "\n", second_10th, "\n", eleventh_19th, "\n", twentiesth

run_all()


# ########################### generate csv
# def generate_csv_table(table_values):
#     """generate csv table with given array"""

#     with open('ayasdi_assignment.csv', 'wb') as csvfile:
#         filewriter = csv.writer(csvfile,
#             delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

#         # write the rest of the column values
#         for i in range(0, len(table_values)):
#             filewriter.writerow([table_values[i]])


# ########################### Loading the CSV table to sqlite
# def create_connection(db_file):
#     """
#         create a database connection to the SQLite database
#         specified by the db_file
#         :param db_file: database file
#         :return: Connection object or None
#     """

#     try:
#         # con = sqlite3.connect(":memory:")
#         conn = sqlite3.connect(db_file)
#         return conn
#     except Error as error:
#         print error

#     return None


# def add_all_lines(conn):
#     """
#         add all lines in CSV to the SQLite database.
#         Query all rows in the tasks table
#         :param conn: the Connection object
#         :return:
#     """

#     cur = conn.cursor()
#     cur.execute("DROP TABLE IF EXISTS ayasdi_table;")
#     cur.execute("CREATE TABLE ayasdi_table (col1, col2);")
#     # use your column names here

#     with open('ayasdi_assignment.csv', 'rb') as fin:
#         # `with` statement available in 2.5+
#         # csv.DictReader uses first line in file for column headings by default
#         dr = csv.DictReader(fin) # comma is default delimiter
#         to_db = [(i['col1'], i['col2']) for i in dr]

#     cur.executemany("INSERT INTO ayasdi_table (col1, col2) VALUES (?, ?);", to_db)


# def select_all_lines(conn):
#     """
#     Query all rows in the tasks table
#     :param conn: the Connection object
#     :return:
#     """
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM ayasdi_table")

#     rows = cur.fetchall()

#     for row in rows:
#         print(row)


# def main():
#     """
#         connect with SQLite
#     """

#     database = "./ayasdi_assignment.db"
#     # create a database connection
#     conn = create_connection(database)
#     with conn:
#         print "run all columns:"
#         # select_all_lines(conn)
#         run_all()
#         add_all_lines(conn)
#         conn.commit()

#     conn.close()


# if __name__ == '__main__':
#     main()
