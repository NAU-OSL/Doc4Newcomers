#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ =  'Felipe Fronchetti'
__contact__ = 'fronchetti@usp.br'

import os
import json
import github_api_scraper.scraper as scraper
import github_api_scraper.repository as project_api

# Variables used to build the /data/raw_files/documentation path
root_dir = os.path.dirname(os.path.dirname(os.getcwd()))
raw_files_dir = os.path.join(root_dir, 'data', 'raw_files', 'documentation')

class DocumentationScraper:
    def __init__(self, project_owner, project_name, collector):
        """Receives project's information and decides if its files should be extracted or not.

        Args:
            project_owner: A string that contains the name of the project owner on GitHub.
            project_name: A string that contains the name of the project on GitHub.
            collector: An object used to scrap data from GitHub's repositories.

        Note:
            On GitHub, a project has always an owner (that might be an user or an organization) and a name.
            For example, `github.com/torvalds/linux` is the address of the `linux` project on GitHub,
            that is owned by the user `torvalds`.
        """
        self.project_owner, self.project_name, self.project_collector = project_owner, project_name, project_collector
        self.project_folder = os.path.join(raw_files_dir, self.project_owner + '#' + self.project_name)
        excluded_projects = {}

        if os.path.isfile(os.path.join(raw_files_dir, 'excluded_projects.json')):
            with open(os.path.join(raw_files_dir, 'excluded_projects.json'), 'r') as excluded_file:
                excluded_projects = json.load(excluded_file)

        if excluded_projects:
            for reason_for_exclusion in excluded_projects:
                if self.project_name in excluded_projects[reason_for_exclusion]:
                    return

        self.__download_files()

    def __download_files(self):
        """Downloads the README and CONTRIBUTING files of a project using GitHbu API.

        In this method, the documentation files of a project are downloaded if: i. Both
        README and CONTRIBUTING files are available, ii. The documentation files are written
        in Markdown, iii. The number of lines per documentation file is greater than five (not empty).
        Porjects that meet these criteria are saved at the `data/raw_files/documentation` folder.
        Projects that do not meet these criteria are ignored and their names are saved into an exclusion file.
        """
        readme, readme_filename = project_collector.readme()
        contributing, contributing_filename = project_collector.contributing()

        if readme and contributing:
            if (str.lower(readme_filename)).endswith('.md') and (str.lower(contributing_filename)).endswith('.md'):
                if len(readme.splitlines()) > 5 and len(contributing.splitlines()) > 5:
                    if not os.path.isdir(self.project_folder):
                        os.makedirs(self.project_folder)

                    with open(os.path.join(self.project_folder, readme_filename), 'wb') as output_file:
                        output_file.write(str.encode(readme, encoding='utf-8'))

                    with open(os.path.join(self.project_folder, contributing_filename), 'wb') as output_file:
                        output_file.write(str.encode(contributing, encoding='utf-8'))
                else:
                    self.__exclude_project("Insufficient lines")
            else:
                self.__exclude_project("Different file extension")
        else:
            self.__exclude_project("Missing files")

    def __exclude_project(self, reason_for_exclusion):
        """Saves excluded projects into a JSON file that includes the reason for each exclusion.

        Args:
            reason_for_exclusion: A string containing the reason why a project was excluded from the downloads list.
        """

        excluded_projects = {}

        if os.path.isfile(os.path.join(raw_files_dir, 'excluded_projects.json')):
            with open(os.path.join(raw_files_dir, 'excluded_projects.json'), 'r') as excluded_file:
                excluded_projects = json.load(excluded_file)

        if reason_for_exclusion in excluded_projects:
            excluded_projects[reason_for_exclusion].append(self.project_owner + '/' + self.project_name)
        else:
            excluded_projects[reason_for_exclusion] = [self.project_owner + '/' + self.project_name]

        with open(os.path.join(raw_files_dir, 'excluded_projects.json'), 'w') as excluded_file:
            json.dump(excluded_projects, excluded_file, indent=4)

if __name__ == '__main__':
    api_client_id = '4161a8257efaea420c94'
    api_client_secret = 'd814ec48927a6bd62c55c058cd028a949e5362d4'
    api_scraper = scraper.Create(api_client_id, api_client_secret)

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
            ('mozilla', 'pdf.js'), ('rg3', 'youtube-dl'), ('mrdoob', 'three.js'), ('springprojects', 'spring-framework'), ('yiisoft', 'yii2')],
        4: [('boto', 'boto'), ('BVLC', 'caffe'), ('codemirror', 'CodeMirror'), ('gradle', 'gradle'), ('ipython', 'ipython'), ('jekyll', 'jekyll'), ('jquery', 'jquery')],
        5: [('iojs', 'io.js'), ('meteor', 'meteor'), ('ruby', 'ruby'), ('WordPress', 'WordPress')],
        6: [('chef', 'chef'), ('cocos2d', 'cocos2d-x'), ('diaspora', 'diaspora'), ('emberjs', 'ember.js'), ('resque', 'resque'), ('Shopify', 'active_merchant'), ('spotify', 'luigi'), ('TryGhost', 'Ghost')],
        7: [('django', 'django'), ('joomla', 'joomla-cms'), ('scikit-learn', 'scikit-learn')],
        9: [('JetBrains', 'intellij-community'), ('puppetlabs', 'puppet'), ('rails', 'rails')],
        11: [('saltstack', 'salt'), ('Seldaek', 'monolog'), ('v8', 'v8')],
        12: [('git', 'git'), ('webscalesql', 'webscalesql-5.6')],
        13: [('fog', 'fog')],
        14: [('odoo', 'odoo')]
    }

    if not os.path.isdir(raw_files_dir):
        os.makedirs(raw_files_dir)

    for truck_factor in projects:
        for project in projects[truck_factor]:
            project_name = project[1]
            project_owner = project[0]
            project_collector = project_api.Collector(project_owner, project_name, api_scraper)
            creator = DocumentationScraper(project_owner, project_name, project_collector)