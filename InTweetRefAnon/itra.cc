//
// DataKind Singapore in-tweet reference anonimization application.
//
// Written for DKSG DataDive April 2015
//
//   This requires boost-regex to run.
//   It assumes a long is 64 bit integer and int is 32 bit.
//
//
//  My compile:
// g++ -c -O2 -W -Wall -m64 -fPIC -I(boost incdir) -o itra.o itra.cc
//
//  My link:
// g++ -o itra itra.o -L(boost libdir) -lboost_regex-gcc44-mt-1_55  


#include <iostream>
#include <fstream>
#include <map>
#include <cstring>
#include <cstdlib>
#include <boost/regex.hpp>

using namespace std;
using namespace boost;

//
// Helper class to parse the entries in the anonimization file.
//
struct Anon
{
    long                 twitter_id;
    int                  anon_id;
    std::string          screen_name;

    Anon() :
        twitter_id (-1),
        anon_id    (-1)
    {}

    bool parse (char *line)
    {
        char    *n = strtok (line, ",\r");

        if (n) {
            twitter_id = atol (n);

            n = strtok (NULL, ",");
        }

        if (n) {
            anon_id = atoi (n);

            n = strtok (NULL, ",");
        }

        if (n)
            screen_name = n;

        return !screen_name.empty();
    }
};


/******************************************************************************
 *
 *  main() - main function.
 *
 *****************************************************************************/

int main (int argc, char *argv[])
{
    if (argc < 3) {
        cerr << "Usage " << argv [0] << " <anon-map.csv> <tweets.csv>" << endl;
        cerr << "Output goes to stdout, all other info to stderr" << endl;

        return 1;
    }

    ifstream    aFile (argv [1]);

    if (!aFile) {
        cerr << "Anonimization file can't be opened: " << argv [1] << endl;

        return 1;
    }

    map <string, Anon *>    anons;
    int                     count = 0;
    char                    line [1024];

    // Skip the header line
    aFile.getline (line, 1024);

    while (aFile.getline (line, 1024)) {
        Anon *a = new Anon();

        if (a->parse (line))
            anons [a->screen_name] = a;
        else {
            cerr << "FAIL anonimizing " << count + 1 << ": "
                 << a->twitter_id << " " << a->anon_id
                 << " [" << a->screen_name << "]" << endl;

            delete a;
        }

        if (!(++count % 100000))
           cerr << "Parsed " << count << endl;
    }

    aFile.close();

    cerr << "Total " << anons.size() << " anoninmization entries" << endl;

    ifstream    tFile (argv [2]);

    if (!tFile) {
        cerr << "Tweet file can't be opened: " << argv [2] << endl;

        while (!anons.empty()) {
            delete anons.begin()->second;

            anons.erase (anons.begin());
        }

        return 1;
    }

    count = 0;

    while (tFile.getline (line, 1024)) {
        string  s (line);

        // Grabbed from Oliver / stackoverflow
        regex   r ("(?<=^|(?<=[^a-zA-Z0-9\\-_\\.]))@([A-Za-z]+[A-Za-z0-9]+)");

        // Also from stackoverflow - example of boost regex findall
        sregex_token_iterator i (s.begin(), s.end(), r, 0);
        sregex_token_iterator end;

        for( ; i != end; ++i ) {
            // strip @ from the matched-name
            string    name = string (*i, 1);

            // If the name is found in the map, then print anon-name
            map <string, Anon *>::const_iterator ai = anons.find (name);

            if (ai != anons.end()) {
                int       x = ai->second->anon_id;
                size_t    p = s.find (name);

                while (p != string::npos) {
                    cout << s.substr (0, p) << x << '@';

                    s = string (s, p + name.size());

                    p = s.find (name);
                }
            }
        }

        // Print the remainder of the record
        cout << s << endl;

        if (!(++count % 10000))
           cerr << "Replaced " << count << " tweets" << endl;
    }

    tFile.close();

    while (!anons.empty()) {
        delete anons.begin()->second;

        anons.erase (anons.begin());
    }

    return 0;
}
