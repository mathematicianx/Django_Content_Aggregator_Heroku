# Django_Content_Aggregator_Heroku

Content agregator page made in Django.
It uses a webscraper which connects to few local pages (local newspapers, news pages and local city hall) to extract latest news.
It also scrapes two local cinemas extracting which movies premiere at current day and what are the premiere dates.
It also uses Filmweb API written by lopezloo go get filmweb score and display it next to movie title.

There is also a basic webforum for local discussions and local advert board.
Using forum and ads is free, but login is required.


* Heroku Scheduler for running webscraper,
* Amazon AWS S3 for storing media,
* whitenoise for serving static files,
* TinyMCE for better input in forms,
* FilmwebAPI written by lopezloo for movie score,
* thumbnail-SORL for handling images and scaling them for forum avatars and advert miniatures,
* REST api for accessing data from scraped news and inputing/updating/deleting new data from JSON file for authorized users (GET/POST/UPDATE/DELETE)
