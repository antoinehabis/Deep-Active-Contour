from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from config import *
import logging

import sys
from argparse import ArgumentParser
from shapely import wkt
from shapely.affinity import affine_transform

from cytomine import Cytomine
from cytomine.models import AnnotationCollection, ImageInstanceCollection
from cytomine.models import TermCollection

__author__ = "Rubens Ulysse <urubens@uliege.be>"


def get_by_id(haystack, needle):
    return next((item for item in haystack if item.id == needle), None)


pb_key = 'd6081ae5-ba45-4e52-bf37-791adcba141d'
pv_key = '23a5bdd8-e7c8-4546-a560-cf341a92fe8e'
host = 'https://bigpicture.demo.cytomine.com/'

logging.basicConfig()
logger = logging.getLogger("cytomine.client")
logger.setLevel(logging.INFO)

project_id = '2578438'

with Cytomine(host=host,
              public_key=pb_key,
              private_key=pv_key) as cytomine:
    
    terms = TermCollection().fetch_with_filter("project", project_id)
    terms_dict = {t.id:t.name for t in terms}
    image_instances = ImageInstanceCollection().fetch_with_filter("project", project_id)
    dic_id_img = {}
    for image in image_instances:
        dic_id_img[image.id] = image.filename.split('/')[-1]
    # We want all annotations in a given project.
    annotations = AnnotationCollection()
    annotations.project = project_id  # Add a filter: only annotations from this project
    # You could add other filters:
    # annotations.image = id_image => Add a filter: only annotations from this image
    # annotations.images = list(dic_id_img.keys()) 
    # annotations.user = id_user => Add a filter: only annotations from this user
    # ...
    annotations.showWKT = True  # Ask to return WKT location (geometry) in the response
    annotations.showMeta = True  # Ask to return meta information (id, ...) in the response
    annotations.showGIS = True  # Ask to return GIS information (perimeter, area, ...) in the response
    annotations.showTerm = True
    # ...
    # => Fetch annotations from the server with the given filters.
    annotations.fetch()

df  = pd.DataFrame(columns= ['id', 'image', 'project','term', 'area','perimeter','location'])

for annotation in annotations:
    if len(annotation.term)>0:

        df = df.append({'id':annotation.id,
                        'image':dic_id_img[annotation.image],
                        'project': annotation.project,
                        'term': terms_dict[annotation.term[0]],
                        'area':annotation.area,
                        'perimeter':annotation.perimeter,
                        'location':annotation.location},
                        ignore_index = True)
df = df[~df['image'].isin(['20077.svs', '20214.svs', '20209.svs','20211.svs','20180.svs','20189.svs', '20215.svs', '20119.svs', '20185.svs'])]
df.to_csv(os.path.join(path_annotations,'annotations.csv'))