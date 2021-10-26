from __future__ import print_function
from core.config.config import configuration
from core.database.database import database
from core.webpage.webpage import webpage
from core.parser.parse import parser
from core.api.api import api
from datetime import datetime
from time import sleep
from sys import exit
import os

__version__ = 2.3

class theater:
	def __init__(self):
		self.api = api()
		self.parser = parser()
		self.webpage = webpage()
		self.database = database()
		self.config = configuration()
		self.directories = self.config.path()
		self.unsantizedFiles = []

	def wait(self):
		# Function to wait for 'x' seconds, the delay is
		# set in config file
		seconds = int(self.config.interval())
		if seconds:
			sleep(seconds)

	def maintenance(self, verbose=True):
		# Start
		print("[{date}] Maintenance started".format(date=datetime.now()))

		# Parse all files in database and check if they
		# still exists on disk. If False, we delete it from
		# the database
		databaseData = self.database.getData()
		if databaseData:
			for x in databaseData:
				if os.path.isfile(x[0]):
					if verbose:
						print("[{date}] File exists: {file}".format(date=datetime.now(), file=x[0]))
				else:
					if self.database.delete(x[0]) == True:
						if verbose:
							print("[{date}] Successfully deleted ({file}) from database".format(date=datetime.now(), file=x[0]))
					else:
						if verbose:
							print("[{date}] Unable to delete ({file}) from database".format(date=datetime.now(), file=x[0]))
		
		# End
		print("[{date}] Maintenance finished".format(date=datetime.now()))

	def start(self):
		# Start
		print("[{date}] MovieTheater started".format(date=datetime.now()))

		# Parse files inside directories
		self.parser.file_names = []
		self.unsantizedFiles = []

		if self.directories:
			for directory in self.directories:
				self.unsantizedFiles = self.parser.files(directory)
		else:
			exit("[{date}] There's no files to process, exiting!".format(date=datetime.now()))

		# Exit if there's no files to enumerate
		if not self.unsantizedFiles:
			exit("[{date}] There's no files to process, exiting!".format(date=datetime.now()))

		# Enumerate files and sanitize the file names
		for index, unsantizedFile in enumerate(self.unsantizedFiles, start=1):
			# Parse file name for title and year etc.
			parsedData = self.parser.parse(unsantizedFile[1], standardise=False)
			if not parsedData:
				print("[{date}] Unable to parse file name - File name: {file}".format(date=datetime.now(), file=unsantizedFile[1]))

			# Check if the file already exist in database
			searchDatabase = self.database.ifFilePathExist(os.path.join(unsantizedFile[0], unsantizedFile[1]))
			if searchDatabase == True:
				print("[{date}] Already exist in database - Title: {title}".format(date=datetime.now(), title=parsedData["title"].capitalize()))
			else:
				# Gather information about the file
				try:
					getInfo = self.api.info(parsedData["title"], parsedData["year"])
				except KeyError:
					getInfo = self.api.info(parsedData["title"], "")

				# Catch error on file names that does not contain a resolution
				# or if they have like 'uhd' or '4k' instead of 2160p.
				#
				# Todo:
				#   * When "n/a" is set, we can try use ctypes to check the files
				#     dimentions and figure out the resolution.
				try:
					resolution = parsedData["resolution"]
					if "uhd" in resolution.lower():
						resolution = "2160p"
					if "4k" in resolution.lower():
						resolution = "2160p"
				except KeyError:
					resolution = "n/a"

				# Add information to database with either limited information or
				# complete information
				if getInfo == False:
					insertData = self.database.insertData(os.path.join(unsantizedFile[0], unsantizedFile[1]),
															parsedData["title"].capitalize(), "n/a", "n/a", "n/a","n/a",
															"n/a", "n/a", "n/a", "n/a", "n/a", "n/a")
					if insertData == True:
						print("[{date}] Added to database with limited information - Title: {title}".format(date=datetime.now(),
										title=parsedData["title"].capitalize()))
					elif insertData == False:
						print("[{date}] Error while adding to database with information - Title: {title}".format(date=datetime.now(),
										title=parsedData["title"].capitalize()))
					elif insertData == "Exist":
						print("[{date}] Already exist in database with limited information - Title: {title}".format(date=datetime.now(),
										title=parsedData["title"].capitalize()))
				else:
					insertData = self.database.insertData(os.path.join(unsantizedFile[0], unsantizedFile[1]),
															getInfo["Title"], getInfo["Year"], getInfo["imdbRating"],
															getInfo["Genre"], getInfo["Plot"], getInfo["Poster"],
															getInfo["imdbID"], getInfo["Trailer_url"],
															resolution, getInfo["Actors"], getInfo["Runtime"])
					if insertData == True:
						print("[{date}] Added to database - Title: {title}".format(date=datetime.now(),
										title=getInfo["Title"], year=getInfo["Year"]))
					elif insertData == False:
						print("[{date}] Error while adding to database - Title: {title}".format(date=datetime.now(),
										title=getInfo["Title"], year=getInfo["Year"]))
					elif insertData == "Exist":
						print("[{date}] Already exist in database - Title: {title} - Year: {year}".format(date=datetime.now(),
										title=getInfo["Title"], year=getInfo["Year"]))

		# Delete the webpage so we can create a new
		self.webpage.delete()

		# Parse all the data in database and add it to the webpage as a column
		# inside the HTML class: <div class="row"></div>
		#
		# Remarks:
		# 	* If the webpage is not deleted before, the columns will end up
		#     in the bottom of the page, non alphabetical order.
		databaseData = self.database.getData()
		if databaseData:
			for index, data in enumerate(databaseData, start=1):
				insertColumn = self.webpage.insertColumn(index, data[0], data[1], data[2],
												data[3], data[4], data[5], data[6], data[7],
												data[8], data[9], data[10], data[11])
				if insertColumn == True:
					print("[{date}] Added to webpage - Title: {title}".format(date=datetime.now(), title=data[1]))
				elif insertColumn == False:
					print("[{date}] Error while adding to webpage - Title: {title}".format(date=datetime.now(), title=data[1]))
				elif insertColumn == "Exist":
					print("[{date}] Already exist in webpage - Title: {title}".format(date=datetime.now(), title=data[1]))
		else:
			exit("[{date}] Unable to create webpage because there's no data in database, exiting!".format(date=datetime.now()))

		# End
		print("[{date}] MovieTheater finished".format(date=datetime.now()))

if __name__ == "__main__":
	theater = theater()

	print("[{date}] Version: {version}".format(date=datetime.now(),
			version=__version__))

	try:
		while True:
			theater.maintenance()
			theater.start()
			theater.wait()
	except KeyboardInterrupt:
		exit("[{date}] Exited, keyboard (CTRL+C) interruption".format(date=datetime.now()))