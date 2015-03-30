import config
import csv
import Levenshtein


class Mappings:
    inexact = dict()
    semiexact = dict()
    inexact_final = dict()
    semiexact_final = dict()
    twitter_final = dict()

    def __init__(self):
        Mappings.c = config.Config()

        with open('stopwords.csv', 'r') as stop_reader:
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

    def __get_max_levenshtein(self, standardized, header):
        max_levensthein = 0
        max_standardized = ''
        for key in Mappings.inexact[header]:
            for pair in Mappings.inexact[header][key]:
                levenshtein = Levenshtein.ratio(pair[1], standardized)
                if levenshtein > max_levensthein:
                    max_levensthein = levenshtein
                    max_standardized = key

        return max_levensthein, max_standardized

    def __add_semiexact_entry(self, header, entry):
        standarized = self.__semi_standardize_string(entry)
        if standarized not in Mappings.semiexact[header]:
            Mappings.semiexact[header][standarized] = set()
            Mappings.semiexact[header][standarized].add(entry)
        else:
            Mappings.semiexact[header][standarized].add(entry)

    def __add_inexact_entry(self, header, entry):
        standardized = self.__full_standardize_string(entry)
        if standardized not in Mappings.inexact[header]:
            levenshtein, close_standardized = self.__get_max_levenshtein(standardized, header)
            if levenshtein < self.c.inexact[header][1]:
                Mappings.inexact[header][standardized] = set()
                Mappings.inexact[header][standardized].add((entry, standardized))
            else:
                Mappings.inexact[header][close_standardized].add((entry, standardized))
        else:
            Mappings.inexact[header][standardized].add((entry, standardized))

    def populate_mappings(self, file_name):
        with open(file_name, 'r') as csvfile:
            original_file_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in original_file_reader:
                for header in Mappings.semiexact:
                    self.__add_semiexact_entry(header, row[header])

                for header in Mappings.inexact:
                    self.__add_inexact_entry(header, row[header])

    def write_mappings(self):
        for header in Mappings.semiexact:
            self.__write_mapping(self.c.semiexact[header], Mappings.semiexact[header], False)

        for header in Mappings.inexact:
            self.__write_mapping('check_' + self.c.inexact[header][0], Mappings.inexact[header], True)

    def __write_mapping(self, file_name, structured_map, is_tuple):
        field_names = "original,anonymized\n"
        with open(file_name, 'w') as mapping_writer:
            mapping_writer.write(field_names)
            count = 0
            alphabetized = sorted(iter(structured_map.keys()))

            for standarized in alphabetized:
                for entry in structured_map[standarized]:
                    if is_tuple:
                        mapping_writer.write(entry[0] + "," + str(count) + "\n")
                    else:
                        mapping_writer.write(entry + "," + str(count) + "\n")
                count = count + 1

    def read_mappings(self):
        for header in Mappings.semiexact:
            Mappings.semiexact_final[header] = self.__read_mapping(self.c.semiexact[header])

        for header in Mappings.inexact:
            Mappings.inexact_final[header] = self.__read_mapping(self.c.inexact[header][0])

        # shouldn't be hard coded, but...
        Mappings.twitter_final = self.__read_mapping('mapping_twitter_handle.csv')

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
    file_name = "original_file.csv"

    m = Mappings()
    m.populate_mappings(file_name)
    m.write_mappings()

if __name__ == '__main__':
    main()
