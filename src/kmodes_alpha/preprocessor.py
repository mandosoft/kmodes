from kmodes_alpha_h import csv_dict
import csv
import pandas as pd

dict_data = csv_dict
csv_file = 'tree_viz/tree_input.csv'

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Cluster', 'Iteration', 'SR Mode'])
        for k, v in dict_data.items():
            lt = list(k)
            lt.append(v)
            writer.writerow(lt)

    df = pd.read_csv(csv_file)
    df['SR Mode'] = df['SR Mode'].round(3)
    df.drop_duplicates(subset='Cluster', inplace=True, keep='last')
    df = df.sort_values(by='SR Mode', ascending=False)
    df.to_csv('outfiles/output.csv', index=False)

except IOError:
    print("I/O error")