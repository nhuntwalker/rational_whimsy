# Test Plan

A cohesive, comprehensive plan for mapping out tests for my website's codebase.

## Rational Whimsy

**None**

## Blog

### Models

- `Post` objects use the title as the string representation
- `Post` objects have the proper attributes (title, body, created, published_date, modified, slug, status, featured)
- The "published" model manager should return only `Post` objects with the "published" status
- The first `Post` object in the list of published `Post` objects should be the most recent
- Only one `Post` should be featured at a time

### Views

- `ListPosts` view should list `Post` objects
- `ListPosts` page type should have "blog" as the name of the page
- `post_detail` view should be able to take a primary key to show the detail for an individual post
- `post_detail` view should also be able to take a slug to show the detail for an individual post
- `EditPost` view edits an existing post given the proper primary key
- `DeletePost` view actually deletes a given post
- `CreatePost` view creates a post given the proper information

### Routes

- `list_posts` route returns a status 200
- `list_posts` route gets published posts
- `list_posts` route has the right page title of "blog"
- `list_posts` route uses both the `layout.html` and `blog_list.html` templates
- For any given post, the `post_detail_slug` route returns a status code of 200
- For any given post, the `post_detail_pk` route also returns a status code of 200
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

- 
