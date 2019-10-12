# bobby
Biblio extractor for PubMed: This script will extract following using user supplied PMID:
- Title
- Abstract
- Authors
- Affiliations
- Citation Info
- URL

Disclaimer: This is a web scraping script for PubMed. Only for educational purposes. Kindly do not exploit. if you want to extract data, PubMed provides Restful APIs, use that.

## bobby_v3:
Takes a csv filepath/filename as input. The csv file must have PMIDs in column A with first PMID starting at cell A2.
### How to run?: use command-line argument >>> python3 bobby_v2.py pmid_list.csv
#make sure to change directory (use: cd path_to_bobby_v2.py) in terminal window to whereever bobby_v2.py is stored on your pc

#output will be produced in a new csv file titled "output_file_bobby_v3.csv".


## bobby_v2:
Takes a csv filepath/filename as input. The csv file must have PMIDs in column A with first PMID starting at cell A2.
### How to run?: use command-line argument >>> python3 bobby_v2.py pmid_list.csv
#make sure to change directory (use: cd path_to_bobby_v2.py) in terminal window to whereever bobby_v2.py is stored on your pc

#output will be produced in the terminal window itself.

## bobby_v1:
Takes only one PMID at a time.

### How to run?: use command-line argument >>> python3 bobby_v1.py pmidHere
#make sure to change directory (use: cd path_to_bobby_v1.py) in terminal window to whereever bobby_v1.py is stored on your pc

#output will be produced in the terminal window itself.
