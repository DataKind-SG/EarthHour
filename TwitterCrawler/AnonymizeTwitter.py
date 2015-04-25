import numpy as np
import glob
import csv


class AnonymizeTwitter:
    def __init__(self):
        self.user_file_01 = 'data/final/anon/users_d0-1.csv'
        self.user_file_2 = 'data/final/anon/users_d2.csv'
        self.connection_file_01 = 'data/final/anon/connection_d0-1.csv'
        self.connection_file_12 = 'data/final/anon/connection_d1-2.csv'
        self.map_file = 'data/final/map/map.csv'
        self.chapter_map_file = 'data/final/map/chapter_map.csv'
        self.log_file = 'data/final/log.csv'

        self.chaptersfile = 'data/final/d0/chapters.csv'
        self.chapter_hydrated_followers = 'data/final/d0/*hydrated_followers.csv'
        self.chapter_unhydrated_followers = 'data/final/d0/*_followers.csv'
        self.d2_followers = 'data/final/connections/out_list_*.csv'
        self.d2_hydrated_followers = 'data/final/d2/hydrated_out_list_*.csv'
        self.counter = 0
        self.rand = np.random.permutation(range(10000000, 60000000))
        self.map = dict()
        self.chapter_map = dict()
        self.user_header = 'anon_id,created_at,description,lang,location,time_zone,utc_offset,statuses_count,favourites_count,followers_count,friends_count,listed_count,contributors_enabled,protected,verified\n'

    def __get_anon_value(self, user_id):
        num_id = long(user_id)
        if num_id not in self.map:
            self.map[num_id] = self.rand[self.counter]
            self.counter += 1
            did_exist = False
        else:
            did_exist = True
        return str(self.map[num_id]), did_exist

    def __write_user_row(self, row, anon_id):
        return '%s,%s,"%s",%s,"%s",%s\n' % (anon_id, row[3], row[4], row[5], row[6], ','.join(row[8:]))

    def anon_users_d0(self):
        log_writer = open(self.log_file, 'w')
        log_writer.write('file,line count,self.counter\n')

        chapter_counter = 0
        map_writer = open(self.map_file, 'w')
        map_writer.write('twitter_id,anon_id,screen_name\n')

        chapter_map_writer = open(self.chapter_map_file, 'w')
        chapter_map_writer.write('twitter_id,anon_id,screen_name\n')

        user_writer = open(self.user_file_01, 'w')
        user_writer.write(self.user_header)

        with open(self.chaptersfile) as orig_reader:
            orig_reader.readline()
            csv_reader = csv.reader(orig_reader, delimiter=',', quotechar='"')
            line_count = 0
            for row in csv_reader:
                self.chapter_map[row[2].lower()] = chapter_counter
                self.map[long(row[0])] = chapter_counter
                map_writer.write('%s,%s,%s\n' % (row[0], str(chapter_counter), row[2]))
                chapter_map_writer.write('%s,%s,%s\n' % (row[0], str(chapter_counter), row[2]))
                user_writer.write(self.__write_user_row(row, chapter_counter))
                chapter_counter += 1
                line_count += 1

        log_writer.write('%s,%s,%s\n' % (self.chaptersfile, str(line_count), str(self.counter)))

        map_writer.close()
        chapter_map_writer.close()
        user_writer.close()
        log_writer.close()

        print 'Finished anon_d0'

    def anon_users_d1(self):
        chapter_files = glob.glob(self.chapter_hydrated_followers)
        chapter_files.sort()
        for chapter_file in chapter_files:
            user_writer = open(self.user_file_01, 'a')
            map_writer = open(self.map_file, 'a')

            with open(chapter_file, 'r') as orig_reader:
                orig_reader.readline()
                csv_reader = csv.reader(x.replace('\0', '\n') for x in orig_reader)
                line_count = 0

                for row in csv_reader:
                    if len(row) != 18:
                        continue
                    anon_id, did_exist = self.__get_anon_value(row[0])
                    if not did_exist:
                        row[3] = row[3][:10]
                        if row[8] == 'None':
                            row[8] = ''
                        if row[9] == 'None':
                            row[9] = ''
                        user_writer.write(self.__write_user_row(row, anon_id))
                        map_writer.write('%s,%s,%s\n' % (row[0], str(anon_id), row[2]))
                    line_count += 1

            log_writer = open(self.log_file, 'a')
            log_writer.write('%s,%s,%s\n' % (chapter_file, str(line_count), str(self.counter)))
            log_writer.close()

            user_writer.close()
            map_writer.close()

            print 'Finished ' + chapter_file
        print 'Finished anon_users_d1'

    def anon_users_d2(self):
        user_writer = open(self.user_file_2, 'w')
        user_writer.write(self.user_header)
        user_writer.close()

        hydrated_files = glob.glob(self.d2_hydrated_followers)
        hydrated_files.sort()
        for hydrated_file in hydrated_files:

            user_writer = open(self.user_file_2, 'a')
            map_writer = open(self.map_file, 'a')

            with open(hydrated_file, 'rb') as orig_reader:
                orig_reader.readline()
                csv_reader = csv.reader(x.replace('\0', '\n') for x in orig_reader)
                line_count = 0
                for row in csv_reader:
                    if len(row) != 18:
                        continue
                    anon_id, did_exist = self.__get_anon_value(row[0])
                    if not did_exist:
                        user_writer.write(self.__write_user_row(row, anon_id))
                        map_writer.write('%s,%s,%s\n' % (row[0], str(anon_id), row[2]))
                    line_count += 1

            log_writer = open(self.log_file, 'a')
            log_writer.write('%s,%s,%s\n' % (hydrated_file, str(line_count), str(self.counter)))
            log_writer.close()
            user_writer.close()
            map_writer.close()

            print 'Finished ' + hydrated_file
        print 'Finished anon_users_d2'

    def anon_connections_d0_1(self):
        connection_writer = open(self.connection_file_01, 'w')
        connection_writer.write('user,follower\n')
        connection_writer.close()

        chapter_files = glob.glob(self.chapter_hydrated_followers)
        unhydrated_files = [item for item in glob.glob(self.chapter_unhydrated_followers) if item not in chapter_files]
        unhydrated_files.sort()
        for unhydrated_file in unhydrated_files:
            tokens = unhydrated_file.split('/')
            chapter = tokens[len(tokens) - 1].split('_')[0]
            anon_chapter = str(self.chapter_map[chapter.lower()])

            connection_writer = open(self.connection_file_01, 'a')
            map_writer = open(self.map_file, 'a')

            with open(unhydrated_file, 'r') as orig_reader:
                orig_reader.readline()
                line_count = 0
                for row in orig_reader:
                    anon_id, did_exist = self.__get_anon_value(row[:-1])
                    connection_writer.write('%s,%s\n' % (anon_chapter, anon_id))
                    if not did_exist:
                        map_writer.write('%s,%s\n' % (row[:-1], anon_id))
                    line_count += 1

            log_writer = open(self.log_file, 'a')
            log_writer.write('%s,%s,%s\n' % (unhydrated_file, str(line_count), str(self.counter)))
            log_writer.close()
            connection_writer.close()
            map_writer.close()

            print 'Finished ' + unhydrated_file
        print 'Finished anon_connections_d0_1'

    def anon_connections_d1_2(self):
        connection_writer = open(self.connection_file_12, 'w')
        connection_writer.write('user,follower\n')
        connection_writer.close()

        follower_files = glob.glob(self.d2_followers)
        follower_files.sort()
        for follower_file in follower_files:
            connection_writer = open(self.connection_file_12, 'a')
            map_writer = open(self.map_file, 'a')

            with open(follower_file, 'r') as orig_reader:
                line_count = 0
                for row in orig_reader:
                    tokens = row.split(',')
                    if len(tokens) != 2:
                        continue

                    anon_id_0, did_exist = self.__get_anon_value(tokens[0])
                    if not did_exist:
                        map_writer.write('%s,%s\n' % (tokens[0], anon_id_0))

                    anon_id_1, did_exist = self.__get_anon_value(tokens[1][:-1])
                    if not did_exist:
                        map_writer.write('%s,%s\n' % (tokens[1][:-1], anon_id_1))

                    connection_writer.write('%s,%s\n' % (anon_id_0, anon_id_1))
                    line_count += 1

            log_writer = open(self.log_file, 'a')
            log_writer.write('%s,%s,%s\n' % (follower_file, str(line_count), str(self.counter)))
            log_writer.close()
            connection_writer.close()
            map_writer.close()
            print 'Finished ' + follower_file
        print 'Finished anon_connections_d1_2'


def main():
    at = AnonymizeTwitter()
    at.anon_users_d0()
    at.anon_users_d1()
    at.anon_users_d2()
    at.anon_connections_d0_1()
    at.anon_connections_d1_2()

if __name__ == '__main__':
    main()
