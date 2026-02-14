# Django Blog Comment System

The comment system allows users to interact with blog posts by leaving feedback and participating in discussions.

## Features
- **View Comments**: Anyone can see comments on a post detail page.
- **Add Comment**: Logged-in users can post a new comment on any post.
- **Edit Comment**: The author of a comment can modify its content.
- **Delete Comment**: The author of a comment can remove it.

## Implementation
- **Model**: `Comment` linked to `Post` and `User`.
- **Form**: `CommentForm` for content input.
- **Views**:
    - `PostDetailView`: Displays post content and associated comments.
    - `CommentCreateView`: Handles new comment submission.
    - `CommentUpdateView`: Handles comment editing (restricted to author).
    - `CommentDeleteView`: Handles comment removal (restricted to author).
- **URLs**:
    - `/post/<int:pk>/comments/new/`: Create a comment.
    - `/comment/<int:pk>/update/`: Update a comment.
    - `/comment/<int:pk>/delete/`: Delete a comment.

## Permissions
- Authentication is required to add, edit, or delete comments.
- A `UserPassesTestMixin` ensures only the original author of a comment can edit or delete it.
