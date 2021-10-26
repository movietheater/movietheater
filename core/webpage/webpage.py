from core.config.config import configuration
from os.path import isfile, join
from os import remove, name
from requests import get
from time import sleep
import os

"""
TODO

 [] Change the modal background-color to little bit darker so it looks better
    when searching for a specific movie and opens the modal up.

 [] When a trailer is played and the end-user press on the Watch trailer again, hide
    the video and pause it.
	
 [] Add following code when either  pressing button 'Watch Movie' or
    'Watch Trailer'
 
	<div class="spinner-border text-light" role="status">
	  <span class="sr-only">Loading...</span>
	</div>
"""

class template:
	html = """<!DOCTYPE html>
<html>
<head>
<title>MovieTheater</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
<link rel="stylesheet" href="css.css"/>

<script type="text/javascript">
$(function(){
    $('.modal').modal({
        show: false
    }).on('hidden.bs.modal', function(){
        $(this).find('video')[0].pause();
    });
});

$(document).ready(function(){
  $("#inputSearch").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $(".column").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});
</script>

</head>
<body>

<div class="searchArea">
	<div class="input-icons">
		<i class="fa fa-search"></i>
		<input id="inputSearch" class="input-field" type="text" placeholder="Search...">
	</div>
</div>

<div class="content"> 
<!-- column -->
</div>
</body>
<script type="text/javascript">
$(".watchButtonTrailer").click(function(){
      $(this).next().toggle();
});
</script>
</html>"""

	css = """* {
	box-sizing: border-box;
}

a:hover, a:visited, a:link, a:active
{
	color: white;
    text-decoration: none;
}

h1 {
	color: #e3ceb3;
}

strong {
	color: #e3ceb3;
	font-size: 16px;
}

p {
	color: #e3ceb3;
	font-size: 16px;
}

body {
	margin: 0;
	font-family: Calibri;
	background-color: #121012;
    max-width: 100%;
    overflow-x: hidden;
	padding-top: 10px;
	padding-left: 20px;
	padding-right: 20px;
	padding-bottom: 20px;
}

/* width */
::-webkit-scrollbar {
	width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
	background: #f1f1f1; 
}
 
/* Handle */
::-webkit-scrollbar-thumb {
	background: #888; 
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
	background: #555; 
}

::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
	color: #e3ceb3;
	opacity: 1; /* Firefox */
}

:-ms-input-placeholder { /* Internet Explorer 10-11 */
	color: #e3ceb3;
}

::-ms-input-placeholder { /* Microsoft Edge */
	color: #e3ceb3;
}

.header {
	text-align: center;
	padding: 32px;
}

.content {
	display: -ms-flexbox; /* IE10 */
	display: flex;
	-ms-flex-wrap: wrap; /* IE10 */
	flex-wrap: wrap;
	padding: 0 4px;
}

.modal-content {
	opacity: 1;
	border-radius: 0px;
	background-color: #121012;
	padding-right: 25px;
	padding-left: 25px;
	padding-top: 25px;
	padding-bottom: 25px;
	margin: 10vh auto 0px auto;
}

.modal-backdrop {
	will-change: transform;
	backdrop-filter: blur(30px);
	background-color: #00000000;
}

.modal-backdrop.in {
	will-change: transform;
	opacity: 0.9 !important;
}

img#image {
	transform: translateZ(0); /*for older browsers*/
	will-change: transform;
}

/* Create four equal columns that sits next to each other */
.column {
	-ms-flex: 12.5%; /* IE10 */
	flex: 12.5%;
	max-width: 12.5%;
	padding: 0 4px;
} 

.column img {
	margin-top: 8px;
	vertical-align: middle;
	width: 100%;
	height: 98%;
	border-radius: 15px;
	transform: translateZ(0); /*for older browsers*/
	will-change: transform;	
}

@media screen and (max-width: 800px) {
	.column {
	-ms-flex: 50%;
	flex: 50%;
	max-width: 50%;
  }
}

@media screen and (max-width: 600px) {
	.column {
	-ms-flex: 100%;
	flex: 100%;
	max-width: 100%;
  }
}

.watchButtonMovie {
	box-shadow: inset 0px 1px 0px 0px #d6913c;
	background: linear-gradient(to bottom, #d6913c 5%, #a6702d 100%);
	background-color: #d6913c;
	display: inline-block;
	cursor: pointer;
	font-family: Arial;
	font-size: 13px;
	font-weight: bold;
	padding: 12px 76px;
	text-decoration: none;
	width: 100%;
	height: 100%;
	margin-top: 10px;
	margin-bottom: 10px;
}

.watchButtonMovie:hover {
	background:linear-gradient(to bottom, #d6913c 5%, #d6913c 100%);
	background-color: #d6913c;
}

.watchButtonMovie:active {
	position:relative;
	top:1px;
}

.watchButtonTrailer {
	box-shadow: inset 0px 1px 0px 0px #6b6b6b;
	background: linear-gradient(to bottom, #6b6b6b 5%, #525252 100%);
	background-color: #525252;
	display: inline-block;
	cursor: pointer;
	font-family: Arial;
	font-size: 13px;
	font-weight: bold;
	padding: 12px 76px;
	text-decoration: none;
	width: 100%;
	height: 100%;
	margin-top: 10px;
	margin-bottom: 10px;
}

.watchButtonTrailer:hover {
	background:linear-gradient(to bottom, #6b6b6b 5%, #525252 100%);
	background-color: #6b6b6b;
}

.watchButtonTrailer:active {
	position:relative;
	top:1px;
}

.video {
	outline:none;
}

.searchArea {
	overflow: hidden;
}

.input-icons i {
	position: absolute;
	padding-top: 10px;
	padding-left: 10px;
}
          
.input-icons {
	width: 100%;
	margin-top: 10px;
	margin-bottom: 10px;
	color: #4f464f;
}
          
.icon {
	padding: 10px;
	min-width: 40px;
}
          
.input-field {
	width: 100%;
	padding-top: 10px;
}

input {
	width: 100%;
	padding-top: 10px;
	padding-bottom: 10px;
	padding-left: 10px;
	border: 0;
}

input[type=text] {
	background-color: #262226;
	color: #e3ceb3;
	background-position: 10px 10px;
	background-repeat: no-repeat;
	padding-left: 30px;
}

textarea:focus, input:focus{
	outline: none;
}

.statsWrapper {
	padding-bottom: 55px;
}

.imdb {
  border-radius: 5px 5px 5px 5px;
  text-align: center;
  color: black;
  padding: 5px 5px 25px 5px;
  width: 80px;
  height: 10px;
  background-image: linear-gradient(#ebbc14, #e6ac19); 
  margin-bottom: 10px;
  float:left;
}

.resolution {
  border-radius: 5px 5px 5px 5px;
  text-align: center;
  color: black;
  padding: 5px 5px 25px 5px;
  width: 80px;
  height: 10px;
  background-image: linear-gradient(#bfbfbf, #949494);
  margin-bottom: 10px;
  margin-left: 10px;
  float:left;
}

.length {
  border-radius: 5px 5px 5px 5px;
  text-align: center;
  color: black;
  padding: 5px 5px 25px 5px;
  width: 95px;
  height: 10px;
  background-image: linear-gradient(#bfbfbf, #949494);
  margin-bottom: 10px;
  margin-left: 10px;
  float:left;
}

imdbFont {
  font-family: Impact;
  font-size: 14px;
}

imdbScore {
  font-family: Calibri;
  font-weight: bold;
  padding-left: 5px;
  font-size: 14px;
}

resolution {
  font-family: Calibri;
  font-weight: bold;
  font-size: 14px;
}

length {
  font-family: Calibri;
  font-weight: bold;
  font-size: 14px;
}

bInfo {
  font-family: Calibri;
  font-weight: bold;
  font-size: 14px;
  color: #716759;
}

bInfoText {
  font-family: Calibri;
  font-weight: normal;
  font-size: 14px;
  color: #716759;
}
"""

	column = """<div class="column">
	<a href="#{index}" data-toggle="modal" data-target="#modal{index}">
		<img src="{poster}" style="width:100%">
	</a>
	<div id="modal{index}" class="modal">
	  <div class="modal-dialog modal-lg" tabindex="-1">
		<div class="modal-content">
			<h1>{title} ({year})</h1>
			<div class="statsWrapper">
				<div class="imdb"><imdbFont>IMDb </imdbFont><imdbScore>{rating}</imdbScore></div>
				<div class="resolution"><i class="fa fa-desktop" aria-hidden="true"></i><resolution> {resolution}</resolution></div>
				<div class="length"><i class="fa fa-clock-o" aria-hidden="true"></i><length> {length}</length></div>
			</div>
			<p>{plot}</p>
			<div class="genre_actors">
				<p><bInfo>Genre:</bInfo><bInfoText> {genre}</bInfoText></p>
				<p><bInfo>Actors:</bInfo><bInfoText> {actors}</bInfoText></p>
			</div>
			<a href="ovlc://{filepath}" class="watchButtonMovie"><center><i class="fa fa-play-circle fa-lg" aria-hidden="true"></i> Movie</center></a>
			<a href="#{index}" class="watchButtonTrailer"><center><i class="fa fa-play-circle fa-lg" aria-hidden="true"></i> Trailer</center></a>
			<div style="display: none;">
				<p><strong>Trailer:</strong></p> 
				<video class="video" width="100%" height="100%" controls>
					<source src="{trailer_url}" type="video/mp4">
				</video>
			</div>		
		<a href="#" rel="modal:close"></a>
		</div>
	  </div>
	</div>	
</div>
<!-- column -->"""

