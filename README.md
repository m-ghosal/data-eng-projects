# data-eng-projects
## Projects completed as part of the Introduction to Data Engineering course
HW1: SQL and Relational Data Modeling (code can be viewed in stocking.py, and exploration of database using SQLite can be viewed in TODO1.txt and TODO2.txt)
- Used SQLite’s command line to explore the Sakila sample database 
    - identified primary key and foreign keys across linked tables to answer important questions about the database
- Compiled the queries into formal code by connecting SQLite to Python
    - created a function called inventory_dataset(), the input of which was an SQLite connection and the output was a Pandas DataFrame

HW2: Entity Resolution (code can be viewed in analyze.py and the accuracy, precision, and recall can be tested by running auto_grader.py)
- Given two large datasets, one with Amazon products and the other with Google products, I found a way to map the same products with each other and output (Amazon ID, Google ID) pairs of the Amazon and Google products that are likely the same.
    - This required cleaning the data first, then grouping by various metrics, and reviewing string and character matches between the smaller groups
- After comparing it with the list of perfect mappings, I got an accuracy of around 51.8% with a runtime of 90 seconds on my laptop
    - This fit under the requirement of the assignment of a 50% accuracy rate with the running time being under 5 minutes on a standard laptop

HW3: Hash (Bloom Filter) (code can be viewed in bloom.py and tested using auto_grader.py)
- Implemented a data structure that uses hashing. A key part of this data structure was to generate a set of "independent" hash functions.
  - Generated K independent hash functions, added a string to the bloom filter, and checked whether the bloom filter actually contained the string.

HW4: Final Project: R-trees and Geospatial Data
- Used DASK and concepts of distributed computing to analyze large relational datasets.
  - cleaned datasets, merged them, and built Rtrees to analyze and plot geospatial data. 
