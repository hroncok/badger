import json
import sys

from pymining import itemmining, assocrules


def load_json(filename, user_limit=0, badge_limit=0):
    """
    Loads data form JSON
    """
    with open(filename) as f:
        data = json.loads(f.read())
    if user_limit:
        data['transactions'] = data['transactions'][:user_limit]
    if badge_limit:
        data['badges'] = data['badges'][:badge_limit]
        data['transactions'] = [[b for b in t if b < badge_limit] for t in data['transactions']]
    return data


def association_rules(data, min_support, min_confidence):
    """
    Generates association rules from crawled data
    """
    badges = data['badges']
    transactions = data['transactions']

    # pymining only works, if the identifiers are one character strings :(
    transactions = tuple(tuple(chr(b) for b in t) for t in transactions)

    # pymining dance
    relim_input = itemmining.get_relim_input(transactions)
    item_sets = itemmining.relim(relim_input, min_support=min_support)
    rules = assocrules.mine_assoc_rules(item_sets, min_support=min_support,
                                        min_confidence=min_confidence)

    # translate identifiers back to badge names
    rules = [[frozenset(badges[ord(b)] for b in r[0]),
              frozenset(badges[ord(b)] for b in r[1]),
              r[2], r[3]] for r in rules]
    return rules


def print_rules(rules):
    """
    Prints the rules in human readable form
    """
    template = '{0} -> {1} with support {2} and confidence {3}'
    for rule in rules:
        print(template.format(', '.join(rule[0]),
                              ', '.join(rule[1]),
                              rule[2], rule[3]))


def parse(text, name, parser):
    """
    Returns parsed thing form text or exits with explanation
    """
    try:
        return parser(text)
    except ValueError:
        sys.stderr.write('{0} has to be {1}\n'.format(name, parser.__name__))
        exit(1)


if __name__ == '__main__':
    if len(sys.argv) not in [3, 5]:
        sys.stderr.write(
            'Usage: miner <min_support> <min_confidence> [<user_limit> <badge_limit>]\n')
        exit(1)

    s = parse(sys.argv[1], 'min_support', int)
    c = parse(sys.argv[2], 'min_confidence', float)
    if len(sys.argv) == 5:
        u = parse(sys.argv[3], 'user_limit', int)
        b = parse(sys.argv[4], 'badge_limit', int)
    print_rules(association_rules(load_json('data.json', u, b), min_support=s, min_confidence=c))