class webpage:
	def __init__(self):
		self.config = configuration()
		self.path = self.config.webpagePath()

	def delete(self):
		""" Deletes the 'index.html' file from disk """
		try:
			os.remove(os.path.join(self.path, "index.html"))
			os.remove(os.path.join(self.path, "css.css"))
		except Exception:
			return False
		else:
			return True

	def ifExists(self, string):
		""" Function to verify if the name already exist, returns
		True if exist and False if not """
		try:
			with open(os.path.join(self.path, "index.html"), "rt") as file:
				data = file.read()
		except Exception:
			return False
		else:
			if string in data:
				return True
			else:
				return False

	def insertColumn(self, index, file_path, title, year, rating, genre, plot, poster, imdbid, trailer_url, resolution, actors, length):
		# If the webpage is not created yet, create it
		if self.ifExists("<!DOCTYPE html>") == False:
			try:
				with open(os.path.join(self.path, "index.html"), "w") as file:
					file.write(template.html)
			except Exception as error:
				return False

		# If the CSS is not created yet, create it
		if os.path.isfile(os.path.join(self.path, "css.css")) == False:
			try:
				with open(os.path.join(self.path, "css.css"), "w") as file:
					file.write(template.css)
			except Exception as error:
				return False

		# Open file and read file data
		try:
			with open(os.path.join(self.path, "index.html"), "rt") as file:
				data = file.read()
		except Exception as error:
			return False

		# Check if file already exist in webpage
		if self.ifExists(os.path.basename(file_path)) == True:
			return "Exist"

		# If trailer URL is not 'n/a' modify the trailer path
		# in order to get it work when added to webpage
		if trailer_url == "n/a":
			pass
		elif "http" in trailer_url:
			pass
		else:
			split = os.path.split(trailer_url)
			trailer_url = os.path.join("trailers", split[1])

		# If there's no poster we will just add a empty stock photo
		# borrowed from IMDB
		if poster == "n/a":
			poster = "https://m.media-amazon.com/images/G/01/imdb/images/nopicture/180x268/film-173410679._CB468515592_.png"
		else:
			poster = poster

		# Add a row to webpage containing the file information
		try:
			data = data.replace("<!-- column -->",
								template.column.format(index=index,
								filepath=file_path.replace("\\", "/"),
								title=title,
								year=year,
								rating=rating,
								genre=genre,
								plot=plot,
								poster=poster,
								trailer_url=trailer_url,
								resolution=resolution,
								actors=actors,
								length=length))
		except Exception as error:
			return False

		# Write changes to webpage
		try:
			with open(os.path.join(self.path, "index.html"), "wt") as file:
				file.write(data)
		except Exception as error:
			return False
		else:
			return True