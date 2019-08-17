#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Felipe Fronchetti'
__contact__ = 'fronchetti@usp.br'

import os
import csv
import json

# TO-DO: Evaluate classifiers performance


def group_performances(results_dir):
    models_folder = os.path.join(results_dir, 'models')
    output_file = os.path.join(results_dir, 'csv', 'performances.csv')

    with open(output_file, 'w') as csv_file:
        fieldnames = ['class', 'f1-score', 'precision', 'recall', 'support']
        writer = csv.DictWriter(csv_file, fieldnames)

        for root, _, files in os.walk(models_folder):
            for filename in files:
                if filename.endswith('.report.json'):
                    filepath = os.path.join(root, filename)
                    with open(filepath, 'r') as json_file:
                        data = json.load(json_file)
                        writer.writerow(
                            {'class': '%s (%s)' % (data['classifier_name'], data['strategy'])})
                        writer.writeheader()

                        for key in data:
                            if isinstance(data[key], dict):
                                row = data[key]
                                row['class'] = key
                                writer.writerow(row)
                        writer.writerow({})


if __name__ == '__main__':
    repository_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    results_dir = os.path.join(repository_dir, 'results')
    group_performances(results_dir)
