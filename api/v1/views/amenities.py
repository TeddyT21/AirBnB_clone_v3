#!/usr/bin/python3
"""Objects that handles all default RestFul API actions for Amenities"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/all_amenities.yml')
def get_amenities():
    """
    Retrieves a list of all amenities

    Returns:
        A JSON representation of all amenities in the storage.
    """
    all_amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in all_amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/amenity/get_amenity.yml', methods=['GET'])
def get_amenity(amenity_id):
    """ Retrieves an amenity by ID.

    Args:
        amenity_id: The ID of the amenity to retrieve.

    Returns:
        A JSON representation of the amenity with the given ID, or a 404 error
        if the amenity does not exist.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/amenity/delete_amenity.yml', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Delete an amenity by ID.

    Args:
        amenity_id: The ID of the amenity to delete.

    Returns:
        An empty JSON response with status code 200 if the amenity is deleted
        successfully, or a 404 error if the amenity does not exist.
    """

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/amenity/post_amenity.yml', methods=['POST'])
def post_amenity():
    """
    Create a new amenity.

    Returns:
        A JSON representation of the new amenity with status code 201 if the
        amenity is created successfully, or a 400 error if the request is not
        in JSON format or is missing the required 'name' field.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Amenity(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/amenity/put_amenity.yml', methods=['PUT'])
def put_amenity(amenity_id):
    """
    Updates an amenity
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
