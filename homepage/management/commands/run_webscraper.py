import os
current_dir = os.getcwd()
x = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))
y = os.path.dirname(os.path.dirname(current_dir))

scraper_abs_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'custom_webscraper.py')
print(scraper_abs_path)

