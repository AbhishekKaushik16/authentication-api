This is an Python API for authenticating user and using JWT tokens.

TechStack:
1. Flask 
2. SQLAlchemy
3. Postgres

Endpoints:

1. /accounts/register: Register user and send them an email for verification and give back JWT token.
2. /accounts/login: Login user by returning new JWT token.
3. /accounts/update: Updates information related to user such as email, password, etc.
4. /accounts/delete: Delete user from database.
5. /confirm/<token>: Confirms token given in email to user for verification.
6. /<resource_name>/<_id>: Search any resource by its _id.
