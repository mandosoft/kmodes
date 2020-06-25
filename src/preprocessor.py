import csv
import pandas as pd
from src.gui import tree_path


def process_tree_file(csv):

    df = pd.read_csv(csv)
    df['SR Mode'] = df['SR Mode'].round(3)
    df.drop_duplicates(subset='Cluster', inplace=True, keep='last')
    df = df.sort_values(by='SR Mode', ascending=False)

    return df.to_csv('output.csv', index=False)


if tree_path is None:

    from src.kmodes_alpha_h import csv_dict
    dict_data = csv_dict
    csv_file = 'tree_input.csv'

    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Cluster', 'Iteration', 'SR Mode'])
            for k, v in dict_data.items():
                lt = list(k)
                lt.append(v)
                writer.writerow(lt)

        process_tree_file(csv_file)

    except IOError:
        print("I/O error in preprocessor")
