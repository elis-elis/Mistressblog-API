from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "neVer", "content": "never say NEvER."},
    {"id": 2, "title": "Something is Cooking", "content": "...not food related."},
    {"id": 3, "title": "NOT you", "content": "i like you."},
    {"id": 4, "title": "NADA", "content": "i am, you are, we are."}
]


def generate_new_id():
    """
    This function calculates the next unique ID by finding the maximum ID
    in the existing POSTS list and incrementing it by 1.
    If the list is empty, it starts with an ID of 1.
    """
    if POSTS:
        return max(post['id'] for post in POSTS) + 1
    else:
        return 1


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    This function is responsible for handling requests to add a new blog post to the list of posts.
    It takes data sent by the user, checks that everything is in order,
    creates a new post with a unique ID, and then adds it to the list of posts.
    """
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid or malformed JSON provided."}), 400

    # Validate the input
    missing_fields = []
    if 'title' not in data:
        missing_fields.append('title')
    if 'content' not in data:
        missing_fields.append('content')
    if missing_fields:
        return jsonify({"error": "Missing field(s): " + ", ".join(missing_fields)}), 400

    # generate new ID for the post
    new_id = generate_new_id()

    # create the new post object
    new_post = {
        'id': new_id,
        'title': data['title'],
        'content': data['content']
    }

    # Add the new post to the POSTS list
    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post_by_id(id):
    """
    This function deletes a blog post by its ID.
    And returns a response as a JSON object with status code 200 if the post is found and deleted,
    or a JSON object with an error message and status code 404 if the post is not found.
    """
    # initializing a default state where no matching post has been found.
    post_to_delete = None

    for post in POSTS:
        if post['id'] == id:
            post_to_delete = post
            break

    if post_to_delete is None:
        return jsonify({"error": f"post with id {id} is not found"}), 404
    else:
        POSTS.remove(post_to_delete)
        return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post_by_id(id):
    """
    This Function updates a blog post by its ID. It allows for partial updates,
    meaning the client can update just the title, just the content, or both.
    It handles cases where the post is not found, or the client provides invalid JSON.
    """
    # Parse the JSON body of the request
    data = request.get_json()

    # Check if the request body is valid JSON
    if data is None:
        return jsonify({"error": "Invalid or malformed JSON provided."}), 400

    # Find the post by ID
    post_to_update = None
    for post in POSTS:
        if post['id'] == id:
            post_to_update = post
            break

    if post_to_update is None:
        return jsonify({"error": f"Post with id {id} is not found"}), 404
    else:
        # Update the post's title and content if provided, otherwise keep the old values
        # The 'get' method is used to retrieve the title and content fields from the data dictionary.
        # If a field is not provided (None), it defaults to the current value in post_to_update.
        title = data.get('title', post_to_update['title'])
        content = data.get('content', post_to_update['content'])
        post_to_update['title'] = title
        post_to_update['content'] = content

        # Return the updated post with a success message
        # Since dics are mutable, modifying post_to_update automatically updates the original POSTS list.
        return jsonify({"id": post_to_update['id'],
                        "title": post_to_update['title'],
                        "content": post_to_update['content']
                        }), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts_by_title_or_content():
    """
    This endpoint allows clients to search for posts by providing 'title' or 'content'
    as query parameters. The search is case-insensitive and will return all posts
    that match the search criteria.

    Returns:
        A JSON list of matched posts with a 200 OK status.
    """
    # Extract query parameters from the URL
    title_query = request.args.get('title')
    content_query = request.args.get('content')

    # List to store matched posts
    searched_posts = []

    # Iterate over POSTS to find matches
    for post in POSTS:
        # Check if the post title or content contains the search terms
        if (title_query and title_query.lower() in post['title'].lower()) or (
                content_query and content_query.lower() in post['content'].lower()):
            searched_posts.append(post)

    return jsonify(searched_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
