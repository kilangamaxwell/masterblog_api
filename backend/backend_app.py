from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


def save_posts_to_file(posts):
    """Save posts to a JSON file.

    Parameters:
        posts (list): The list of posts to be saved.
    """
    with open("posts.json", "w") as file:
        json.dump(posts, file)


def load_posts_from_file():
    """Load posts from the JSON file.

    Returns:
        list: The list of posts loaded from the file or default data if the file doesn't exist.
    """
    try:
        with open("posts.json", "r") as file:
            posts = json.load(file)
    except FileNotFoundError:
        # Handle the case when the file doesn't exist
        posts = [
            {"id": 1,
             "title": "My First Blog Post",
             "content": "This is the content of my first blog post.",
             "author": "Robert Maxwell",
             "date": "2023-06-07"},
            {"id": 2,
             "title": "My Second Blog Post",
             "content": "This is the content of my second blog post.",
             "author": "John Doe",
             "date": "2023-06-08"},
        ]
    return posts


def find_post_id(post_id):
    """Find the post with the given ID.

    Parameters:
        post_id (int): The ID of the post to find.

    Returns:
        dict or None: The post with the specified ID if found, otherwise None.
    """
    posts = load_posts_from_file()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all posts or sorted posts based on parameters.

    Returns:
        jsonify: JSON response containing the list of posts or sorted posts based on the parameters.
    """
    posts = load_posts_from_file()
    save_posts_to_file(posts)
    sort = request.args.get('sort')
    direction = request.args.get('direction')

    if not sort and not direction:
        return jsonify(posts), 200

    if sort in ['title', 'content', 'author', 'date'] and direction in ['asc', 'desc']:
        sorted_posts = sorted(
            posts, key=lambda post: post[sort], reverse=(direction == 'desc'))
        return jsonify(sorted_posts), 200

    return jsonify({'message': 'Invalid Parameters 404'}), 404


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Add a new post.

    Returns:
        jsonify: JSON response containing the new post data.
    """
    posts = load_posts_from_file()
    new_post = request.get_json()

    new_id = max(post['id'] for post in posts) + 1
    new_post['id'] = new_id

    for key in ["title", "content", "author", "date"]:
        if key not in new_post.keys():
            return jsonify({'message': f'Missing post {key} 404'}, new_post), 404

    posts.append(new_post)
    save_posts_to_file(posts)

    print("Successfully added a new post.")
    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """Delete a post with the given ID.

    Parameters:
        id (int): The ID of the post to delete.

    Returns:
        jsonify: JSON response containing the deleted post data and a success message.
    """
    posts = load_posts_from_file()
    post = find_post_id(id)

    if post is None:
        return post_not_found_error(404)

    posts.remove(post)
    save_posts_to_file(posts)

    return jsonify(post, {"message": f"Post with id: {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """Update a post with the given ID.

    Parameters:
        id (int): The ID of the post to update.

    Returns:
        jsonify: JSON response containing the updated post data.
    """
    posts = load_posts_from_file()
    post = find_post_id(id)

    if post is None:
        return post_not_found_error(404)

    new_data = request.get_json()
    if new_data is None:
        print("No changes to the post")
        return jsonify(post)
    else:
        post.update(new_data)
        save_posts_to_file(posts)
        print(f"The post with id: {id} was successfully updated.")

    return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search for posts based on parameters.

    Returns:
        jsonify: JSON response containing the filtered posts based on the parameters.
    """
    posts = load_posts_from_file()
    title = request.args.get('title')
    content = request.args.get('content')
    author = request.args.get('author')
    date = request.args.get('date')

    if title:
        filtered_posts = [post for post in posts if post.get('title') == title]
        return jsonify(filtered_posts), 200

    if content:
        filtered_posts = [
            post for post in posts if post.get('content') == content]
        return jsonify(filtered_posts), 200

    if author:
        filtered_posts = [
            post for post in posts if post.get('author') == author]
        return jsonify(filtered_posts), 200

    if date:
        filtered_posts = [post for post in posts if post.get('date') == date]
        return jsonify(filtered_posts), 200

    return jsonify({'message': "Post Not Found"}), 404


@app.errorhandler(400)
def invalid_post_entry(error):
    """Handle and return a JSON response for invalid post entry.

    Returns:
        jsonify: JSON response for invalid post entry.
    """
    print("Invalid data structure for post entry")
    return jsonify({"error": "Invalid data structure"}), 400


@app.errorhandler(404)
def post_not_found_error(error):
    """Handle and return a JSON response for a post not found error.

    Returns:
        jsonify: JSON response for a post not found error.
    """
    print("Post Not Found")
    return jsonify({"error": "Post Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    """Handle and return a JSON response for a method not allowed error.

    Returns:
        jsonify: JSON response for a method not allowed error.
    """
    print("Method Not Allowed")
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
