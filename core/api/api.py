from core.config.config import configuration
from json import loads, JSONDecoder
from urllib.parse import quote_plus
from shutil import copyfileobj
from requests import get
from time import sleep
import os

class api:
	def __init__(self):
		self.config = configuration()
		self.key = self.config.omdbapiKey()
		self.webpagePath = self.config.webpagePath()
		self.useragent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
							AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}

	def parse(self, text, decoder=JSONDecoder()):
		"""
		Find JSON objects in text, and yield the decoded JSON data. Does not attempt
		to look for JSON arrays, text, or other JSON types outsideof a parent
		JSON object.

		https://stackoverflow.com/questions/54235528/how-to-find-json-object-in-text-with-python
		"""
		position = 0

		while True:
			match = text.find("{", position)
			if match == -1:
				break
			try:
				result, index = decoder.raw_decode(text[match:])
				yield result
				position = match + index
			except ValueError:
				position = match + 1

	def url(self, imdbID):
		# List of trailer URLs
		trailer = []

		# Make a request to IMDB and collect HTML data
		try:
			data = get("https://www.imdb.com/title/{imdbID}".format(imdbID=imdbID), headers=self.useragent, timeout=25)
		except Exception:
			return False
		else:
			# Parse the html data and pass it to parse function in order
			# to convert data into dict
			parsedData = self.parse(data.text)
			if parsedData:
				for result in parsedData:
					if result:
						# Try the embedded one first since it's being used
						# on all new trailers
						try:
							trailer_url = "https://imdb.com/" + result["trailer"]["embedUrl"] + "/imdb/embed"
						except KeyError:
							pass
						else:
							try:
								data = get(trailer_url, headers=self.useragent, timeout=25)
							except Exception as error:
								return False
							
							# Remove imdb/embed from URL and try again if the
							# trailer is not found
							if "This video is not available" in data.text:
								try:
									trailer_url = "https://imdb.com/" + result["trailer"]["embedUrl"]
								except KeyError:
									pass
								else:
									try:
										data = get(trailer_url, headers=self.useragent, timeout=25)
									except Exception as error:
										return False
									else:
										if "This video is not available" in data.text:
											return False
			else:
				return False

		# Parse and bruteforce until we find the ".mp4" URL inside
		# HTML data and return it to function
		try:
			data = get(trailer_url, headers=self.useragent, timeout=25)
		except Exception as error:
			return False
		else:
			for result in self.parse(data.text):
				# For older movies the HTML data can be different
				try:
					x = self.parse(result["playbackData"][0])
					for c in x:
						url = c["videoLegacyEncodings"][1]["url"]
						if url:
							trailer.append(url)
				except:
					pass

				# For newer movies
				try:
					url = result["videoPlayerObject"]["video"]["videoInfoList"][1]["videoUrl"]
				except KeyError:
					pass
				except IndexError:
					try:
						url = result["videoPlayerObject"]["video"]["videoInfoList"][0]["videoUrl"]
					except KeyError:
						pass
					except IndexError:
						return False
					else:
						trailer.append(url)
				else:
					trailer.append(url)

		# Check if we have anything in list, if so return
		# the first URL in list
		if trailer:
			return trailer[0]
		else:
			return None

	def downloadTrailer(self, imdbID, url):
		""" Downloads trailer to disk """
		if os.path.isdir(os.path.join(self.webpagePath, "trailers")) == False:
			try:
				os.mkdir(os.path.join(self.webpagePath, "trailers"))
			except Exception as error:
				return False

		if os.path.isdir(self.webpagePath) == True:
			filename = os.path.join(os.path.join(self.webpagePath, "trailers"), "{imdbID}.mp4".format(imdbID=imdbID))
			if os.path.isfile(filename) == True:
				return filename
			else:
				with get(url, stream=True, timeout=120) as data:
					with open(filename, "wb") as file:
						copyfileobj(data.raw, file)

			if os.path.isfile(filename):
				return filename
			else:
				False

	def info(self, title, year):
		""" Gather information about the title and download trailer from IMDB """
		if not self.key:
			return False
		else:
			try:
				html = get("http://www.omdbapi.com/?apikey={key}&t={title}&y={year}".format(key=self.key,
								title=quote_plus(str(title)), year=year), timeout=30)
			except Exception as error:
				return False

		json = loads(html.content)
		if json["Response"] == "False":
			return False

		trailerUrl = self.url(json["imdbID"])
		if trailerUrl:
			result = self.downloadTrailer(json["imdbID"], trailerUrl)
			if result:
				json["Trailer_url"] = result
				return json
			else:
				json["Trailer_url"] = "n/a"
				return json
		else:
			json["Trailer_url"] = "n/a"
			return json