from core.config.config import configuration
import sqlite3
import os

class database:
	def __init__(self):
		self.config = configuration()
		self.path = self.config.databasePath()

	def createTable(self):
		""" Create table and return True if created and False if already exists """
		try:
			connect = sqlite3.connect(os.path.join(self.path, "database.db"))
		except Exception as error:
			return False
		else:
			try:
				connect.execute("""CREATE TABLE MOVIES(FILE_PATH TEXT, TITLE TEXT,
									YEAR TEXT, IMDB_RATING TEXT, GENRE TEXT, PLOT TEXT,
									POSTER TEXT, IMDBID TEXT, TRAILER_URL TEXT,
									RESOLUTION TEXT, ACTORS TEXT, LENGTH TEXT);""")
			except Exception as error:
				return False
			else:
				connect.commit()
				return True
			finally:
				connect.close()

	def insertData(self, *args):
		""" Insert data into MOVIES table """
		self.createTable() # Creates table if it does not exist

		try:
			connect = sqlite3.connect(os.path.join(self.path, "database.db"))
		except Exception as error:
			return False
		else:
			cursor = connect.cursor()

		try:
			cursor.execute("""INSERT INTO MOVIES (FILE_PATH, TITLE, YEAR, IMDB_RATING, GENRE, PLOT, POSTER,
							IMDBID, TRAILER_URL, RESOLUTION, ACTORS, LENGTH) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
								(args[0], # File path
								args[1], # Title
								args[2], # Year
								args[3], # Imdb rating
								args[4], # Genre
								args[5], # Plot
								args[6], # Poster
								args[7], # ImdbID
								args[8], # Trailer URL
								args[9], # Resolution
								args[10], # Actors
								args[11])) # Length
			connect.commit()
		except sqlite3.IntegrityError as error:
			return("Exist")
		except Exception as error:
			return False
		else:
			return True
		finally:
			connect.close()

	def getData(self):
		""" Search and return all available data in database """
		#print(self.path)
		try:
			connect = sqlite3.connect(os.path.join(self.path, "database.db"))
			cursor = connect.cursor()
		except Exception as error:
			return False
		else:
			try:
				# Retrieve all the data inside database but sort titles asc
				cursor.execute("SELECT * FROM MOVIES order by TITLE asc")
			except Exception:
				return False
			else:
				return(cursor.fetchall())
			finally:
				connect.close()
	
	def ifTitleExist(self, title):
		""" Checks if title exist in database """
		#print(title)

		try:
			connect = sqlite3.connect(os.path.join(self.path, "database.db"))
		except Exception as error:
			return False
		else:
			try:
				titles = connect.execute("SELECT TITLE from MOVIES")
			except sqlite3.OperationalError:
				pass
			else:
				for t in titles:
					if title.lower() in t[0].lower():
						return True
			finally:
				connect.close()

	def ifFilePathExist(self, file_path):
		""" Checks if file path exist in database """
		try:
			connect = sqlite3.connect(os.path.join(self.path, "database.db"))
		except Exception as error:
			return False
		else:
			try:
				file_paths = connect.execute("SELECT FILE_PATH from MOVIES")
			except sqlite3.OperationalError:
				pass
			else:
				for fp in file_paths:
					if file_path in fp[0]:
						return True
			finally:
				connect.close()

	def delete(self, file_path):
		""" Deletes a file and its information from database """
		try:
			connect = sqlite3.connect(os.path.join(self.path, "database.db"))
		except Exception as error:
			return False
		
		try:
			file_paths = connect.execute("DELETE FROM MOVIES WHERE FILE_PATH='{}'".format(file_path))
		except sqlite3.OperationalError:
			pass
		else:
			connect.commit()
			connect.close()
			return True