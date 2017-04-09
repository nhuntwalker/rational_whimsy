# Test Plan

A cohesive, comprehensive plan for mapping out tests for my website's codebase.

## Rational Whimsy

**None**

## Blog

### Models

- `Post` objects use the title as the string representation
- `Post` objects have the proper attributes ("title", "body", "created", "published_date", "modified", "slug", "status", "featured")
- The "published" model manager should return only `Post` objects with the "published" status
- The first `Post` object in the list of published `Post` objects should be the most recent
- Only one `Post` should be featured at a time
- When a `Post` is created, no matter its status, its `created` date should be set

### Views

- `ListPosts` view should list `Post` objects
- `ListPosts` page type should have "blog" as the name of the page
- `ListPosts` should only be listing published posts
- `post_detail` view should be able to take a primary key to show the detail for an individual post
- `post_detail` view should also be able to take a slug to show the detail for an individual post
- `EditPost` view edits an existing post given the proper primary key
- When `EditPost` is given the wrong `pk`, a 404 should be raised
- `DeletePost` view actually deletes a given post
- When `DeletePost` is given the wrong `pk`, a 404 should be raised
- `CreatePost` view creates a post given the proper information


### Routes

- `list_posts` route returns a status 200
- `list_posts` route gets published posts
- `list_posts` route has the right page title of "blog"
- `list_posts` route uses both the `layout.html` and `blog_list.html` templates
- For any given post, the `post_detail_slug` route returns a status code of 200
- For any given post, the `post_detail_pk` route also returns a status code of 200
- When the `post_detail` route is hit with a `slug` that doesn't exist, a 404 page should be shown
- When the `post_detail` route is hit with a `pk` that doesn't exist, a 404 page should be shown
- `create_posts` route has a form on the page
- `create_posts` route has the correct form fields
- `create_posts` route creates a new post when given the appropriate information
- `create_posts` route redirects after a successful post
- `edit_post` route has a form on the page
- `edit_post` route has correct form fields
- `edit_post` route redirects on a successful post
- `edit_post` route redirects to the `list_posts` page
- `delete_post` route returns status code of 200
- `delete_post` route confirms whether or not you want to actually delete the given post
- `delete_post` route removes the given `Post` object from the database
- `delete_post` route redirects after a successful deletion
- `delete_post` route redirects to the `list_posts` page after a successful deletion

## Profile

### Models

- A `Profile` is made whenever a `User` is saved
- Only one `Profile` gets created when a `User` is saved
- The `NMHWProfile` object has the proper attributes
- The string representation of the `NMHWProfile` object is the username

### Views

- `profile_detail` view has the right details on the page (linkedin, twitter, github, instagram links)
- `profile_edit` view has a form on the page
- `profile_edit` view form has the right input fields
- `profile_edit` view form redirects with successful submission
- `profile_edit` view form redirects to profile page with successful submission
- `profile_edit` view actually changes the model's attributes with a successful submission

### Routes

- `profile` route accesses an actual profile object and attaches it to the `profile` keyword in the response context
- `profile` route uses the proper template
- `login` route has a form on the page
- `login` route's form has the right input fields
- A successful login redirects
- A successful login redirects and lands on the home page
- A successful login authenticates the user
- `profile_edit` route has a model form in the response's context
- A successful submission to the `profile_edit` route changes the model object
- An unauthenticated user gets redirected to the `login` page when they attempt to access the `profile_edit` route
- An authenticated user, when logged out, becomes unauthenticated


## To be written

- The `edit_post` route when given the right data actually edits the given post
- The `edit_post` route when given the wrong pk shows a 404 page
- The `delete_post` route when given the wrong pk shows a 404 page

- `get_github_repos` returns a serialized list of GitHub repositories that I've worked on
- `get_github_info` takes in a URL with the appropriate headers and returns JSON corresponding to the data at the URL
- `process_github_events` takes in some JSON event data from GitHub and returns a list of repositories from whitelisted repositories

- The `home_view` takes a request and returns all published posts
- The `home_view` takes a request and returns the featured post
- The `home_page` route uses the `home.html` template
- The `home_page` route returns the 3 most recently-published posts excluding the featured post
- The `home_page` route contains the featured post in its response