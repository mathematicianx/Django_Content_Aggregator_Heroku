# Django_Content_Aggregator_Heroku

LIVE version can be viewed here: http://olawa-agregator.herokuapp.com/

Content agregator page made in Django.
It uses a webscraper(requests, BS4) which connects to few local pages (local newspapers, news pages and local city hall) to extract latest news.
It also scrapes two local cinemas extracting which movies premiere at current day and what are the premiere dates.
It also uses Filmweb API written by lopezloo to get filmweb score and display it next to movie title. If there are no premieres at that day then the appropiate message is displayed.

There is also a basic webforum for local discussions and local advertisement board.
Using forum and ads is free, but login is required.


-Heroku Scheduler for running webscraper,
-Amazon AWS S3 for storing media,
-whitenoise for serving static files,
-TinyMCE for better input in forms,
-FilmwebAPI written by lopezloo for movie score,
-thumbnail-SORL for handling images and scaling them for forum avatars and advert miniatures, 
