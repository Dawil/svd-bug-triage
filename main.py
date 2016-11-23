import argparse
import csv
import numpy as np

def open_csv(filename, as_dict=True):
    contents = open(filename).read().strip().split("\n")
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
            assignee_keywords[bug['Assignee']] += map(
                lambda keyword: keyword.strip(),
                bug['Keywords'].split(',')
            )

    with open('assignee_keywords.csv', 'w+') as f:
        writer = csv.writer(f)
        for assignee, keywords in assignee_keywords.items():
            writer.writerow([assignee] + keywords)

def load_assignee_keywords():
    assignee_keywords = open_csv('assignee_keywords.csv', as_dict=False)
    ak_dict = {}
    unique_keywords = set()
    for row in assignee_keywords:
        ak_dict[row[0]] = {}
        for keyword in row[1:]:
            unique_keywords.add(keyword)
            ak_dict[row[0]][keyword] = ak_dict[row[0]].get(keyword, 0) + 1
    import pdb
    pdb.set_trace()
    keywords = sorted(list(unique_keywords))
    assignees = sorted(list(filter(
        lambda assignee: sum(ak_dict[assignee].values()) > 5,
        ak_dict.keys()
    )))

    matrix = [
        [
            ak_dict[assignee].get(keyword, 0)
            for keyword in keywords
        ]
        for assignee in assignees
    ]
    return (assignees, keywords, matrix)

def save_matrix():
    assignees, keywords, matrix, U, s, V = compute_svd()
    with open('matrix.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerows(matrix)
    with open('assignees.txt', 'w+') as f:
        f.write("\n".join(assignees))
    with open('keywords.txt', 'w+') as f:
        f.write("\n".join(keywords))
    with open('U.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerows(U)
    with open('V.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerows(V)
    with open('s.txt', 'w+') as f:
        f.write("\n".join(map(str, s)))

def compute_svd():
    assignees, keywords, matrix = load_assignee_keywords()
    U, s, V = np.linalg.svd(matrix)
    return (
        assignees, keywords, matrix,
        U, s, V
    )

def interactive():
    assignees, keywords, matrix, U, s, V = compute_svd()
    import pdb
    pdb.set_trace()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    args = parser.parse_args()
    locals()[args.command]()
