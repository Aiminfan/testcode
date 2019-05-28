# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:58:46 2019

@author: aimin.fan
"""
DOMAIN = {'Address': {}}
# Let's just use the local mongod instance. Edit as needed.

# Please note that MONGO_HOST and MONGO_PORT could very well be left
# out as they already default to a bare bones local 'mongod' instance.
MONGO_HOST = 'localhost'
MONGO_PORT = 27017

## Skip this block if your db has no auth. But it really should.
#MONGO_USERNAME = '<your username>'
#MONGO_PASSWORD = '<your password>'
## Name of the database on which the user can be authenticated,
## needed if --auth mode is enabled.
#MONGO_AUTH_SOURCE = '<dbname>'

MONGO_DBNAME = 'dbGIS'

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
schema = {
    # An embedded 'strongly-typed' dictionary.
    'attributes': {
        'type': 'dict',
        'schema': {
            'ADDRESS': {'type': 'string'},
            'FID': {'type': 'string'},
        },
    },
    'geometry': {
        'type': 'dict',
        'schema': {
            'x': {'type': 'float',
                  'min':-180, 
                  'max':180,
                  },
            'y': {'type': 'float',
                  'min':-90, 
                  'max':90,
                  }
        },
    },
    'Precision': {
        'type': 'float',
    },
    'Accuracy': {
        'type': 'float',
    },
    'MatchLevel': {
        'type': 'float', 
        'max':9,
    },
}
address = {
    # 'title' tag used in item links. Defaults to the resource title minus
    # the final, plural 's' (works fine in most cases but not for 'people')
    'item_title': 'Addr',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/people/<lastname>'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'attributes.ADDRESS'
    },

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],

    'schema': schema
}