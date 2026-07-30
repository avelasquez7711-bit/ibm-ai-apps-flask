from flask import Flask, make_response, request

# create instance of Flask class, passing name of current module
app = Flask(__name__)

# client data
data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    },
]


# define route for root URL ("/")
@app.route("/")
def index():
    # function handles requests to root URL
    # return plain text response
    return "hello world"


# define route for '/no_content' URL
@app.route("/no_content")
def no_content():
    # return dictiornary with message and 204 No Content code
    return ({"message": "No content found"}, 204)


# define route for '/exp' URL
@app.route("/exp")
def index_explicit():
    # create response object
    resp = make_response({"message": "Hello world"})
    resp.status_code = 200  # set status code to 200

    return resp


# define route for '/data' URL
@app.route("/data")
def get_data():
    try:
        # check if data exists and has len > 0
        if data and len(data) > 0:
            # return JSON response with message showing data len
            return {"message": f"Data of length {len(data)} found"}
        else:
            # return JSON response with 500 status code if data is empty
            return {"message": "Data is empty"}
    except NameError:
        # return JSON response with 404 status code if data is not defined
        return ({"message": "Data not found"}, 404)


# define route for '/name_search' URL
@app.route("/name_search")
def name_search():
    """find person in database

    returns:
        json: person if found with status of 200
        400: if arg 'q' is missing from request
        422: if arg 'q' is invalid
        404: if person not found in data
    """
    # get arg 'q' from query params. of reuqest
    query = request.args.get("q")

    # check if query param. 'q' is missing
    if query is None:
        return {"message": 'Query parameter "q" is missing'}, 400

    # check if query param. 'q' is invalid
    if query.strip() == "" or query.isdigit():
        return {"message": "Invalid input paramter"}, 422

    # iter. thru data list to find person  whose first name matches query
    for person in data:
        if query.lower() in person["first_name"].lower():
            # if match found, return person as JSON response with 200 OK status code
            return person, 200

    # if no match, return appropiate JSON response with 404 Not Found status code
    return {"message": "Person not found"}, 404


# define route for '/count' URL
@app.route("/count")
def count():
    """Count items in data list"""
    try:
        # return JSON response with count of item in data
        return {"data count": len(data)}, 200
    except NameError:
        # if data not define, raise NameError, return JSON response with 500 Internal Server status code
        return {"message": "data not defined"}, 500


# define route for '/person/<uuid:id>' URL
@app.route("/person/<uuid:id>")
def find_by_uuid(id):
    """find person in data list by UUID"""
    # iter. trhu data to find person with matching ID
    for person in data:
        # check for match
        if person["id"] == str(id):
            # return JSON response if match is found
            return person, 200
    # if no match, return JSON reponse with message and 404 Not Found status code
    return {"message": "Person not found"}, 404


# define route for '/person/<uuid:id>' URL with DELETE method
@app.route("/person/<uuid:id>", methods=["DELETE"])
def delete_by_uuid(id):
    """find and delete person info from data list by UUID"""
    for person in data:
        if person["id"] == str(id):
            # remove  person from data list
            data.remove(person)
            # return JSON response with message and OK 200 status code
            return {"message": f"Person with ID {id} deleted"}, 200
    # if no match, return JSON response with message and Not Found 404 status code
    return {"message": "Person not found"}, 404


# define route for '/person' URL with POST method
@app.route("/person", methods=["POST"])
def add_by_uuid():
    """add new user to data list"""
    # get JSON data from request
    new_person = request.get_json()

    # check if JSON data is empty or None
    if not new_person:
        return {"message": "Invalid input paramter"}, 422

    try:
        # add new user to data
        data.append(new_person)
        # return JSON message with OK 200 status code
        return {"message": f'Added person with ID {new_person["id"]}'}, 200
    except NameError:
        return {"message": "data not defined"}, 500


# define error handler for 404 Not Found errors
@app.errorhandler(404)
def api_not_found(error):
    # error handler for 404 Not Found errors, triggered when 404 error occurs
    return {"message": "API not found"}, 404


# define error handler for 500 Internal Server errors   
@app.errorhandler(Exception)
def handle_exception(e):
    return {"exception": str(e)}, 500


# FOR TESTING
@app.route("/test500")
def test500():
    raise Exception("Forced exception for testing")
