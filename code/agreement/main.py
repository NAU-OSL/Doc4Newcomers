import os
import pandas
import subprocess

if __name__ == '__main__':
    repository_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    results_dir = os.path.join(repository_dir, 'results')
    agreement_dir = os.path.join(results_dir, 'csv', 'agreement')
    if not os.path.isdir(agreement_dir):
        os.mkdir(agreement_dir)
    dataframe_path = os.path.join(results_dir, 'csv', 'raw_dataframe.csv')
    dataframe = pandas.read_csv(dataframe_path)
    categories = ['CF – Contribution flow',
               'CT – Choose a task',
               'FM – Find a mentor',
               'TC – Talk to the community',
               'BW – Build local workspace',
               'DC – Deal with the code',
               'SC – Submit the changes']

    for project in dataframe.groupby(['Filename']):
        filename = project[0]
        authors = project[1].Author.unique()
        if len(authors) == 2:
            author_index = 1
            project_dir = os.path.join(agreement_dir, filename.replace('.xlsx', ''))
            if not os.path.isdir(project_dir):
                os.mkdir(project_dir)
            for author in authors:
                with open(os.path.join(project_dir, 'author_' + str(author_index) + '.txt'), 'w') as csv_file:
                    csv_file.write("# Author: " + str(author) + " \n")
                    csv_file.write("# " + ', '.join(str(category)[:2] for category in categories) + '\n')
                    author_project_dataframe = dataframe.loc[(dataframe['Author'] == author) & (dataframe['Filename'] == filename)]
                    for index, row in author_project_dataframe.iterrows():
                        marked_categories = []
                        for category in categories:
                            if row[category] == 1:
                                marked_categories.append(category[:2])
                        if marked_categories:
                            csv_file.write(','.join(marked_categories))
                        else:
                            csv_file.write('NONE')
                        csv_file.write('\n')
                author_index += 1