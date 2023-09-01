from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import sys
from argparse import ArgumentParser

from shapely.geometry import Point, box

from cytomine import Cytomine
from cytomine.models import Property, Annotation, AnnotationTerm, AnnotationCollection

__author__ = "Rubens Ulysse <urubens@uliege.be>"

logging.basicConfig()
logger = logging.getLogger("cytomine.client")
logger.setLevel(logging.INFO)

def delete_annotations(id_image ,id_project):

    pb_key = 'd6081ae5-ba45-4e52-bf37-791adcba141d'
    pv_key = '23a5bdd8-e7c8-4546-a560-cf341a92fe8e'
    host = 'https://bigpicture.demo.cytomine.com/'
    
    with Cytomine(host=host, public_key=pb_key, private_key=pv_key) as cytomine:

        # Get the list of annotations
        annotations = AnnotationCollection()
        annotations.image = id_image
        annotations.project =id_project
        annotations.fetch()
        for annotation in annotations:
            annotation.delete()
    return 'You deleted all the annnotations'