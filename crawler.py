import json
import operator
import requests
import time


LIMIT = 20000
BADGELIMIT = 400

USERS = 'https://badges.fedoraproject.org/leaderboard/json?limit={limit}'.format(limit=LIMIT)
USER = 'https://badges.fedoraproject.org/user/{user}/json'


def data(url, count=1):
    """
    For given URL, returns dictionary with data parsed from JSON
    """
    req = requests.get(url)
    if req.status_code != 200:
        if count < 10:
            time.sleep(5)
            return data(url, count=count+1)
        raise Exception('Weird status code {code} at {url}'.format(code=req.status_code, url=url))
    return json.loads(req.text)


def users():
    """
    Returns list of user dicts
    """
    return data(USERS)['leaderboard']


def user_detail(user):
    """
    Returns dict with user's detail (including badges list)
    """
    print(user['nickname'])
    return data(USER.format(user=user['nickname']))


def badges_ids(detail):
    """
    Returns badges' ids list from user detail
    """
    return [badge['id'] for badge in detail['assertions']]


def transactions():
    """
    Returns dictionary with list of badges and anonymized users with list of their badges
    """
    badges = {}
    transactions = []
    nextid = 0
    for user in users():
        transaction = []
        for badge in badges_ids(user_detail(user)):
            if badge not in badges:
                badges[badge] = nextid
                nextid += 1
            if badges[badge] < BADGELIMIT:
                transaction.append(badges[badge])
        if transaction:
            transactions.append(transaction)
    badges = [kv[0] for kv in sorted(badges.items(), key=operator.itemgetter(1))]
    return {'badges': badges, 'transactions': transactions}


def save_json(filename, what):
    """
    Saves a dictionary to a file for a later use (as JSON)
    """
    with open(filename, 'w') as f:
        f.write(json.dumps(what))


save_json('data.json', transactions())
