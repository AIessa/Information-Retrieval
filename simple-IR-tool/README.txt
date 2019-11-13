
Simple IR tool



System requirements:
			IDEALLY with Python 3.6.4
			(From standard library: sys, pickle, timeit, re, math, operator.itemgetter)
			May need to install: nltk.stem.PorterStemmer
			$ python3 -m pip install nltk
			OR execute:
			$ sudo chmod 777 requirements.sh
			$ ./requirements.sh

			ELSE try earlier version of Python
			>> Following commands for execution should then be run with python ...




Steps for execution:
(Note - check the given filepaths.)

1) Create positional inverted index
	(Optional: Output files already included in directory.
	Executing cw1createindex.py will update these.)

	Execute in console:
	$ python3 cw1createindex.py CW1collection/trec.5000.txt
	(OR: $ python cw1createindex.py CW1collection/trec.5000.txt)

	Console output:
	Time elapsed (timing pre-processing steps, index creation)
	Files: 
	- index.txt
	- (indexvar.txt)
	- (docindexvar.txt)

2) Run cw1exec.py for both queries

	Execute in console:
	$ python3 cw1exec.py CW1collection/queries.boolean.txt
	(OR: $ python cw1exec.py CW1collection/queries.boolean.txt)

	$ python3 cw1exec.py CW1collection/queries.ranked.txt
	(OR: $ python cw1exec.py CW1collection/queries.ranked.txt)

	Console output: 
	- Boolean: query, # of matches found
	- Ranked: query, # of matches found, top 10 matches (+ scores)
	Files: 
	- results.boolean.txt
	- boolquery.resultdocs.txt
	- results.ranked.txt

