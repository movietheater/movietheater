from configparser import ConfigParser
from os.path import join
from os import getcwd, name

class configuration:
	""" Handles the configuration file and settings """
	def __init__(self):
		self.file = join(getcwd(), "config.ini")
		self.config = ConfigParser()

	def update(self, section, key, value):
		if self.config.read(self.file):
			self.config[section][key] = value
			with open(self.file, "w") as configfile:
				self.config.write(configfile)
			return True
		else:
			return False

	def path(self):
		if self.config.read(self.file):
			return(self.config["DIRECTORY"]["path"].split(", "))
		else:
			return False

	def omdbapiKey(self):
		if self.config.read(self.file):
			return(self.config["API"]["omdbapi"])
		else:
			return False

	def interval(self):
		if self.config.read(self.file):
			return(self.config["INTERVAL"]["time"])
		else:
			return False

	def webpagePath(self):
		if self.config.read(self.file):
			return(self.config["WEBPAGE"]["path"])
		else:
			return False

	def databasePath(self):
		if self.config.read(self.file):
			return(self.config["DATABASE"]["path"])
		else:
			return False