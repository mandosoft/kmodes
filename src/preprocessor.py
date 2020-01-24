from kmodes_alpha_h import csv_dict
import csv

dict_data = csv_dict
csv_file = 'output.csv'

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Cluster', 'Iteration', 'SR Mode'])
        for k, v in dict_data.items():
            lt = list(k)
            lt.append(v)
            writer.writerow(lt)
except IOError:
    print("I/O error")