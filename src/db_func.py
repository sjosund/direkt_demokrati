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

#TODO: Proposition vote functions work. But there is a bug: If a user updates a vote with the same value, the up/down-
#TODO: vote data will be corrupt. Entry in table 'votes' is ok, but the function always increments/decrements when a
#TODO: user votes. Example: if prop X has 5 upvotes and 3 downvotes and a user downvotes the prop will have 4u 4d. If
#TODO: the user now downvotes again the prop will have 3u 5d, then 2u 6d and so on. The sum upvote+downvote will always
#TODO: be correct (in ex 8 votes), but the difference upvote-|downvote| will be skewed. Can this be fixed with SQL???
#TODO: otherwise we need to implement function has_voted(user_id, prop_id), which will cost us some extra db-calls :/

def vote_for_prop(user_id, prop_id, vote):
    """
    Used to vote for propositions. Adds or modifies a row in table ´votes´ (registers
    a vote) and adds an upvote or a downvote for each proposition.

    :param user_id: Users uique id
    :param prop_id: Proposition unique id
    :param vote: Users vote. +1 for upvote, -1 for downvote
    :return: True if success, False otherwise
    """

    if vote not in {1, -1}:
        raise IncorrectVoteException('Incorrect vote value')

    retval = add_vote_for_prop(user_id, prop_id, vote)

    if retval == 1:
        return True
    elif retval == 2:
        # TODO: To fix bug mentioned above, find out how user has voted, only update if new vote differs.
        if update_vote_for_prop(user_id, prop_id, vote):
            return True
        else:
            return False
    else:
        return False


def add_vote_for_prop(user_id, prop_id, vote):
    """
    Used when a user votes for a proposition. Updates two tables: Adds or modifies a row in table ´votes´ (registers
    a vote) and adds an upvote or a downvote for each proposition.

    :param user_id: User who votes
    :param prop_id: Proposition to vote for
    :param vote: -1 for downvote, +1 for upvote
    :return: 1 if voting succeded, 2 if user has already voted, 0 if the connection failed.
    """

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
            except Exception as e:
                #TODO: Better practice might be: sql.err.IntegrityError as e??
                con.rollback()

                if e.args[0] == 1062:
                    print('Duplicate entry!')
                    return 2
                else:
                    print('Unknown Error')
                    return 0
            else:
                con.commit()
                return 1


def update_vote_for_prop(user_id, prop_id, vote):
    """
    Changes a users vote if they have already voted.

    :param user_id: Users unique id
    :param prop_id: proposition id
    :param vote: Vote, +1 for upvote, -1 for downvote
    :return: True if update succeded, False Otherwise
    """

    con = connect_to_db()

    if con:
        with con:
            cursor = con.cursor()
            curr_time = int(time.time())

            vote_stmt = "UPDATE votes SET vote = %s, timestamp = %s WHERE user_id = %s AND proposition_id = %s"

            if vote == 1:
                inc_stmt = "UPDATE " \
                            "propositions " \
                           "SET " \
                            "upvotes = upvotes + 1, downvotes = downvotes - 1 " \
                           "WHERE " \
                            "id = %s"
            elif vote == -1:
                inc_stmt = "UPDATE " \
                            "propositions " \
                           "SET " \
                            "downvotes = downvotes + 1, upvotes = upvotes - 1 " \
                           "WHERE " \
                            "id = %s"

            try:
                cursor.execute(vote_stmt, (vote, curr_time, user_id, prop_id))
                cursor.execute(inc_stmt, (prop_id))
            except:
                print('change fail')
                print(inc_stmt)
                con.rollback()
                return False
            else:
                con.commit()
                return True

def has_voted():
    return False

class IncorrectVoteException(Exception):
    def __init__(self, message):
        super(IncorrectVoteException, self).__init__(message)


