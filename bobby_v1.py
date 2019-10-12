import sys, requests
from bs4 import BeautifulSoup as bs

"""
-------------------------------------------------------------------------------
FUNCTIONS:
-------------------------------------------------------------------------------
"""
def htmlToList(htmlList):
	"""This function converts lists with html items into list with text items
	"""
	htmlList = [i.text for i in htmlList]
	return htmlList

"""
-------------------------------------------------------------------------------
PROGRAM:
-------------------------------------------------------------------------------
"""
#cmd input
pmid = sys.argv[1]
url = "https://www.ncbi.nlm.nih.gov/pubmed/"
url += str(pmid)

#get url
r = requests.get(url)
#instance of bs, pass html doc to it for parsing
soup = bs(r.content, "lxml")

# find fields
title = soup.findAll("h1")
abstr = soup.findAll("div", {"class":"abstr"})
author_list = soup.findAll("div", {"class":"auths"})
try:
	authors = author_list[0].findChildren("a", recursive=False)
	authors = htmlToList(authors)
except:
	pass
affiliation_list = soup.findAll("div", {"class":"afflist"})
try:
    affiliations = affiliation_list[0].findChildren("dd", recursive=True)
    affiliations = htmlToList(affiliations)
except:
    pass
cite_info = soup.findAll("div", {"class":"cit"})

#print output
try:
    print("Title:", title[1].text, sep="\n", end="\n\n")
except:
    print("No document found")
    exit()
print("Abstract:")
try:
    print(abstr[0].text, sep="\n", end="\n\n")
except:
    print("Abstract not found", end="\n\n")
print("Authors:")
try:
    print(*authors, sep=" | ", end="\n\n")
except:
    print("Authors not found", end="\n\n")
print("Affiliations:")
try:
    for index, affiliation in enumerate(affiliations):
    	print(index+1, affiliation, sep=". ")
    print()
except:
    print("Affiliations not found!", end="\n\n")
try:
    print("Cite using:", cite_info[0].text)
except:
    print("Citation not found")