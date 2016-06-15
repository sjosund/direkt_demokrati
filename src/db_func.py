"""
Set of functions to read and write data to DD Database
"""

import pymysql as sql
import time


def connect_to_db(host='localhost', user='root', password='', database='direct_democracy'):
    """
    Initializes a connection to the database to be used by the other methods.
    :param host: host machine of the database
    :param user: database user
    :param password: password for the chosen user
    :param database: database to connect to.
    :return: True if the connection was successful. False otherwise
    """

    #TODO: Add parameter for database port? /Alex 160605

    try:
        c = sql.connect(host, user, password, database)
    except:
        return False
    else:
        return c


def add_proposition(prop_data):
    """
    Inserts a new proposition into the database
    :param prop_data: Metadata for the proposition.
                      Should have the following format:
                        {title: Proposition title,
                         url: URL to proposition PDF,
                         date: Proposition publish date}

    :return: True if update was successful, False otherwise.
    """
    con = connect_to_db()

    if con:
        title = prop_data['title']
        url = prop_data['url']
        pub_date = prop_data['date']
        curr_time = int(time.time())
        with con:
            cursor = con.cursor()
            stmt = "INSERT INTO propositions(updated, upvotes, downvotes,title,url,pub_date) VALUES(%s,%s,%s,%s,%s,%s)"
            try:
                cursor.execute(stmt, (curr_time, 0, 0, title, url, pub_date))
                con.commit()
            except:
                con.rollback()
                return False
            else:
                return True
    return False


def get_proposition():
    return False


def vote_for_prop():
    return False


def has_voted(user_id, propostion_id):
    return False