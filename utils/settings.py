from dotenv import load_dotenv
import os

#Load .env file
load_dotenv()

#define environment variable
DATABASE_URL = os.getenv("DB_URL_ASYNC")
SOLR_USER = os.getenv("SOLR_USER")
SOLR_URL = os.getenv("SOLR_URL")
SOLR_PASSWORD = os.getenv("SOLR_PASSWORD")

# Mapping from type to prefix and template
CRKN_PREFIX_TEMPLATE_MAPPING = {
    'generic': ('g', 'reedeedeedk'),
    'canvas': ('c', 'reedeedeedk'),
    'canvases': ('c', 'reedeedeedk'),
    'collection': ('s', 'reedeedeedk'),
    'collections': ('s', 'reedeedeedk'),
    'manifest': ('m', 'reedeedeedk'),
    'manifests': ('m', 'reedeedeedk'),
}