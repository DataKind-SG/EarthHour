# In Tweet Reference Anonymization

Replace all twitter screen name references mentioned in a file with their corresponding anonymized handle instead.

Building this application requires the boot regex library.


## Overview

This is an anonimization follow-up application written in C++ (for performance reasons). It can be applied after the basic anonymization mapping is created. Other applications, elsewhere in this repository (../Anon and ../SimpleAnon) handle that.

The application simply matches a twitter screen name by means of a regex:

> "(?<=^|(?<=[^a-zA-Z0-9\\-_\\.]))@([A-Za-z]+[A-Za-z0-9]+)"

If such a twitter reference is found in the secrets list, then it is replaced by the coded key **plus another trailing @**... We added the '@' so the handle can easily be grabbed by someone looking for matches.



## Usage

> ./itra anon-map.csv tweets.csv > anonimized-tweets.csv

All results are written to stdout, so in the example, the output is redirected to the file called anonimized-tweets.csv.

All other relevant info (including a somewhat meaningful measurement of progress) is written to stderr.

Input files need to be in text format with a header line. Only the strucutre of the anonymization key (anon.csv) is important.

It's structure must be as follows:

|handle|anon|name|
| --- | --- | --- |
|12341234|42|mrbla|
|12345678|43|foobar|

