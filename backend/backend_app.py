from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "never", "content": "never say never."},
    {"id": 2, "title": "Something is cooking", "content": "not food related."},
    {"id": 3, "title": "not you", "content": "i like you."},
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
