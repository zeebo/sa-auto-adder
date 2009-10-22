from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import urls
import logging

application = webapp.WSGIApplication(urls.urls.build_url_list(), debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()