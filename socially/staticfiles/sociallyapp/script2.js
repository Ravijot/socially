$(document).ready(function() {
    const username = localStorage.getItem('profileToVisit');  // Replace with the actual username or fetch it dynamically
    const token = localStorage.getItem('accessToken');
    const userData = {
        first_name: localStorage.getItem('firstName'),
        last_name: localStorage.getItem('lastName'),
        profile_pic: localStorage.getItem('profilePic'),
        username: localStorage.getItem('username') // Add username to local storage
    };
    // Fetch user profile data
    
        $.ajax({
        url: `http://localhost:8000/profile/${username}/`,
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        success: function(response) {
            // Set the user data in the profile section
            $('#profile-pic').attr('src', userData.profile_pic);
            $('#cover-photo').css('background-image', `url(${response.cover_pic})`);
            $('#user-name').text(`${userData.first_name} ${userData.last_name}`);
            $('#profile-picture').attr('src', response.profile_pic);
            $('#user-full-name').text(`${response.first_name} ${response.last_name}`);
            $('#user-username').text(`@${response.username}`);
            $('.profile-info .mr-3').text(`Followers: ${response.followers_count}`);
            $('.profile-info .d-flex p:nth-child(2)').text(`Followings: ${response.following_count}`);
            if (response.is_following) {
                $('#follow-button').text('Unfollow');
            // Perform actions if the user is a follower
            } else {
                $('#follow-button').text('Follow');
            // Perform actions if the user is not a follower
            }
        },
        error: function(xhr) {
            console.error('Failed to fetch profile data');
        }
        });
    
        function fetchFollowersfollowing() {
            $.ajax({
                url: `http://localhost:8000/profile/${username}/`,
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                success: function(response) {
                    $('.profile-info .mr-3').text(`Followers: ${response.followers_count}`);
                    $('.profile-info .d-flex p:nth-child(2)').text(`Followings: ${response.following_count}`);
                    if (response.is_following) {
                        $('#follow-button').text('Unfollow');
                    // Perform actions if the user is a follower
                    } else {
                        $('#follow-button').text('Follow');
                    // Perform actions if the user is not a follower
                    }
                },
                error: function(xhr) {
                    console.error('Failed to fetch profile data');
                }
                });
        }

        if (username !== userData.username) {
            $('#follow-button').show();
            
        }
        else{
            $('#cover-upload-icon').show();
            $('#profile-upload-icon').show();
        }

        /*function updateFollowButton(message) {
            if (message=="Unfollowed successfully") {
                $('#follow-button').text('Follow');
            } else {
                $('#follow-button').text('Unfollow');
            }
        }*/

     // Handle follow/unfollow button click
     $('#follow-button').click(function() {
        $.ajax({
            url: `http://127.0.0.1:8000/follow/${username}/`,
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            success: function(response) {
                fetchFollowersfollowing(); // Update the button text based on the following status
            },
            error: function(xhr) {
                console.error('Failed to follow/unfollow user');
            }
        });
    });

    
    // Handle logout button click
    $('#logout-button').click(function() {
        localStorage.removeItem('accessToken');
        window.location.href = '/login/';
    });
    
    
        // Handle logout button click
    $('#logout-button').click(function() {
        const refreshToken = localStorage.getItem('refreshToken');
        const token = localStorage.getItem('accessToken');

        $.ajax({
            url: 'http://localhost:8000/login/',
            method: 'GET',
            success: function(response) {
   
                // Clear local storage
                localStorage.removeItem('userId');
                localStorage.removeItem('firstName');
                localStorage.removeItem('lastName');
                localStorage.removeItem('profilePic');
                localStorage.removeItem('username');
                localStorage.removeItem('accessToken');
                localStorage.removeItem('refreshToken');
                // Redirect to login page
                window.location.href = '/login/';
        },
        error: function(xhr) {
            $('#error-message').text('Failed to log out. Please try again.').removeClass('d-none').addClass('alert-danger');
        }
        });
    });

    // Fetch and display posts
    function loadPosts() {
        const token = localStorage.getItem('accessToken');
  
        $.ajax({
            url: 'http://localhost:8000/posts/',
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            success: function(response) {
                const postsContainer = $('#posts-container');
                postsContainer.empty(); // Clear any existing posts
  
                response.forEach(post => {
                    // Check if the user has liked the post
                    //const isLiked = post.likes.includes(userId);
                    let commentsHtml = '';
                    post.comments.forEach(comment => {
                        const timestamp = new Date(comment.created);
                        const timeAgo = getTimeAgo(timestamp);
                        
                        commentsHtml += `
                            <div class="comment mt-2">
                                <strong>${comment.commented_by.first_name} ${comment.commented_by.last_name}</strong>
                                <a href="/profile/${comment.commented_by.username}" class="username-link">
                                    <span>@${comment.commented_by.username}</span>
                                </a>
                                <small class="text-muted">${timeAgo}</small>
                                
                               ${userData.username === comment.commented_by.username ? `<i class="bi bi-trash delete-comment-icon" data-comment-id="${comment.id}"></i>` : ``}
                                <p>${comment.content}</p>                                        
                            </div>`;
                    });
                    const timestamp = new Date(post.created);
                    const timeAgo = getTimeAgo(timestamp);
                    const likesHtml = post.likes.map(like => like.username).join(', ');
                    const isLiked = post.likes.some(like => like.username === userData.username);
                    const postHtml = `
                        <div class="post mt-4 p-4 shadow" data-post-id="${post.id}">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <strong>${post.posted_by.first_name} ${post.posted_by.last_name}</strong> 
                                    <a href="/profile/${post.posted_by.username}" class="username-link">
                                        <span>@${post.posted_by.username}</span>
                                    </a>
                                </div>
                                <div>
                                    <small class="text-muted">${timeAgo}</small>
                                </div>
                            </div>
                            <div class="post-content mt-2">
                                ${post.content}
                            </div>
                            <div class="post-actions mt-3 d-flex justify-content-between">
                                <button class="btn btn-light like-button ${isLiked ? 'liked' : ''}" data-post-id="${post.id}">
                                    <i class="bi bi-hand-thumbs-up"></i> <span class="badge badge-primary">${post.likes.length}</span>
                                </button>
                                <button class="btn btn-light comment-button" data-post-id="${post.id}">
                                    <i class="bi bi-chat"></i> <span class="badge badge-primary">${post.comments.length}</span>
                                </button>
                                ${userData.username === post.posted_by.username ? `<button class="btn btn-light delete-button" data-post-id="${post.id}"><i class="bi bi-trash"></i></button>` : ``}
                            </div>
                            <div class="comments-container mt-3" >
                                ${commentsHtml}
                                <div class="comment-form">
                                    <textarea class="form-control" id="comment-content" placeholder="Add a comment..."></textarea>
                                    <button class="btn btn-primary post-comment-button" data-post-id="${post.id}">Post Comment</button>
                                </div>
                            </div>
                        </div>
                    `;
                    postsContainer.append(postHtml);
                });
            },
            error: function(xhr) {
                $('#error-message').text('Failed to load posts. Please try again.').removeClass('d-none');
            }
        });
    }
    // Function to convert timestamp to human-readable format
    function getTimeAgo(timestamp) {
        const seconds = Math.floor((new Date() - timestamp) / 1000);
        let interval = Math.floor(seconds / 31536000);
        if (interval > 1) return `${interval} years ago`;
        interval = Math.floor(seconds / 2592000);
        if (interval > 1) return `${interval} months ago`;
        interval = Math.floor(seconds / 86400);
        if (interval > 1) return `${interval} days ago`;
        interval = Math.floor(seconds / 3600);
        if (interval > 1) return `${interval} hours ago`;
        interval = Math.floor(seconds / 60);
        if (interval > 1) return `${interval} minutes ago`;
        return `just now`;
    }

    loadPosts();

    $('#post-button').click(function() {
        const content = $('#post-content').val().trim();
        const token = localStorage.getItem('accessToken');

        if (!content) {
            $('#error-message').text('Please add some content to post.').removeClass('d-none');
            return;
        }

        $.ajax({
            url: 'http://localhost:8000/posts/',
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            contentType: 'application/json',
            data: JSON.stringify({ content: content }),
            success: function(response) {
                $('#post-content').val('');
                $('#error-message').text('Post Created Successfully').removeClass('d-none').addClass('alert-success').removeClass('alert-danger');
                loadPosts(); // Reload posts to show the new post
            },
            error: function(xhr) {
                $('#error-message').text('Failed to post content. Please try again.').removeClass('d-none').addClass('alert-danger');
            }
        });
    });

    // When clicking the like button
  $(document).on('click', '.like-button', function() {
    const postId = $(this).data('post-id');
    const token = localStorage.getItem('accessToken');

    $.ajax({
          url: `http://localhost:8000/posts/${postId}/like/`,
          method: 'POST',
          headers: {
          'Authorization': `Bearer ${token}`
      },
      success: function(response) {
          $.ajax({
                  url: `http://localhost:8000/posts/${postId}/`,
                  method: 'GET',
                  headers: {
                  'Authorization': `Bearer ${token}`
              },
              success: function(response) {
              const isLiked = response.likes.some(like => like.username === userData.username);
              const likeButton = $(`.like-button[data-post-id="${postId}"]`);
              likeButton.toggleClass('liked', isLiked);
              likeButton.find('.badge').text(response.likes.length);
              },
              error: function(xhr) {
              $('#error-message').text('Failed to like post. Please try again.').removeClass('d-none').addClass('alert-danger');
              }
          });
      }
    });
});

    // Handle comment button clicks to toggle comment visibility
    $(document).on('click', '.comment-button', function() {
        const postId = $(this).data('post-id');
        const commentsContainer = $(`[data-post-id="${postId}"] .comments-container`);
        commentsContainer.toggle(); // Toggle visibility of comments
    });

    

    // Handle delete button clicks
    $(document).on('click', '.delete-button', function() {
        const postId = $(this).data('post-id');
        const token = localStorage.getItem('accessToken');

        $.ajax({
            url: `http://localhost:8000/posts/${postId}/`,
            method: 'DELETE',
            headers: {
                        'Authorization': `Bearer ${token}`
            },
            success: function(response) {
            loadPosts(); // Reload posts to reflect the deleted post
            },
            error: function(xhr) {
                        $('#error-message').text('Failed to delete post. Please try again.').removeClass('d-none').addClass('alert-danger');
            }
        });
    });

    // Handle post comment button clicks
    $(document).on('click', '.post-comment-button', function() {
        const postId = $(this).data('post-id');
        const content = $(`[data-post-id="${postId}"] #comment-content`).val().trim();
        const token = localStorage.getItem('accessToken');

        if (!content) {
            $('#error-message').text('Please add some content to comment.').removeClass('d-none');
            return;
        }

        $.ajax({
            url: `http://localhost:8000/comments/`,
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            contentType: 'application/json',
            data: JSON.stringify({ content: content, post: postId }),
            success: function(response) {
            $(`[data-post-id="${postId}"] #comment-content`).val('');
            loadPosts(); // Reload posts to show the new comment
        },
        error: function(xhr) {
            $('#error-message').text('Failed to post comment. Please try again.').removeClass('d-none').addClass('alert-danger');
        }
        });
    });
    // Handle delete comment icon clicks
    $(document).on('click', '.delete-comment-icon', function() {
        const commentId = $(this).data('comment-id');
        const token = localStorage.getItem('accessToken');

        $.ajax({
            url: `http://localhost:8000/comments/${commentId}/`,
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            success: function(response) {
            loadPosts(); // Reload posts to reflect the deleted comment
            },
            error: function(xhr) {
                $('#error-message').text('Failed to delete comment. Please try again.').removeClass('d-none').addClass('alert-danger');
            }
        });
    });
    // Handle username link clicks
    $(document).on('click', '.username-link', function(e) {
        e.preventDefault(); // Prevent default link behavior
        const username = $(this).text().trim().replace('@', ''); // Get the username without the '@' symbol
        localStorage.setItem('profileToVisit', username); // Store the username in local storage
        const token = localStorage.getItem('accessToken');
        $.ajax({
            url: `http://localhost:8000/profile/`,
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            success: function(response) {
            window.location.href = '/profile/'; // Redirect to the profile page
        },
        error: function(xhr) {
            $('#error-message').text('Please try again.').removeClass('d-none').addClass('alert-danger');
        }
        });

    });

    //Profile Icon click
    $(document).on('click', '#profile-icon', function(e) {
        e.preventDefault(); // Prevent default link behavior
        localStorage.setItem('profileToVisit', localStorage.getItem('username')); // Store the username in local storage
        const token = localStorage.getItem('accessToken');
        $.ajax({
            url: `http://localhost:8000/profile/`,
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            success: function(response) {
            window.location.href = '/profile/'; // Redirect to the profile page
            },
            error: function(xhr) {
                $('#error-message').text('Please try again.').removeClass('d-none').addClass('alert-danger');
            }
        });

});

function showUploadIcon(iconId) {
    $(iconId).show();
}

function hideUploadIcon(iconId) {
    $(iconId).hide();
}

// Show upload icon on hover
$('.cover-pic-upload').hover(
    function() { showUploadIcon('#cover-upload-icon'); },
    function() { hideUploadIcon('#cover-upload-icon'); }
);

$('.profile-pic-upload').hover(
    function() { showUploadIcon('#profile-upload-icon'); },
    function() { hideUploadIcon('#profile-upload-icon'); }
);

// Handle cover upload icon click
$('#cover-upload-icon').click(function() {
    $('#cover-pic-input').click();
});

// Handle profile upload icon click
$('#profile-upload-icon').click(function() {
    $('#profile-pic-input').click();
});

// Handle cover picture upload
$('#cover-pic-input').change(function() {
    const formData = new FormData();
    formData.append('cover_pic', this.files[0]);

    $.ajax({
        url: 'http://127.0.0.1:8000/update/cover-pic/',
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        processData: false,
        contentType: false,
        data: formData,
        success: function(response) {
            $('#cover-photo').css('background-image', `url(${response.cover_pic})`);
        },
        error: function(xhr) {
            console.error('Failed to upload cover picture');
        }
    });
});

// Handle profile picture upload
$('#profile-pic-input').change(function() {
    const formData = new FormData();
    formData.append('profile_pic', this.files[0]);

    $.ajax({
        url: 'http://127.0.0.1:8000/update/profile-pic/',
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        processData: false,
        contentType: false,
        data: formData,
        success: function(response) {
            $('#profile-picture').attr('src', response.profile_pic);
        },
        error: function(xhr) {
            console.error('Failed to upload profile picture');
        }
    });
});
    });