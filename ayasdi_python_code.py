""" Generates ayasdi_assignment.csv and ayasdi_assignment.db """
import random
import math
import datetime
import csv
import sqlite3
from sqlite3 import Error

def generate_header(start, end, attachment):
    """
        header generator
    """

    result = []

    for i in range(start, end + 1):
        result.append("col" + str(i) + str(attachment))

    return result


def generate_column(values, previous_table):
    """Generate a column with given values"""

    result = []

    for i in range(0, len(previous_table)):
        current_item = previous_table[i] + values[i]
        result.append(current_item)

    return result


# Generating CSV file
def generate_1st_column(rows):
    """
        labeled as col1
        the index column where the values are 1 to 1 million
        (1 million rows with 1 header)
    """

    values = [i for i in range(1, rows+1)]
    result = []
    result.append(['col1'])

    for i in range(0, len(values)):
        result.append([values[i]])

    return result


def get_random_num_given_per_null(max_number, percentage):
    """
        add 10% up of the number existing
        if the number is over index, generate null
    """

    tenup = int(math.floor(max_number * (1 + percentage)))
    random_num = random.randint(0, tenup)

    if random_num > max_number:
        return None

    return random_num


def get_gauss_num_10per_null(input_mean, input_std):
    """
        get a number within normal distribution with 10percent null
    """

    if get_random_num_given_per_null(1, 0.1) != None:
        gauss_num = random.normalvariate(input_mean, input_std)
    else:
        gauss_num = None

    return gauss_num


def generate_2nd_10th_column(rows):
    """
        The next 9 columns (2 to 10) contain randomly distributed gaussian data
        and are labelled col2_x ... col10_x where 'x' is the mean of the gaussian distribution.
        For example, if you chose means of 10, 20, 30, 40, 50, 60, 70, 80 for col2 through col10,
        the labels are col2_10, col3_20, col4_30 and etc.
        You can choose whatever mean and variance you would like for each column.
    """

    start_col = 2
    end_col = 10
    range_for_col = end_col - start_col
    result = []

    for i in range(1, range_for_col + 1):
        input_mean = i * 10
        std = 1
        column_to_attach = [["col" + str(i) + "_" + str(input_mean)]]

        # paste a column to the previous column
        while len(column_to_attach) < rows + 1:
            item = []
            to_append = "{0:.2f}".format(get_gauss_num_10per_null(input_mean, std))
            item.append(to_append)
            column_to_attach.append(item)

        if result:
            result = generate_column(column_to_attach, result)
        else:
            result = column_to_attach

    return result


def get_random_word_10per_null():
    """
        returns word with 10% possiblity of returning null
    """

    # word_dic = open('wordlist.txt', 'w')
    word_dic = file('wordlist.txt').read().split()
    word_dic_length = len(word_dic)
    random_word_location = get_random_num_given_per_null(word_dic_length, 0.1)

    if random_word_location:
        return word_dic[random_word_location]

    return None


def append_data(start_col, end_col, rows, func_for_content):
    """
        append given data for the fows and columns given
    """

    result = [generate_header(start_col, end_col, "")]

    while len(result) < rows + 1:
        item = []
        while len(item) < end_col - start_col + 1:
            to_append = func_for_content()
            item.append(to_append)
        result.append(item)

    return result


# English word list downloaded from the following link
# http://www-01.sil.org/linguistics/wordlists/english/
def generate_11th_19th_column(rows):
    """
        Columns 11 to 19 are labelled as col11...col19,
        where each column has random strings selected from the English Dictionary.
        10% randomly distributed nulls in this column as well.
    """

    start_col = 11
    end_col = 19
    return append_data(start_col, end_col, rows, get_random_word_10per_null)


def get_random_date():
    """
        generates random date
    """

    start_date = "01/01/2014"
    date_1 = datetime.datetime.strptime(start_date, "%m/%d/%Y")
    random_number = get_random_num_given_per_null(365, 0)
    return str((date_1 + datetime.timedelta(days=random_number)).strftime("%B %d, %Y"))


def generate_20th_column(rows):
    """
        Column 20 has random dates selected between January 1, 2014 to December 31, 2014.
        No nulls in this column.
    """

    # 0 - 364 (range to 365) are the random numbers to generate
    return append_data(20, 20, rows, get_random_date)


def run_all():
    """
    run all functions that generates the table
    """

    rows = 100
    result = generate_1st_column(rows)
    second_10th = generate_2nd_10th_column(rows)
    result = generate_column(second_10th, result)
    eleventh_19th = generate_11th_19th_column(rows)
    result = generate_column(eleventh_19th, result)
    twentiesth = generate_20th_column(rows)
    result = generate_column(twentiesth, result)


    return result


########################### generate csv
def generate_csv_table(table_values):
    """generate csv table with given array"""

    with open('ayasdi_assignment.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerows(table_values)


# ########################### Loading the CSV table to sqlite
def create_connection(db_file):
    """
        create a database connection to the SQLite database
        specified by the db_file
        :param db_file: database file
        :return: Connection object or None
    """

    try:
        # con = sqlite3.connect(":memory:")
        conn = sqlite3.connect(db_file)
        return conn
    except Error as error:
        print error

    return None


def add_all_lines(conn, table_values):
    """
        add all lines in CSV to the SQLite database.
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
    """

    column_list = table_values[0]
    column_row = filter(lambda x: x != "'", str(column_list)[1: -1])
    qmark = "?"
    col_count = len(column_list)
    for cols in range(1, col_count):
        qmark += ", ?"
        cols = cols

    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS ayasdi_table;")
    cur.execute("CREATE TABLE ayasdi_table (" + column_row + ");")

    with open('ayasdi_assignment.csv', 'rb') as fin:
        # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr_name = csv.DictReader(fin) # comma is default delimiter

        to_db = [(i['col1'], i['col1_10'], i['col2_20'], i['col3_30'], i['col4_40'], i['col5_50'], \
        i['col6_60'], i['col7_70'], i['col8_80'], i['col11'], i['col12'], i['col13'], i['col14'], \
        i['col15'], i['col16'], i['col17'], i['col18'], i['col19'], i['col20']) for i in dr_name]

    cur.executemany("INSERT INTO ayasdi_table (" + column_row + ") VALUES (" + qmark + ");", to_db)


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
#         print row


def main():
    """
        connect with SQLite
    """

    table_values = run_all()
    generate_csv_table(table_values)

    database = "./ayasdi_assignment.db"
    # create a database connection
    conn = create_connection(database)
    with conn:
        print "run all columns:"
        # select_all_lines(conn)
        run_all()
        print "ran all"
        add_all_lines(conn, table_values)
        print "add all lines"
        conn.commit()
        print "committed"

    conn.close()
    print "connection closed"


if __name__ == '__main__':
    main()
