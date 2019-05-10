import os
import urllib.parse
import shutil
from time import gmtime, strftime
from distutils.dir_util import copy_tree

#Config

output_folder = 'output'
design_folder = 'design'
articles_folder = 'articles'
temp_folder = 'temp'
final_folder = '../docs'

#Functions

def createFolder(folder):
	try:
		# Create target Directory
		os.mkdir(folder)
		print("Directory " , folder ,  " Created ") 
	except FileExistsError:
		print("Directory " , folder ,  " already exists")    
	return

def articleUrl(article):
	article = article.replace('\'', "_")
	article = article.replace(' ', "_")
	article = urllib.parse.quote_plus(article[8:])
	article = article.replace('%', "")
	return article;

def articleTitle(article):
	return article[:-5][8:]

def mergePages(pages, outfile):
	with open(outfile, 'w') as outf:	
		for fname in pages:
			with open(fname) as infile:
				for line in infile:
					outf.write(line)
	print(outfile)
	return

def deleteFolder(folder):
	if os.path.exists(folder):
		shutil.rmtree(folder)
	print("Directory " , folder ,  " deleted ") 
	return

deleteFolder(temp_folder)
createFolder(temp_folder)
createFolder(output_folder)
output_folder = output_folder + '/' + strftime("%Y%m%d-%H%M%S", gmtime())
createFolder(output_folder)

#Making menu

articles = os.listdir("articles")

f = open(temp_folder + "/articlelist","w+")
f.write("<ul>")
for i in articles:
	f.write("<li><a href=\"" + articleUrl(i) + "\">" + articleTitle(i) + "</a></li>")
	print(articleTitle(i))
f.write("</ul>")
f.close() 

#Making index

filenames = [design_folder + '/header.html', 
			design_folder + '/index1.html', 
			temp_folder + '/articlelist', 
			design_folder + '/index2.html',
			articles_folder + '/' + articles[-1], 
			design_folder + '/footer.html']

mergePages(filenames, output_folder + '/index.html' )

#Making about

filenames = [design_folder + '/header.html', 
			design_folder + '/about.html', 
			design_folder + '/footer.html']

mergePages(filenames, output_folder + '/about.html' )

#Making articles

for article in articles:

	filenames = [design_folder + '/header.html', 
	articles_folder + '/' + article, 
	design_folder + '/footer.html']

	mergePages(filenames, output_folder + '/'+ articleUrl(article))

#Copying css and images

shutil.copyfile(design_folder + '/css.css', output_folder + '/css.css')
print('css.css')
shutil.copyfile(design_folder + '/phoque.png', output_folder + '/phoque.png')
print('phoque.png')
shutil.copyfile(design_folder + '/favicon.png', output_folder + '/favicon.png')
print('favicon.png')

#Clean up 
deleteFolder(temp_folder)
deleteFolder(final_folder)
createFolder(final_folder)
copy_tree(output_folder, final_folder)