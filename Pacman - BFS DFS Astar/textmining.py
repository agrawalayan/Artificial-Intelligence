# $Id: Nielsen2012Python_case.py,v 1.2 2012/09/02 16:55:25 fn Exp $

# Define a url as a Python string (note we are only getting 100 documents)
url = "https://www.nytimes.com/"

# Import the 'urllib' module for Web page retrieval
from urllib import urlopen

# Get help on how to use the module
#help('urllib')

# Get and read the web page
doc = urlopen(url).read()  # Object from urlopen has read function

# Show the first 1000 characters
print(doc[:100])
