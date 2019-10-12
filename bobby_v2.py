import sys, requests, csv
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

"""
-------------------------------------------------------------------------------
FUNCTIONS:
-------------------------------------------------------------------------------
"""
def pmidList(filePath):
	with open(filename) as file_object:
		reader = csv.reader(file_object)
		header_row = next(reader)
		pmids = [str(data_rows[0]) for data_rows in reader]
	return pmids

def urlDict(pmids):
	pmid_url_dict = {}
	for pmid in pmids:
		url = "https://www.ncbi.nlm.nih.gov/pubmed/" + pmid
		pmid_url_dict[pmid] = url
	return pmid_url_dict

def scrapeData(pmid_url_dict):
	database = []
	for pmid, url in pmid_url_dict.items():
		print(f"Extracting PMID: {pmid}")
		try:
			r = requests.get(url)
		except:
			if database:
				printData(database)
			print(f"Connection error occured. PMIDs extracted: {len(database)}")
			sys.exit()
		soup = bs(r.content, "lxml")
		title = soup.findAll("h1")
		abstract = soup.findAll("div", {"class":"abstr"})
		author_list = soup.findAll("div", {"class":"auths"})
		try:
			authors = author_list[0].findChildren("a", recursive=False)
		except:
			pass
		affiliation_list = soup.findAll("div", {"class":"afflist"})
		try:
			affiliations = affiliation_list[0].findChildren("dd", recursive=True)
		except:
			pass
		cite_info = soup.findAll("div", {"class":"cit"})

		title, abstract, authors, affiliations, cite_info = cleanData(title, abstract, authors, affiliations, cite_info)
		biblio = dictBuilder(pmid, title, abstract, authors, affiliations, cite_info, url)
		database.append(biblio)
	return database

def cleanData(title, abstract, authors, affiliations, cite_info):
	try:
		title = title[1].text
	except:
		title, abstract, authors, affiliations, cite_info = "Not found"
		return title, abstract, authors, affiliations, cite_info
	try:
		abstract = abstract[0].text
	except:
		abstract = "Not found"
	try:
		authors = " | ".join([author.text for author in authors])
	except:
		authors = "Not found"
	try:
		affiliations = " | ".join([affiliation.text for affiliation in affiliations])
	except:
		affiliations = "Not found"
	try:
		cite_info = cite_info[0].text
	except:
		cite_info = "Not found"
	return title, abstract, authors, affiliations, cite_info

def dictBuilder(pmid, title, abstract, authors, affiliations, cite_info, url):
	biblio = {
		"PMID:" : pmid,
		"Title:" : title,
		"Abstract:" : abstract,
		"Authors:" : authors,
		"Affiliations:" : affiliations,
		"Citation Info:" : cite_info,
		"URL:" : url,
	}
	return biblio

def printData(database):
	for items in database:
		for key, value in items.items():
			print(key, value, end="\n\n")
		print("\n\n")
"""
-------------------------------------------------------------------------------
PROGRAM:
-------------------------------------------------------------------------------
"""
filename = sys.argv[1]
pmids = pmidList(filename)
pmid_url_dict = urlDict(pmids)
dataX = scrapeData(pmid_url_dict)
printData = printData(dataX)