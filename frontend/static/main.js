// Function that runs once the window is fully loaded
window.onload = function () {
  // Attempt to retrieve the API base URL from the local storage
  var savedBaseUrl = localStorage.getItem("apiBaseUrl");
  // If a base URL is found in local storage, load the posts
  if (savedBaseUrl) {
    document.getElementById("api-base-url").value = savedBaseUrl;
    loadPosts();
  }
};

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
  // Retrieve the base URL from the input field and save it to local storage
  var baseUrl = document.getElementById("api-base-url").value;
  localStorage.setItem("apiBaseUrl", baseUrl);

  // Use the Fetch API to send a GET request to the /posts endpoint
  fetch(baseUrl + "/posts")
    .then((response) => response.json()) // Parse the JSON data from the response
    .then((data) => {
      // Once the data is ready, we can use it
      // Clear out the post container first
      const postContainer = document.getElementById("post-container");
      postContainer.innerHTML = "";

      // For each post in the response, create a new post element and add it to the page
      data.forEach((post) => {
        const postDiv = document.createElement("div");
        postDiv.className = "post";
        postDiv.innerHTML = `<h2>${post.title}</h2><h3>by: ${post.author}</h3>
                <p>${post.content}</p><p>Date: ${post.date}</p>
                <button onclick="updatePost(${post.id})">Update</button>
                <button onclick="deletePost(${post.id})">Delete</button>`;
        postContainer.appendChild(postDiv);
      });
    })
    .catch((error) => console.error("Error:", error)); // If an error occurs, log it to the console
}

// Function to send a POST request to the API to add a new post
function addPost() {
  // Retrieve the values from the input fields
  var baseUrl = document.getElementById("api-base-url").value;
  var postTitle = document.getElementById("post-title").value;
  var postContent = document.getElementById("post-content").value;
  var postAuthor = document.getElementById("post-author").value;
  var postDate = document.getElementById("post-date").value;

  // Use the Fetch API to send a POST request to the /posts endpoint
  fetch(baseUrl + "/posts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: postTitle,
      content: postContent,
      author: postAuthor,
      date: postDate,
    }),
  })
    .then((response) => response.json()) // Parse the JSON data from the response
    .then((post) => {
      console.log("Post added:", post);
      loadPosts(); // Reload the posts after adding a new one
    })
    .catch((error) => console.error("Error:", error)); // If an error occurs, log it to the console
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
  var baseUrl = document.getElementById("api-base-url").value;

  // Use the Fetch API to send a DELETE request to the specific post's endpoint
  fetch(baseUrl + "/posts/" + postId, {
    method: "DELETE",
  })
    .then((response) => {
      console.log("Post deleted:", postId);
      loadPosts(); // Reload the posts after deleting one
    })
    .catch((error) => console.error("Error:", error)); // If an error occurs, log it to the console
}
// Function to send an UPDATE request to the API to delete a post
// function updatePost(postId) {
//   var baseUrl = document.getElementById("api-base-url").value;

//   // Prompt the user to enter the new values for the post
//   var postTitle = prompt("Enter the new title:");
//   var postContent = prompt("Enter the new content:");
//   var postAuthor = prompt("Enter the new author:");
//   var postDate = prompt("Enter the new date:");

//   // Use the Fetch API to send a PUT request to the specific post's endpoint
//   fetch(baseUrl + "/posts/" + postId, {
//     method: "PUT",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({
//       title: postTitle,
//       content: postContent,
//       author: postAuthor,
//       date: postDate,
//     }),
//   })
//     .then((post) => {
//       console.log("Post added:", post);
//       //loadPosts(); // Reload the posts after adding a new one
//     })
//     .then((response) => {
//       console.log("Post Update:", postId);
//       loadPosts(); // Reload the posts after updating one
//     })
//     .catch((error) => console.error("Error:", error)); // If an error occurs, log it to the console
// }

// Function to send an UPDATE request to the API to update a post
function updatePost(postId) {
  var baseUrl = document.getElementById("api-base-url").value;

  // Retrieve the values from the input fields
  var postTitle = prompt("Enter the new title:");
  var postContent = prompt("Enter the new content:");
  var postAuthor = prompt("Enter the new author:");
  var postDate = prompt("Enter the new date:");

  // Create the updated post object
  var updatedPost = {
    title: postTitle,
    content: postContent,
    author: postAuthor,
    date: postDate,
  };

  // Use the Fetch API to send a PUT request to the specific post's endpoint
  fetch(baseUrl + "/posts/" + postId, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updatedPost),
  })
    .then((response) => {
      if (response.ok) {
        console.log("Post Updated:", postId);
        loadPosts(); // Reload the posts after updating one
      } else {
        console.error("Error:", response.status);
      }
    })
    .catch((error) => console.error("Error:", error)); // If an error occurs, log it to the console
}
