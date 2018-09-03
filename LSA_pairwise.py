import pandas as pd
from mechanize import Browser
from Tkinter import Tk
from tkFileDialog import askopenfilename,askdirectory

Tk().withdraw()
csvpath=askopenfilename(title = "Select csv of word pairs") #Loading the file
outputFolder=askdirectory(title = "Select an output directory") #Where do you want to save it
col1 = raw_input('Column name of the first word: ')
col2 = raw_input('Column name of the second word: ')

print 'Reading '+ csvpath

# read in the data and fix format
data=pd.DataFrame.from_csv(csvpath, index_col=None)
listWords = []

# chunk data into parts of 3500 pairs. Bcs if list > 3500 pairs : error
def chunk(l, n):
	for i in range(0, len(l), n):
		yield l[i:i+n]

chunks = chunk(data, 3500)
for current_chunk in chunks:
	temp_list = []
	for index,row in current_chunk.iterrows():
		temp_list.append(row[col1])
		temp_list.append(row[col2])
	listWords.append(temp_list)




def getLSAratings(listWords, data=None, numFactors='', url="http://lsa.colorado.edu/cgi-bin/LSA-pairwise.html"):
	"""Get ratings for pairs of words from LSA website and outpus it to a table.
	numFactors = Number of factors to use, see LSA website for details. Default=300
	listWords = List of words to get LSA ratings for"""

	LSA=[]
	print ("\nComputing...\n")
	for sub_list in listWords:
		formattedWords = "\r\n\r\n".join(sub_list)
		br = Browser()

		br.open(url)
		br.select_form(nr=0)
		br["LSAFactors"] = numFactors
		br["txt1"]=formattedWords
		br.submit()

		df =  pd.read_html(br.response().read(),header=None, index_col=None)
		br.response().close()
		del br

		for pair in df:
			LSA.append(pair[1][1])
	data['LSA']=LSA

	return data

data_out = getLSAratings(listWords,data)
print 'Saving', outputFolder + '/LSAratings_'+csvpath.split('/')[-1]
data_out.to_csv(outputFolder+ '/LSAratings_'+csvpath.split('/')[-1], index=None)
print 'Done.'
