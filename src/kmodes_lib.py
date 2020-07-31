#!/bin/env python3

import sys
import warnings
import random
import gc
import csv
import os
import pandas as pd
from itertools import combinations
from sklearn.metrics.cluster import normalized_mutual_info_score as nmis
warnings.simplefilter(action='ignore', category=FutureWarning)


class KmodesAlpha:

    if not os.path.exists('data'):
        os.makedirs('data')

    def __init__(self):
        # self.notify = None
        self.csv_dict = dict()

    def map_clusters(self, cluster_list, k):
        cluster_list = [self.calculate_sr_mode(cluster, self.csv_dict, k) for cluster in cluster_list]
        return cluster_list

    def kmodes(self, cluster_list, k) -> dict:

        """Begin by selecting a random mode from list"""
        enumerated_list = list(enumerate(cluster_list))
        random_df_il, random_df = random.choice(enumerated_list)
        new_mode = random_df[random_df.columns[0]]

        """Add random mode to best cluster"""

        max_rii = 0
        for location, cluster in enumerated_list:
            cluster_mode = cluster[cluster.columns[0]]
            if location != random_df_il:
                rii = nmis(new_mode, cluster_mode, average_method='geometric')
                if rii > max_rii:
                    max_rii, best_cluster = rii, location
        cluster_list[random_df_il] = cluster_list[random_df_il].drop(cluster_list[random_df_il].columns[0], axis=1)
        cluster_list[best_cluster] = pd.concat([cluster_list[best_cluster], new_mode], axis=1)

        """Calculate the new mode and sr_mode for the best cluster"""
        cluster_list[best_cluster] = self.calculate_new_mode(cluster_list[best_cluster])
        cluster_list[best_cluster] = self.calculate_sr_mode(cluster_list[best_cluster], self.csv_dict, k)

        """Go back to the cluster the random mode came from and auction off remaining attributes"""
        if cluster_list[random_df_il].empty:
            del cluster_list[random_df_il]
            gc.collect()

        elif not cluster_list[random_df_il].empty:
            for i in cluster_list[random_df_il]:
                max_rii = 0
                remaining_attr = cluster_list[random_df_il][i]
                for location, cluster in enumerated_list:
                    cluster_mode = cluster[cluster.columns[0]]
                    if location != random_df_il:
                        rii = nmis(remaining_attr, cluster_mode, average_method='geometric')
                        if rii > max_rii:
                            max_rii, attr_winner = rii, location
                # noinspection PyUnboundLocalVariable
                cluster_list[attr_winner] = pd.concat([cluster_list[attr_winner], remaining_attr], axis=1)
                cluster_list[attr_winner] = self.calculate_new_mode(cluster_list[attr_winner])
                cluster_list[attr_winner] = self.calculate_sr_mode(cluster_list[attr_winner], self.csv_dict, k)
            del cluster_list[random_df_il]

        else:
            sys.stderr.write('\nThere was a problem breaking up a cluster.')

        return self.csv_dict

    @staticmethod
    def calculate_sr_mode(c: pd.DataFrame, csv_dict, k) -> pd.DataFrame:

        n_mis = nmis
        cc = len(list(combinations(c.columns, 2)))

        if len(c.columns) < 2:
            return c
        elif len(c.columns) == 2:
            max_sum = n_mis(c[c.columns[0]], c[c.columns[1]], average_method='geometric')
        else:
            max_sum = max([sum([n_mis(c[i], c[j], average_method='geometric')
                                for j in c if c[i].name != c[j].name]) for i in c])

        sr_mode = max_sum / cc
        csv_dict[tuple([tuple(sorted(c)), 'k = ' + str(k)])] = round(sr_mode, 3)

        return c

    @staticmethod
    def calculate_new_mode(c: pd.DataFrame) -> pd.DataFrame:
        n_mis = nmis
        max_sum = 0
        cluster_mode = pd.Series(dtype=object)
        for location, i in enumerate(c):
            sum_rii = 0
            for j in c:
                if c[i].name != c[j].name:
                    sum_rii += n_mis(c[i], c[j], average_method='geometric')
            if sum_rii > max_sum:
                max_sum, cluster_mode, ix = sum_rii, c[i], location

        if cluster_mode.empty:
            del cluster_mode
        else:
            c = c.drop(c.columns[ix], axis=1)
            c = pd.concat([c, cluster_mode], axis=1)
            cols = c.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            c = c[cols]

        return c

    @staticmethod
    def format_table_output(csv):
        df = pd.read_csv(csv)
        df['SR Mode'] = df['SR Mode'].round(3)
        df.drop_duplicates(subset='Cluster', inplace=True, keep='last')
        df = df.sort_values(by='SR Mode', ascending=False)

        # ask what to save file as
        return df.to_csv('data/output.csv', index=False)

    def export_to_tree(self):
        csv_file = 'data/tree_input.csv'
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Cluster', 'Iteration', 'SR Mode'])
                for k, v in self.csv_dict.items():
                    lt = list(k)
                    lt.append(v)
                    writer.writerow(lt)

            self.format_table_output(csv_file)

        except IOError:
            print("I/O error in preprocessor")


