import csv
import time
import mappings
import re


class Anon:
    methods = dict()
    def __init__(self, m):
        self.m = m
        Anon.methods = {"delete_left_characters": self.__delete_left_characters,
                        "delete_right_characters": self.__delete_right_characters,
                        "get_year": self.__get_year,
                        "none": self.__none,
                        "inexact_mapping": self.__inexact_mapping,
                        "semiexact_mapping": self.__semiexact_mapping,
                        "regex_twitter_handles": self.__regex_twitter_handles}

    def __delete_right_characters(self, entry, header):
        return entry[: -int(self.m.c.all[header][1])]

    def __delete_left_characters(self, entry, header):
        return entry[int(self.m.c.all[header][1]):]

    def __get_year(self, entry, header):
        return str(time.strptime(entry, self.m.c.all[header][1]).tm_year)

    def __inexact_mapping(self, entry, header):
        return self.m.inexact_final[header][entry]

    def __semiexact_mapping(self, entry, header):
        return self.m.semiexact_final[header][entry]

    def __regex_twitter_handles(self, entry, header):
        tokens = re.findall("(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z_]+[A-Za-z0-9_]+)", entry)
        for token in tokens:
            handle = '@' + token
            if handle in self.m.twitter_final:
                entry = entry.replace(handle, '@' + self.m.twitter_final[handle])
        return entry

    def __none(self, entry, header):
        return entry

    def go(self, file_name, new_file_name):
        with open(file_name, 'r') as infile, open(new_file_name, 'w') as outfile:
            infile_reader = csv.DictReader(infile, delimiter=',', quotechar='"')
            outfile.writelines(str.join(',', infile_reader.fieldnames) + '\n')
            for row in infile_reader:
                for header in infile_reader.fieldnames:
                    out_entry = '\"' + self.methods[self.m.c.all[header][0]](row[header], header) + '\"'
                    outfile.write(out_entry + ',')
                outfile.write('\n')


def main():
    # file names should be passed as argument
    file_name = "original_file.csv"
    new_file_name = "anon_file.csv"

    m = mappings.Mappings()
    m.read_mappings()
    a = Anon(m)
    a.go(file_name, new_file_name)


if __name__ == '__main__':
    main()
