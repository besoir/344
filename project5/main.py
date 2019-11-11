#massive amounts of imports here, mainly to handle the emailing of the file
#some are commented out becuase I was originally using them or they were there for a test
import os,subprocess,sys,zipfile,smtplib
from lxml import etree
import re
from io import BytesIO
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#path = sys.argv[1]
#path = input("Directory: ")

#############################################################################################################
#This is the method we created for the microproject
#It takes a file and returns its wordcount
#It has to split some of the stuff returned because it actually returns more garbage than we need
#############################################################################################################
def wordcounter(fileName):
	path = fileName
	if os.path.isfile(fileName):
		p = subprocess.Popen(["wc", "-l", fileName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		res = p.communicate()[0].decode('UTF-8')
		trash = res.split()
		print(fileName + ": " + str(trash[0]))
		return str(trash[0])

#############################################################################################################
#this was the most tedious method that was written
#the problem i had was really how much of the process of grabbing all the words do i need to execute in the 
#method
#originally it just returned a list but I ended up returning a set
#First I defined a set called usa to return later
#Then I open the file that I want to gather the words from
#Then I delete the following things:
#1: Lines that start with #, because those lines are comments in python and replace the line with ""
#2: Lots of whitespace: tabs and other things like that (whitespaces) and replace with just ""
#3: Lines that start with %, because those lines are comments in prolog and replace the line with ""
#4: Lines that start with /, because those lines are comments in C and scala and replace the line with ""
#5: Lines with ; becuase those are end statements in C and comments in clojure
#Then I gather all of the characters between whitespace and then:
#Strip the tabs returns and new line characters
#Sub whitespace with ""
#Strip with new lines again
#Then we check if we already have seen that word,
#If not then we add it to the set, if we have we move on to the next word
#Finally we return the set
#############################################################################################################
def wordgrabber(fileName):
	usa = set()
	#listofwords = []
	with open(fileName, "r") as opener:
		for currLine in opener:
			currLine = re.sub("(\#)+.*(?=\s)", "", currLine)
			currLine = re.sub("\"\s*.*?\s*\"", "", currLine)
			currLine = re.sub("(\%)+.*(?=\s)", "", currLine)
			currLine = re.sub("(\//.*)", "", currLine)
			currLine = re.sub("(\;.*)", "", currLine)
			currLine = re.findall("(\s*[a-zA-Z]*\s*)", currLine)
			#listofwords.append(currLine)
			for y in currLine:
				y = y.rstrip('\t\r\n')
				y = re.sub("\s+", "", y)
				y = y.rstrip('\n')
				if usa.__contains__(y) is False:
					usa.add(y)
	return usa

#############################################################################################################
#This method is used to write all of the files words to an xml file for that individual file
#First we create a root element, followed by a doc subelement, I needed both I couldn't get it to work without
#both of these
#Next for each file in the list of files we were passed, we:
#1. Create a href so that we can use it to link ourselves to each project we created
#2. Create a subelement to doc called files, to show that this is a file in the xml
#3. Set the path to the file as an attribute so we can call it later
#4. Set the files name to the file we are looking at
#Note: I never use the name, because I couldn't get the xsl file take both args
#Next we make another files element in order to get back to the main html page
#Next we create a wc element to give the wordcount to the xml file
#We set it as text because I think it looks better in the xml that way
#Next we have to do some tedious garbage
#For each word that is in the set listofwords that was passed to us, we:
#Create a currWord subelement
#Create a wordin subelement so that when we do a for each in xsl we dont skip any
#Set the wordin text to the word we are looking at in listofwords
#Next we make an element tree from the root element
#We have to set all of this weird stuff up to lisnk the html, xsl and xml files together
#This is what the sethead is for
#Then we let the file write to itself
#############################################################################################################
def xmlwriter(files, wordcount, count, listofwords):  
	root = etree.Element("root")
	doc = etree.SubElement(root, "doc")

	i = 1
	for file in files:
		href = "../project" + str(i) + "/" + file
		files = etree.SubElement(doc, "files")
		files.set("path", href)
		#flie = etree.SubElement(files, "file")
		files.text = file
		i+=1

	files = etree.SubElement(doc, "files")
	href = "index.html"
	files.set("path", href)
	#flie = etree.SubElement(files, "file")
	files.text = "home"
	
	wc = etree.SubElement(doc, "wc")
	words = etree.SubElement(wc, "words")
	words.text = wordcount

	for word in listofwords:
		currword = etree.SubElement(doc, "currword")
		wordin = etree.SubElement(currword, "wordin")
		wordin.text = word

	tree = etree.ElementTree(root)
	sethead = b"""<?xml version="1.0" encoding="utf-8"?><?xml-stylesheet type='text/xsl' href='yes.xsl'?>"""
	with open("a"+ str(count) + ".xml", 'wb') as writer:
		writer.write(sethead)
		tree.write(writer, xml_declaration=False, encoding='utf-8', method='xml')

#############################################################################################################
#This method is here to zip the files together
#Basically it creates a .zip file,
#Then it goes into the directory that was passed to it
#Then we check and see if the path we have is a directory
#If it is we put all of the files in that directory into the zipfile and call this folder Project5
#If its not... which they all are we just add it to another folder
#I couldnt get it to work without that, so that folder is just always empty
#############################################################################################################
def myzipper(system):
	myzipfile = zipfile.ZipFile("Project5.zip", 'w', zipfile.ZIP_DEFLATED)
	for curr in os.listdir(system):
		if os.path.isdir((system + curr + "/")):
			for filenext in os.listdir(system + "/" + curr):
				myzipfile.write(system + "/" + curr + "/" + filenext, "/Project5/" + curr + "/" + filenext)
		else:
			myzipfile.write(system + "/" + curr, "/nothingishere/" + curr)
	myzipfile.close()

#############################################################################################################
#Basically I wrote this next part because of gmails ineptitude
#They dont allow us to send zip files, but i can send a zip file that has been renamed to a .txt file
#I just run a command in the terminal to rename the file
#This means that the reciever has to change the file back to a .zip file to unzip it
#############################################################################################################
def changeName(zipFile):
	os.rename(zipFile, "Project5.txt")

#############################################################################################################
#This method emails the file to an email that was passed to it
#Basically I made up an email for gmail that would allow me to send an email I compose here
#I give my email credentials, followed by the name of the "zip" file we created above
#Them we open the file, then we create a message through MIME, which I found very easy to use
#Then we create a MIMEApplication with the "zip" file and a title
#Finally we log in to gmail and send the message we created
#############################################################################################################
def emailzipfile(givenemail):
	
	tommy = ""
	password = ""
	
	myZipFile = "Project5.txt"
	attach = open(myZipFile, "rb")
	
	msg = MIMEMultipart()
	msg['From'] = tommy
	msg['To'] = givenemail
	
	part = MIMEApplication(attach.read(), Name="Project5.txt")
	msg.attach(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % myZipFile)

	server = smtplib.SMTP_SSL('smtp.gmail.com',465)
	server.login(tommy, password)
	server.sendmail(tommy, givenemail, msg.as_string())
	server.close()

#############################################################################################################
#In the main method I hardcoded the files that I was using, becuase it made things much cleaner
#I declare some different useful things such as the set so when I return a set in my wordgrabber() I can keep
#the values it returned
#Then I get the wc for all of the files that we want
#I store each value in my wordcountlist
#After this I write all of the information of each file into an xml file
#I repeat this five times because we want the xml files to be distinct from eachother
#next I zip the group of files that I want to send -> the csc344 directory, this is where everything is 
#Then I rename the .zip file because of gmail being ridiculous
#Then I get the email from the user that we want to send the "zip" file to
#Then we email the "zip" file to that email 
#############################################################################################################
def main():
	wordcountlist = []
	wordlist = set()
	i = 1
	j = 0
	files = ["main.c", "main.clj", "main.scala", "main.txt", "main.py"]
	while i < 6:
		n = wordcounter("../project" + str(i) + "/" + files[j])
		wordcountlist.append(n)
		#print(int(n))
		i += 1
		j += 1

	o = 0
	while o < 5:
		xmlwriter(files, wordcountlist[o], o, wordgrabber("../project" + str(o+1) + "/" + files[o]))
		o += 1

	p = 1
	myzipper("../")
	changeName("Project5.zip")
	emailme = input("Email: ")
	emailzipfile(emailme)

#############################################################################################################
#This just make that main method we created the first executed when we python3 the file in terminal
#############################################################################################################
if __name__ == "__main__":
	main()
