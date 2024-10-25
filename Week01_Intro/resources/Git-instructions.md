# GitHub Repository Instructions for Students

Dear Students,

Below are the instructions for accessing and working on our course's private GitHub repository:

## 1. Accessing the Repository:

Once you receive an invitation to collaborate on the private GitHub repository, please accept the invitation to gain access.

## 2. Cloning the Repository:

After accepting the invitation:
1. Open a terminal or command prompt.
2. Use the following command to clone the repository to your local machine:
    ```bash
    git clone [REPO_URL]
    ```

*Note: Replace `[REPO_URL]` with the actual URL of the repository.*

## 3. Creating Your Personal Branch:

To ensure that everyone’s work is separate and organized, you'll each create your own branch:
1. Navigate to the cloned repository directory:
    ```bash
    cd [REPO_NAME]
    ```
2. Create a new branch named after your username or full name:
    ```bash
    git checkout -b [YOUR_NAME_OR_USERNAME]
    ```

## 4. Making Changes:

You can now make changes, add files, and more in your personal branch. After making changes, commit them using the following commands:
1. Add your changes:
    ```bash
    git add .
    ```
2. Commit your changes with a descriptive message:
    ```bash
    git commit -m "Your descriptive message about the changes here"
    ```

## 5. Pushing Changes to GitHub:

Once you're ready to upload your changes to GitHub:
1. Use the following command to push your changes:
    ```bash
    git push origin [YOUR_NAME_OR_USERNAME]
    ```

## 6. Pull Requests (PR):

If you'd like your changes to be reviewed and potentially merged into the main branch:
1. Navigate to our GitHub repository page.
2. Click on the "New Pull Request" button.
3. Select your branch and create a PR to the target branch (usually `main` or `master`).
4. Add any necessary comments and submit the PR. The instructor will review and merge your PR after verifying the changes.

## 7. Staying Updated:

If there are updates to the main branch that you need:
1. Checkout your personal branch:
    ```bash
    git checkout [YOUR_NAME_OR_USERNAME]
    ```
2. Pull the latest changes from the main branch:
    ```bash
    git pull origin main
    ```

---

Please always ensure you're working in your branch to avoid conflicts. Reach out if you have any questions or need further clarification. Happy coding!

---

*Note: Ensure you replace placeholders like `[REPO_URL]` and `[REPO_NAME]` with actual values before sharing.*