## Summary

- Convert the existing `blog` app from a stub into a simple database-backed blog.
- Add a `Post` model and admin integration so new posts can be created via the Django admin UI.
- Implement list/detail views and templates for blog posts, plus a site-wide navigation link to the blog.

## Changes

### Data model and migrations

- Added a `Post` model in `blog/models.py` with:
  - `title`, `slug`, `excerpt`, `body`
  - `created_at`, `updated_at`
  - `published` flag
- Generated an initial migration (`blog/migrations/0001_initial.py`) to create the `blog_post` table.

### Admin

- Registered `Post` with the Django admin in `blog/admin.py`.
- Configured `PostAdmin` with:
  - `list_display = ("title", "published", "created_at")`
  - `list_filter = ("published", "created_at")`
  - `search_fields = ("title", "body")`
  - `prepopulated_fields = {"slug": ("title",)}` so slugs are auto-filled from titles.
- This allows blog posts to be added, edited, and searched through `/admin/`.

### Views and URLs

- Implemented `PostListView` and