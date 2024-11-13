#!/usr/bin/python3
""" index module """

from flask import abort
from api.v1.views import app_views


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized():
    abort(401)
