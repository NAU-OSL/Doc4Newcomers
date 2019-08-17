#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ =  'Felipe Fronchetti'
__contact__ = 'fronchetti@usp.br'

import csv
import os 
import re
import statistics
import xlsxwriter
import random
import telescope.collector as GitHub
import telescope.search as GitHubSearch
import telescope.repository as GitHubRepository

raw_files_folder = '../raw_files'
spreadsheet_folder = '../spreadsheets'

class SpreadsheetCreator:
    def __init__(self, organization, name, repository):
        self.organization, self.name, self.repository = organization, name, repository
        self.folder = raw_files_folder + '/' + self.name + ' (' + self.organization + ')'
        self.readme = None
        self.contributing = None
        self.ignore = []

        if os.path.isfile(raw_files_folder + '/ignore.txt'):
            with open(raw_files_folder + '/ignore.txt', 'r') as file:
                self.ignore = file.read().splitlines()

        if self.name not in self.ignore:
            self.__download_files()

    def __download_files(self):
        self.readme, self.readme_filename = repository.readme()
        self.contributing, self.contributing_filename = repository.contributing()

        if self.readme and self.contributing:
            if not os.path.isdir(self.folder):
                os.makedirs(self.folder)

            with open(self.folder + '/' + self.readme_filename, 'wb') as file:
                file.write(str.encode(self.readme, encoding='utf-8'))

            with open(self.folder + '/' + self.contributing_filename, 'wb') as file:
                file.write(str.encode(self.contributing, encoding='utf-8'))
        else:
            with open(raw_files_folder + '/ignore.txt', 'a') as file:
                file.write(self.organization + '/' + self.name + '\n')

if __name__ == '__main__':
    api_client_id = str('4161a8257efaea420c94')
    api_client_secret = str('d814ec48927a6bd62c55c058cd028a949e5362d4')
    api_collector = GitHub.Collector(api_client_id, api_client_secret)
    projects = {
        1: [('alexreisner', 'geocoder'), ('atom', 'atom-shell'), ('bjorn', 'tiled'), ('bumptech', 'glide'), ('celery', 'celery'), ('celluloid', 'celluloid'),
            ('dropwizard', 'dropwizard'), ('dropwizard', 'metrics'), ('erikhuda', 'thor'), ('Eugeny', 'ajenti'), ('getsen-try', 'sentry'), ('github', 'android'),
            ('gruntjs', 'grunt'), ('janl', 'mustache.js'), ('jr-burke', 'requirejs'), ('justinfrench', 'formtastic'), ('kivy', 'kivy'), ('koush', 'ion'),
            ('kriswallsmith', 'assetic'), ('Leaflet', 'Leaflet'), ('less', 'less.js'), ('mailpile', 'Mailpile'), ('mbostock', 'd3'), ('mitchellh', 'vagrant'),
            ('mitsuhiko', 'flask'), ('mongoid', 'mongoid'), ('nate-parrott', 'Flashlight'), ('nicolasgramlich', 'AndEngine'), ('paulas-muth', 'fnordmetric'),
            ('phacility', 'phabricator'), ('powerline', 'powerline'), ('puphpet', 'puphpet'), ('ratchetphp', 'Ratchet'), ('ReactiveX', 'RxJava'),
            ('sandstorm-io', 'capnproto'), ('sass', 'sass'), ('sebastianbergmann', 'phpunit'), ('sferik', 'twitter'), ('silexphp', 'Silex'),
            ('sstephenson', 'sprockets'), ('substack', 'node-browserify'), ('thoughtbot', 'factory_girl'), ('thoughtbot', 'paperclip'), ('wp-cli', 'wp-cli')],
        2: [('activeadmin', 'activeadmin'), ('ajaxorg', 'ace'), ('ansible', 'ansible'), ('apache', 'cassandra'), ('bup', 'bup'), ('clojure', 'clojure'),
            ('composer', 'composer'), ('cucumber', 'cucumber'), ('driftyco', 'ionic'), ('drupal', 'drupal'), ('elas-ticsearch', 'elasticsearch'),
            ('elasticsearch', 'logstash'), ('ex-cilys', 'androidannotations'), ('facebook', 'osquery'), ('facebook', 'presto'), ('FriendsOfPHP', 'PHP-CS-Fixer'),
            ('github', 'linguist'), ('Itseez', 'opencv'), ('jadejs', 'jade'), ('jashkenas', 'backbone'), ('JohnLangford', 'vowpal_wabbit'), ('jquery', 'jquery-ui'),
            ('libgdx', 'libgdx'), ('meskyanichi', 'backup'), ('netty', 'netty'), ('omab', 'django-social-auth'), ('openframeworks', 'openFrameworks'),
            ('plataformatec', 'devise'), ('prawnpdf', 'prawn'), ('pydata', 'pandas'), ('Re-spect', 'Validation'), ('sampsyo', 'beets'), ('SFTtech', 'openage'),
            ('sparklemo-tion', 'nokogiri'), ('strongloop', 'express'), ('thinkaurelius', 'titan'), ('ThinkU-pLLC', 'ThinkUp'), ('thumbor', 'thumbor'),
            ('xetorthio', 'jedis')],
        3: [('bbatsov', 'rubocop'), ('bitcoin', 'bitcoin'), ('bundler', 'bundler'), ('divio', 'django-cms'), ('haml', 'haml'), ('jnicklas', 'capybara'),
            ('mozilla', 'pdf.js'), ('rg3', 'youtube-dl'), ('mrdoob', 'three.js'), ('springprojects', 'spring-framework'), ('yiisoft', 'yii2')]
    }

    if not os.path.isdir(raw_files_folder):
        os.mkdir(raw_files_folder)

    if not os.path.isdir(spreadsheet_folder):
        os.mkdir(spreadsheet_folder)

    for truck_factor in projects:
        for project in projects[truck_factor]:
            name = project[1]
            organization = project[0]
            repository = GitHubRepository.Repository(organization, name, api_collector)
            creator = SpreadsheetCreator(organization, name, repository)