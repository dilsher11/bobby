import sys, requests, csv
from bs4 import BeautifulSoup as bs

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
	total_pmids = len(pmid_url_dict)
	counter = 1
	print(f"Total number of PMIDs to extract: {total_pmids}")
	database = []
	for pmid, url in pmid_url_dict.items():
		print(f"Extracting PMID: {pmid} ({str(counter)}/{str(total_pmids)})")
		counter += 1
		try:
			r = requests.get(url)
		except:
			if database:
				outputGen(database)
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
		if abstract.lower().startswith("abstract"):
			abstract = abstract[8:]
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
		"PMID" : pmid,
		"Title" : title,
		"Abstract" : abstract,
		"Authors" : authors,
		"Affiliations" : affiliations,
		"Citation Info" : cite_info,
		"URL" : url,
	}
	return biblio

def outputGen(database):
	with open("output_file_bobby_v3.csv", "w", newline="") as file_object:
		header_row = ["PMID", "Title", "Abstract", "Authors", "Affiliations", "Citation Info", "URL"]
		writer = csv.DictWriter(file_object, fieldnames=header_row)
		writer.writeheader()
		for items in database:
			writer.writerow(items)
"""
-------------------------------------------------------------------------------
PROGRAM:
-------------------------------------------------------------------------------
"""
filename = sys.argv[1]
pmids = pmidList(filename)
pmid_url_dict = urlDict(pmids)
dataX = scrapeData(pmid_url_dict)
outputGen(dataX)
