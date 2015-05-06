import json

from pymining import itemmining, assocrules


def load_json(filename):
    """
    Loads data form JSON
    """
    with open(filename) as f:
        data = json.loads(f.read())
    return data


def association_rules(data):
    """
    Generates association rules from crawled data
    """
    badges = data['badges']
    transactions = data['transactions']

    # pymining only works, if the identifiers are one character strings :(
    transactions = tuple(tuple(chr(b) for b in t) for t in transactions)

    # pymining dance
    relim_input = itemmining.get_relim_input(transactions)
    item_sets = itemmining.relim(relim_input, min_support=7)
    rules = assocrules.mine_assoc_rules(item_sets, min_support=7, min_confidence=0.8)

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

print_rules(association_rules(load_json('data.json')))
