# import module
from bs4 import BeautifulSoup
 
# assign html document
html_doc = """
<html>
 
<head>
<meta http-equiv="Content-Type" content="text/html;
charset=iso-8859-1">
<title>An example of HTML page to find the length of
the first tag</title>
</head>
 
<body>
<h2>An example of HTML page to find the length of the
first tag</h2>
 
 
<p>
Beautiful Soup is a library which is essential to scrape
information from web pages.
It helps to iterate, search and modifying the parse tree.</p>
 
 
</body>
</html>
"""
 
# create beautiful soup object
soup = BeautifulSoup(html_doc, 'lxml')
 
# Get all the tags present in the html and
# getting their length
for tag in soup.findAll(True):
    print(tag.name, " : ", len(soup.find(tag.name).text))