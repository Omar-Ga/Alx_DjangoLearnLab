# Tagging and Search Functionality

This document explains the tagging and search features implemented in the Django Blog.

## Tagging System
- **Adding Tags**: When creating or editing a post, use the "Tags" field to enter comma-separated tag names (e.g., `python, django, webdev`).
- **Viewing Tags**: Tags are displayed on the post list and post detail pages.
- **Filtering by Tag**: Clicking on a tag will take you to a page listing all posts associated with that tag.

## Search Functionality
- **Using the Search Bar**: Located in the header, the search bar allows you to find posts by keywords.
- **What is searched**: The search query looks for matches in:
    - Post titles
    - Post content
    - Tag names
- **Results**: A dedicated search results page displays all matching posts.

## Technical Details
- **Model**: A `Tag` model with a many-to-many relationship to `Post`.
- **Views**:
    - `PostByTagListView`: A ListView filtered by tag name.
    - `search`: A functional view using Django's `Q` objects for multi-parameter filtering.
- **Forms**: `PostForm` handles the conversion of comma-separated strings into `Tag` objects during post creation and updates.
