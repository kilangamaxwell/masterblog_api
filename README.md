# masterblog_api

API for carrying CRUD operations on blog website.
The provided code is a Flask application that serves as a simple API for managing blog posts. Here is a breakdown of the code and its functionality:

# Flask Initialization:

The Flask application is initialized with Flask(**name**), where **name** represents the current module.
CORS (Cross-Origin Resource Sharing) is enabled for all routes using CORS(app), allowing cross-origin requests.

# File Operations:

The code includes functions for saving and loading blog posts from a JSON file.
save_posts_to_file(posts) saves the provided posts to a JSON file called "posts.json".
load_posts_from_file() loads the posts from the JSON file. If the file doesn't exist, it initializes the posts with some default data.

# Route Definitions:

/api/posts (GET): Retrieves all the posts. Optionally, it can sort the posts based on the provided sort and direction parameters.
/api/posts (POST): Adds a new post. It retrieves the new post data from the request JSON, generates a new ID, validates the data, adds the post to the list, and saves the updated list to the file.
/api/posts/<int:id> (DELETE): Deletes a post with the given ID. It finds the post by ID, removes it from the list, and saves the updated list to the file.
/api/posts/<int:id> (PUT): Updates a post with the given ID. It finds the post by ID, retrieves the updated data from the request JSON, updates the post with the new data, and saves the updated list to the file.
/api/posts/search (GET): Searches for posts based on the provided title, content, author, or date parameters. It filters the posts based on the provided parameters and returns the filtered posts.

# Error Handlers:

The code includes error handlers for HTTP error status codes 400, 404, and 405. These handlers return JSON responses with appropriate error messages.

# Execution:

The code includes a conditional block to run the Flask application only when the script is executed directly (**name** == '**main**').
The application runs on host "0.0.0.0" and port 5002 in debug mode.
Overall, this code provides a basic API for managing blog posts, including CRUD operations (create, read, update, delete) and search functionality. It uses a JSON file to store the post data and communicates with the frontend or other clients using JSON-based request and response data.
