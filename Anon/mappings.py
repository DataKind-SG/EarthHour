import config
import csv
import Levenshtein as edit
import numpy as np


class Mappings:
    inexact = dict()
    inexact_final = dict()
    inexact_standard = dict()
    semiexact = dict()
    semiexact_final = dict()
    twitter_final = dict()

    def __init__(self):
        Mappings.c = config.Config()
        with open('stopwords.txt', 'r') as stop_reader:
            self.stopwords = file.read(stop_reader).splitlines()

        for header in self.c.inexact:
            Mappings.inexact[header] = dict()

        for header in self.c.semiexact:
            Mappings.semiexact[header] = dict()

    def __semi_standardize_string(self, entry):
        standardized = entry.lower()
        standardized = standardized.replace(' ', '')
        return standardized

    def __full_standardize_string(self, entry):
        standardized = self.__semi_standardize_string(entry)
        standardized = standardized.replace('.', '')
        standardized = standardized.replace(',', '')
        for stopword in self.stopwords:
            standardized = standardized.replace(stopword, '')
        return standardized

    def __add_semiexact_entry(self, header, entry):
        standarized = self.__semi_standardize_string(entry)
        if standarized not in Mappings.semiexact[header]:
            Mappings.semiexact[header][standarized] = set()
            Mappings.semiexact[header][standarized].add(entry)
        else:
            Mappings.semiexact[header][standarized].add(entry)

    def __get_max_jaro_winkler(self, standardized, header):
        max_jw = 0
        max_standard = ''
        for key in Mappings.inexact_standard[header]:
            jw = edit.jaro_winkler(key, standardized)
            if jw > max_jw:
                max_jw = jw
                max_standard = Mappings.inexact_standard[header][key]

        return max_jw, max_standard

    def __add_inexact_entry(self, header, entry):
        standardized = self.__full_standardize_string(entry)

        if standardized not in Mappings.inexact_standard[header]:
            max_jw, max_standard = self.__get_max_jaro_winkler(standardized, header)
            if max_jw < self.c.inexact[header][1]:
                Mappings.inexact_standard[header][standardized] = entry
                Mappings.inexact[header][entry] = set()
                Mappings.inexact[header][entry].add(entry)
            else:
                if max_standard not in Mappings.inexact[header]:
                    Mappings.inexact[header][max_standard] = set()

                Mappings.inexact[header][max_standard].add(entry)
        else:
            standard = Mappings.inexact_standard[header][standardized]
            if standard not in Mappings.inexact[header]:
                Mappings.inexact[header][standard] = set()

            Mappings.inexact[header][standard].add(entry)

    def populate_mappings(self, file_name):
        for header in Mappings.inexact:
            Mappings.inexact_standard[header] = dict()
            with open(Mappings.c.inexact[header][2], 'r') as standard_file:
                all_standard = file.read(standard_file).splitlines()
                for standard in all_standard:
                    Mappings.inexact_standard[header][self.__full_standardize_string(standard)] = standard

        with open(file_name, 'r') as csvfile:
            original_file_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in original_file_reader:
                for header in Mappings.semiexact:
                    if row[header] != None:
                        self.__add_semiexact_entry(header, row[header])

                for header in Mappings.inexact:
                    if row[header] != None:
                        self.__add_inexact_entry(header, row[header])

    def write_mappings(self):
        for header in Mappings.semiexact:
            field_names = "original,anonymized\n"
            random_permutation = np.random.permutation(range(100000, 999999))
            alphabetized = sorted(iter(Mappings.semiexact[header].keys()), key=str.lower)

            with open(self.c.semiexact[header], 'w') as mapping_writer:
                mapping_writer.write(field_names)
                count = 0
                for standarized in alphabetized:
                    for entry in Mappings.semiexact[header][standarized]:
                        mapping_writer.write(entry + "," + str(random_permutation[count]) + "\n")
                    count = count + 1

        for header in Mappings.inexact:
            field_names = "original,common,anonymized\n"
            random_permutation = np.random.permutation(range(100000, 999999))
            alphabetized = sorted(iter(Mappings.inexact[header].keys()), key=str.lower)

            with open('check_' + self.c.inexact[header][0], 'w') as mapping_writer:
                mapping_writer.write(field_names)
                count = 0
                for standard in alphabetized:
                    for entry in Mappings.inexact[header][standard]:
                        mapping_writer.write("\"%s\",\"%s\",%s\n" % (entry,  standard, str(random_permutation[count])))
                    count = count + 1

    def read_mappings(self):
        for header in Mappings.semiexact:
            Mappings.semiexact_final[header] = self.__read_mapping(self.c.semiexact[header])

        for header in Mappings.inexact:
            Mappings.inexact_final[header] = self.__read_mapping(self.c.inexact[header][0])

        # shouldn't be hard coded, but...
        #Mappings.twitter_final = self.__read_mapping('mapping_twitter_handle.csv')

    def __read_mapping(self, file_name):
        with open(file_name, 'r') as mapping_reader:
            # skip the header
            mapping_reader.readline()
            dict_lines = file.read(mapping_reader).splitlines()

        mapping = dict()
        for line in dict_lines:
            tokens = line.split(',')
            mapping[tokens[0]] = tokens[1]

        return mapping


def main():
    # file name should be an argument...
    file_names = ["data/earthhour_campaign_report_unsubscribe_lists.csv", "data/earthhour_campaign_report_unopen_lists.csv", "data/earthhour_campaign_report_open_lists.csv", "data/earthhour_campaign_report_link_lists.csv"]

    m = Mappings()
    for file_name in file_names:
        m.populate_mappings(file_name)
        print file_name
    m.write_mappings()

if __name__ == '__main__':
    main()
