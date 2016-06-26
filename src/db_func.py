"""
Set of functions to read and write data to DD Database
"""

from datetime import datetime
import time

import pymysql as sql


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
                                         'pub_date': datetime.utcfromtimestamp(int(row[6])).date()})
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
    if not ret_data:
        return False
    else:
        return ret_data


def get_proposition_by_criteria(criteria={}):
    """
    Fetches propositions from the database according to set criteria. Criteria can be set in almost any way but
    with one limitation: all columns in the propositions table has to be returned (this is to keep dependent code
    as simple as possible). The criteria are set using a dict where one specifies how to filter. There is no need
    to set any criteria. If none are set, all propositions will be returned.
    :param criteria: a dict that contains the criteria to format on. There is no need to specify all of the columns.
                     Format:
                     criteria = {where_col: column specified for a WHERE clause,
                                 where_clause: <, >, >=, <=, =, <> [NOTE: IN and LIKE are NOT supported]
                                 where_val: Value to filter column on, if keyword BETWEEN was used in where clause
                                            then where val should be a list with two values
                                 order_by: Column to order by,
                                 order_dir: ASC or DESC (ascending or descending)
                                 limit: Number of results to return

    :return: A dict of propositions in the following format:
             propositions = {prop_id: Internal database row ID
                             updated: Unix timestamp from last database update
                             up_votes: Number of approving votes (YES Votes)
                             down_votes: Number of disapproving votes (NO Votes)
                             title: Proposition Title
                             url: Proposition URL at riksdagen.se
                             pub_date: Date of publication (at riksdagen.se)
    """

    params = []

    if 'where_col' and 'where_clause' and 'where_val' in criteria:
        where_str = 'WHERE ' + criteria['where_col'] + ' ' + criteria['where_clause']

        if criteria['where_clause'] == 'BETWEEN':
            where_str += ' %s AND %s'
            params.append(criteria['where_val'][0])
            params.append(criteria['where_val'][1])
        else:
            where_str += ' %s'
            params.append(criteria['where_val'])
    else:
        where_str = ''

    if 'order_by' and 'order_dir' in criteria:
        order_str = 'ORDER BY %s ' + criteria['order_dir']
        params.append(criteria['order_by'])
    else:
        order_str = ''

    if 'limit' in criteria:
        limit_str = 'LIMIT %s'
        params.append(criteria['limit'])
    else:
        limit_str = ''

    stmt = 'SELECT * FROM propositions ' + where_str + ' ' + order_str + ' ' + limit_str

    ret_data = get_propositions({'stmt': stmt, 'params': tuple(params)})

    if not ret_data:
        return False
    else:
        return ret_data


def get_proposition_by_date(start,stop):
    return False


def vote_for_prop(user_id, prop_id, vote):
    """
    Used when a user votes for a proposition. Updates two tables: Adds or modifies a row in table ´votes´ (registers
    a vote) and adds

    :param user_id:
    :param prop_id:
    :param vote:
    :return:
    """

    # TODO: Handle cases for when user has voted. Now it will only return false.

    con = connect_to_db()

    if con:
        with con:
            cursor = con.cursor()
            curr_time = int(time.time())

            vote_stmt = "INSERT INTO votes (proposition_id, user_id, vote, timestamp) VALUES (%s, %s, %s, %s)"

            if vote == 1:
                inc_stmt = "UPDATE propositions SET upvotes = upvotes + 1 WHERE id = %s"
            elif vote == -1:
                inc_stmt = "UPDATE propositions SET downvotes = downvotes + 1 WHERE id = %s"

            try:
                cursor.execute(vote_stmt, (prop_id, user_id, vote, curr_time))
                cursor.execute(inc_stmt,(prop_id))
            except:
                con.rollback()
                return False
            else:
                con.commit()
                return True






def has_voted():
    return False