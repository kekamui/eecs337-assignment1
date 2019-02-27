Group members: Daniel McGrory, Jimmy Kooy, Kevin Mui, Youngeon Kim

HOW TO RUN:
Run gg_api.py with every year you wish to grade as a separate argument.
For example, if you want to grade our outputs for the years 2013, 2015, and 2018, use the following command:
python gg_api.py 2013 2015 2018
After running gg_api.py, the autograder should be able to successfully produce grades for all of the years passed to gg_api.py as arguments.

Files containing the json data for each of the 5 info types for a given year should be generated in the same directory as the gg_api.py and results_assembler.py
These files will be named "resultsYEAR.json" where year is the year (i.e. 2013, 2018) of the corpus from which the results were generated.

Human readable information will be printed to the console during the running of gg_api.py for the given years provided.

The packages we used are NLTK, spaCy, en_core_web_sm, re, json, sys, and operator.
NLTK can be found here: https://www.nltk.org/install.html
spaCy can be found here: https://spacy.io/usage/
en_core_web_sm can be downloaded using spaCy's download: python -m spacy download en_core_web_sm

Github repository: https://github.com/kekamui/eecs337-assignment1

Notes: Everything but finding awards and presenters take a reasonably short time to run. For 2013, awards take 2 minutes and presenters take 1 minute.
