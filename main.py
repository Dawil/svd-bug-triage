import argparse
import csv

def open_csv(filename, as_dict=True):
    contents = open(filename).read().split("\n")
    if as_dict:
        print('foo')
        reader = csv.DictReader(contents)
    else:
        print('bar')
        reader = csv.reader(contents)
    return list(reader)

def get_assignee_keywords():
    bugs = open_csv('data.csv')
    assignee_keywords = {}
    for bug in bugs:
        if bug['Keywords']:
            assignee_keywords[bug['Assignee']] = assignee_keywords.get(bug['Assignee'], [])
            assignee_keywords[bug['Assignee']].append(bug['Keywords'])

    with open('assignee_keywords.csv', 'w+') as f:
        writer = csv.writer(f)
        for assignee, keywords in assignee_keywords.items():
            writer.writerow([assignee] + keywords)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    args = parser.parse_args()
    locals()[args.command]()
