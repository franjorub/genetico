import csv


def delete_linebreak(s):
    if '\n' in s:
        return s[:len(s) - 1]
    else:
        return s


def generate_csv(results):
    f = open('genetic_algorithm_results.csv', 'w')

    writer = csv.writer(f)

    writer.writerows(results)

    f.close()
