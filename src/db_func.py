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


def get_propositions(sql_stmt):
    """
        Fetches propositions from the database according to parameters in sql_stmt
        :param sql_stmt: Dict defining the query to run:
                         {stmt: SQL STATEMENT
                          params: tuple containing statement parameters

        :return: A dict of propositions in the following format:
                 propositions = {prop_id: Internal database row ID
                                 updated: Unix timestamp from last database update
                                 up_votes: Number of approving votes (YES Votes)
                                 down_votes: Number of disapproving votes (NO Votes)
                                 title: Proposition Title
                                 url: Proposition URL at riksdagen.se
                                 pub_date: Date of publication (at riksdagen.se)
        """
    con = connect_to_db()
    if con:
        with con:
            cursor = con.cursor()
            try:
                cursor.execute(sql_stmt['stmt'], sql_stmt['params'])
            except:
                return False
            else:
                rows = cursor.fetchall()
                propositions = []
                for row in rows:
                    propositions.append({'prop_id': row[0],
                                         'updated': row[1],
                                         'up_votes': row[2],
                                         'down_votes': row[3],
                                         'title': row[4],
                                         'url': row[5],
                                         'pub_date': row[6]})
                return propositions
    return False


def get_proposition_all(limit=100, order_by='id'):
    """
    Fetches propositions from the database.
    :param limit: Maximum number of propositions to return.
    :param order_by: Column to order results by. List if ordered by mySQL before LIMIT is used, so the order
                     might affect the results returned.
    :return: A dict of propositions in the following format:
             propositions = {prop_id: Internal database row ID
                             updated: Unix timestamp from last database update
                             up_votes: Number of approving votes (YES Votes)
                             down_votes: Number of disapproving votes (NO Votes)
                             title: Proposition Title
                             url: Proposition URL at riksdagen.se
                             pub_date: Date of publication (at riksdagen.se)
    """

    stmt = "SELECT * FROM propositions ORDER BY %s LIMIT %s"
    params = (order_by, limit)

    ret_data = get_propositions({'stmt': stmt, 'params': params})
    print(ret_data)
    if not ret_data:
        return False
    else:
        return ret_data


def get_proposition_by_criteria(criteria):

    return False


def get_proposition_by_date(start,stop):
    return False


def vote_for_prop():
    #Register vote in vote table.

    #Increment vote in proposition
    return False


def has_voted(user_id, propostion_id):
    return False