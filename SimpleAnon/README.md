# Simple Anonymization

This is a bare-bones, no-frills anonymizer that produces a map to allow de-anonymization.

## Overview

Input files need to be in CSV format with a header line. You can optionally specify a quote character.

If you have multiple columns that require anonymization, the program needs to be run multiple times.

If you have multiple columns (possibly in different files) that should have the same map applied to them, the program needs to be run multiple times while specifying the same mapping file. 

## Usage

The example files are original_file1.csv:

|twitter handle|tweet|name|
| -------- | --------- | ---------|
|@asdf|"Hello @qwer"|jack|
|@qwer|"@asdf| does it work if a handle is at the start of the tweet?"|Jill|
|@_asdf|"Make sure that emails like a@b.com are not affected"|jim|
|@QWER |"twitter trivia: @_ is the husband of @__ and father of @___"|jill|

and original_file2.csv:

|twitter handle|age|
|-------|-------|
|@asdf|34|
|@r|65|
|@bnm|45|
|@QWER |3|

We want to anonymize "twitter handle" in both files using the same map, and "name" in the first file.

To anonymize "name" in original_file1.csv:

'''
$ python anon.py original_file1.csv "name" name_key.csv
'''

This produces a file called anon_original_1.csv which has the "name" column anonymized, and name_key.csv, which is the map from the original value (changing everything to lower case and stripping out spaces) to the anonymized value.

Next, we anonymize "twitter handle":

'''
$ python anon.py anon_original_file1.csv "twitter handle" twitter_key.csv
'''

Notice that you need to run it on the file generated in the previous step. This produces a file called anon_anon_original_1.csv which has both "name" and "twitter handle" anonymized, and twitter_key.csv. 

Finally, we anonymize "twitter handle" in the second file:

'''
$ python anon.py original_file2.csv "twitter handle" twitter_key.csv
'''

Since we've specified the same file as we produced in the previous step, the script first reads that map in so that any common twitter handles that occur in both files can be linked.

