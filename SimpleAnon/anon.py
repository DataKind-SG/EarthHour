import csv
import numpy as np
import sys
import os.path


class Anon:
    def __init__(self):
        self.mapping = dict()
        self.orig_file = ''
        self.anon_file = ''
        self.column = ''
        self.mapping_file = ''
        self.mapping_exists = False
        self.rand_perm = np.random.permutation(range(1000000, 9999999))
        self.count = 0
        self.quotechar = '"'

    def parse_arguments(self):
        n_args = len(sys.argv) - 1
        if n_args == 4:
            self.quotechar = sys.argv[4]
        elif n_args != 3:
            print 'Need to have three or four arguments for anon.py'
            return False

        self.orig_file = sys.argv[1]
        if not os.path.isfile(self.orig_file):
            print 'File in first argument does not exist'
            return False

        self.anon_file = 'anon_' + self.orig_file

        self.column = sys.argv[2]
        with open(self.orig_file, 'r') as csvfile:
            orig_reader = csv.DictReader(csvfile, delimiter=',', quotechar=self.quotechar)
            if self.column not in orig_reader.fieldnames:
                print 'Column in second argument does not exist'
                return False

        self.mapping_file = sys.argv[3]
        if os.path.isfile(self.mapping_file):
            self.__read_mapping()
            self.mapping_exists = True

        return True

    def anonymize(self):
        with open(self.anon_file, 'w') as anon_writer:
            with open(self.orig_file, 'r') as csvfile:
                orig_reader = csv.DictReader(csvfile, delimiter=',', quotechar=self.quotechar)
                columns = orig_reader.fieldnames
                anon_writer.write(",".join(columns) + "\n")

                for row in orig_reader:
                    if row[self.column] is not None:
                        row[self.column] = self.__get_add_map_entry(row[self.column])
                    else:
                        row[self.column] = ''

                    line = []
                    for item in columns:
                        line.append('%s%s%s' % (self.quotechar, row[item], self.quotechar))
                    anon_writer.write('%s\n' % ",".join(line))

        self.__write_mapping()

    def __get_add_map_entry(self, entry):
        standardized = self.__semi_standardize_string(entry)
        if standardized in self.mapping:
            anon_value = self.mapping[standardized][0]
        else:
            anon_value = self.rand_perm[self.count]
            self.count += 1
            self.mapping[standardized] = (anon_value, True)

        return str(anon_value)

    @staticmethod
    def __semi_standardize_string(entry):
        standardized = entry.lower()
        standardized = standardized.replace(' ', '')
        return standardized

    def __read_mapping(self):
        used_keys = set()
        with open(self.mapping_file, 'r') as csvfile:
            map_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in map_reader:
                anon_value = int(row['anonymized'])
                self.mapping[row['original']] = (anon_value, False)
                used_keys.add(anon_value)

            self.rand_perm = [item for item in self.rand_perm if item not in used_keys]

    def __write_mapping(self):
        with open(self.mapping_file, 'a') as write_map:
            if not self.mapping_exists:
                write_map.write('original,anonymized\n')

            for orig in self.mapping:
                if self.mapping[orig][1]:
                    write_map.write('"%s",%s\n' % (orig, str(self.mapping[orig][0])))


def main():

    a = Anon()
    if not a.parse_arguments():
        return
    a.anonymize()


if __name__ == '__main__':
    main()



