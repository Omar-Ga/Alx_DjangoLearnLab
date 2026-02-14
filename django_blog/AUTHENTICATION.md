# Django Blog Authentication System

This document describes the user authentication system implemented in the Django Blog project.

## Features
- **User Registration**: New users can create an account with a username and email.
- **User Login**: Existing users can securely log in to their accounts.
- **User Logout**: Authenticated users can log out.
- **Profile Management**: Logged-in users can view and update their profile information (username and email).

## Implementation Details
- **Forms**: 
    - `UserRegisterForm`: A custom form extending Django's `UserCreationForm` to include the email field.
- **Views**:
    - `register`: Handles the registration process and logs in the user upon successful sign-up.
    - `profile`: A login-protected view that allows users to see and edit their account details.
    - Built-in `LoginView` and `LogoutView` are used for standard login/logout logic.
- **Templates**:
    - `login.html`: Provides the login form.
    - `register.html`: Provides the registration form.
    - `profile.html`: Displays user info and an update form.
    - `logout.html`: Confirmation page for logouts (if configured).

## How to Test
1. **Registration**: 
    - Navigate to `/register/`.
    - Fill out the form and submit.
    - You should be redirected to the `/profile/` page.
2. **Login**:
    - Navigate to `/login/`.
    - Enter valid credentials.
    - You should be redirected to the `/profile/` page.
3. **Logout**:
    - Click the "Logout" button in the navigation bar.
    - You should be redirected to the home page (or show a logout confirmation).
4. **Profile Update**:
    - Log in and go to `/profile/`.
    - Change your username or email and click "Update Profile".
    - Verify the changes are saved.

## Security
- All forms use the `{% csrf_token %}` tag to prevent Cross-Site Request Forgery.
- Password hashing is handled automatically by Django's authentication system.
