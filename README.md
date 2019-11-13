# Mesh2ICD10

Code to translate Mesh codes into ICD10 categories.

## Getting started

Files written in Python 2.7 because USML API is developed for Python 2.7 and Python 3.0 (uses python 3 prints with from future import ...).

We use two codes from UMLS API: src/Authenticator.py and src/crosswalk.py. Other codes from UMLS API are within uts-rest-api/ in case we need them.

### Prerrequisites

You need an API key from UMLS API to translate Mesh codes into ICD10 categories with the code src/crosswalk.py

+ Python 2.7

+ pandas                    0.24.2

+ requests                  2.22.0

+ argparse                  1.4.0


### Installing

```
git clone <repo_url>
```

## Running the scripts


### 1. Filter PubMed results and get its Mesh codes

+ Script: src/filter_pubmed_articles.py

+ Description:

1. Keep only PubMed results with abstract and Mesh terms.

2. Create CSV with Pubmed IDs and Mesh terms associated to that article

3. Get unique MeSH terms in our results and create a txt with them.

+ Input: PubMed XML with results downloaded from its webpage. docs/filtered_results.xml

+ Output: Text file with Mesh codes (docs/mesh-codes.txt) and CSV file with PubMed Id and its Mesh codes (docs/filtered_results.csv)

+ Execute:

You may need to open file and change paths. 

```
python filter_pubmed_articles.py
```


### 2. Translate Mesh codes in XML with PubMed results into ICD10

+ Script: src/crosswalk.py

+ Description: Uses UMLS API to translate Mesh codes in docs/mesh-codes.txt to ICD10 categories. Saves mapping result into a CSV file

+ Input: Text file with Mesh codes (docs/mesh-codes.txt)

+ Output: A CSV file with

Mesh code;ICD10 code; ICD10 description 

(output/dict.txt)

+ Execute: 

You may need to open file and change paths. 

```
python crosswalk.py -k API_KEY
```

## Files information

##### src/Authenticator.py

Sets up authentication details with UMLS API. We only have to provide the API key.

##### src/filter_pubmed_articles.py

Filter dumpled PubMed articles. Select those that have abstract and MeSH terms.

Also, create CSV with: pubmedID;Mesh Term;Mesh Description;Mesh Qualifier;Mesh Qualifier Description

Also, create txt with: list of Mesh terms in CSV

Output: docs/filtered_results.xml, docs/filtered_results.csv, docs/mesh-code.txt

##### src/crosswalk.py
Make API calls to UMLS API. Send Mesh code and retrieves equivalent ICD10 code. Create dict file with Mesh code, ICD10 code and ICD10 description

Output: output/dict.txt

##### data/

Downloaded XML PubMed Results



