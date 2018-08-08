#!/usr/bin/python

import sys
import getopt
import requests
from bs4 import BeautifulSoup
from termcolor import colored


'''
CHECKING DRUPAL
'''

def drupalFunc (data):
	drupal_version = False
	version_drupal = None
	try:

		if data.status_code == 404:
			version_drupal = None
			cms = False
			return cms, version_drupal
		drupal = data.text.find("Drupal")

		
		if data.text.find("Drupal") > 0:
			cms = True
			version_drupal = data.text[drupal+7:12]

			if version_drupal != '8.5.6':
				version_drupal = version_drupal

			else:
				version_drupal = None

		else:
			version_drupal = None
			cms = False

	except Exception as e:
		print (e)

	finally:
		return cms, version_drupal

def identify_drupal(url):
	"""FUNCTION identify_drupal"""
	response = ""
	flag = False
	try:
		urldrupal =  url + "/CHANGELOG.txt"
		response = requests.get(urldrupal)
		(flag, version_cms) = drupalFunc (response)

		if flag == False:
			urldrupal =  url + "drupal/CHANGELOG.txt"
			response = requests.get(urldrupal)
			(flag, version_cms) = drupalFunc (response)

		elif flag == False:
			urldrupal =  url + "core/CHANGELOG.txt"
			response = requests.get(urldrupal)
			(flag, version_cms) = drupalFunc (response)			

	finally:
		return flag, version_cms



'''
CHECKING HEADERS
'''

def getVulnerability(res):
	headers = res.headers
	status = None
	for header in headers:
		if header == "X-Original-URL":
			status = "X-Original-URL detected"
		elif header == "X-Rewrite-URL":
			status = "X-Rewrite-URL detected"
		
	if status is None:
		print ('\033[1;32mNot vulnerable\033[1;m')
	else:
		print ('\033[1;38m'+status+'. Vulnerable\033[1;m')

def checkDrupal(url):
	res = requests.get(url)
	if res.status_code == 200:
		getVulnerability(res)

	elif res.status_code == 401:
		print ('\033[1;34mAuth required\033[1;m')

	elif res.status_code == 500:
		print ('\033[1;33mServer error\033[1;m')

	elif res.status_code == 301:
		print ('\033[1;35mForbidden\033[1;m')

	else:
		print ('\033[1;31mURL unreachable\033[1;m')

def main(argv):
	
	inputfile = ''
	outputfile = ''

	if(len(argv) < 1):
		print('legacySymfony.py -h')
		sys.exit(2)		

	try:
		opts, args = getopt.getopt(argv,"hi:u:",["help", "ifile=", "url="])

	except getopt.GetoptError:
		print('legacySymfony.py [-i <inputfile>] [-u <url>]')
		sys.exit(2)
	
	for opt, arg in opts:
		if opt in ("-i", "--ifile"):
			inputfile = arg
			with open(inputfile) as f:
				content = f.read().splitlines()
			
			for url in content:
				try:
					flag, version_drupal = identify_drupal(url)
					print(url, end =" :: ")

					if flag:
						if(version_drupal != '8.5.6'):
							checkDrupal(url)
						else:
							print ('\033[1;32mNot vulnerable\033[1;m')	

					else:
						print ('\033[1;36mNo drupal detected\033[1;m', end =" :: ")						
						checkDrupal(url)					
					
				except:
					print(url, end =" :: ")
					print ('\033[1;31mURL unreachable\033[1;m')

		elif opt in ("-u", "--url"):
			url = arg
			try:
				flag, version_drupal = identify_drupal(url)
				print(url, end =" :: ")

				if flag:
					if(version_drupal != '8.5.6'):
						checkDrupal(url)
					else:
						print ('\033[1;32mNot vulnerable\033[1;m')	

				else:
					print ('\033[1;36mNo drupal detected\033[1;m', end =" :: ")						
					checkDrupal(url)					
				
			except:
				print(url, end =" :: ")
				print ('\033[1;31mURL unreachable\033[1;m')

		else:
			print('legacySymfony.py [-i <inputfile>] [-u <url>]')
			sys.exit()


if __name__ == "__main__":
	main(sys.argv[1:])
