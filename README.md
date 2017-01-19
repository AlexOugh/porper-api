
# Porper (Portable Permission Controller) API

Overview
=================

This is an API interface to support Porper implemented by AWS Lambda and API Gateway.

![porper][porper-image]

## Database Initialization

After creating a database, populate initial data using 'porper_initial.sql' in [porper-core][porper-core-url] repository
```
$ mysql -h <db_host> -u <db_user> -p <db_name> < porper_initial.sql
```

## How to use Google+ and Github Authentication

If you plan to use Google+ and/or GitHub authentications, set related values as environment variables of Lambda Function. (Please see next section, 'Environment Variables')

Please see these 2 sites to find out how to setup OpenID connect

Google+ : https://developers.google.com/identity/protocols/OpenIDConnect

GitHut : https://developer.github.com/v3/oauth/

## Environment Variables

These are environment variables for the Lambda Function.
```
{
  "MYSQL_Host": "<db_host>",
  "MYSQL_User": "<db_user>",
  "MYSQL_Password": "<db_password>",
  "MYSQL_Database": "<db_name>",
  "Google_Tokeninfo_Endpoint": "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=",
  "Github_Auth_Endpoint": "https://github.com/login/oauth",
  "Github_API_Endpoint": "https://api.github.com",
  "Github_Client_Id": "<client_id>",
  "Github_Secret": "<secret_id>"
}
```

## How to authenticate

```
path: /porper/auth
method : POST
# when authenticating using Google+ accounts
data:
{
  "provider": "google",
  "id_token": "<id_token value returned from Google Auth>"
}
# when authenticating using GitHub accounts
data:
{
  "provider": "github",
  "code": "<code value returned from GitHub Auth>",
  "state": "<state value returned from GitHub Auth>",
  "redirect_uri": "<registered redirect_url in GitHub Auth>"
}
```

## How to manage roles

### A couple of roles will be created during the database initialization
```
('435a6417-6c1f-4d7c-87dd-e8f6c0effc7a','public')
('ffffffff-ffff-ffff-ffff-ffffffffffff','admin')
```

### To create a new role
you must be the admin
```
path: /porper/role
method : POST
data:
{
  "name": "<name_of_the_role>"
}
```

### To find roles
```
path: /porper/role
method: GET
```
> if you're the admin, it will return all roles

> otherwise, return all roles where you're belong

```
path: /porper/role?id=<role_id>
method: GET
```
> It will return the role with the given id


## How to manage users

The first user logging into the system will be added as an admin automatically

### To invite users
you have to invite them first and you must be either the admin or the role admin of the role where the new user will belong
```
path: /porper/invited_user
method: POST
data
{
  "email": "<email_address>",
  "role_id": "<role_id>",
  "is_admin": "<0_or_1>"
}
```

### To find invited users
```
path: /porper/invited_user
method: GET
```
> if you're the admin, it will return all invited users

> if you're the role admin of one or more roles, it will return all invited users of the roles where you're the role admin

> otherwise, it will raise an exception of 'not permitted'

```
path: /porper/invited_user?role_id=<role_id>
method: GET
```
> if you're the admin or a role admin of the given role, it will return all invited users of the given role

> otherwise, it will raise an exception of 'not permitted'

Once the invited users log in successfully for the first time, they will be automatically registered and added to the roles specified during invitation


### To find registered user
```
path: /porper/user
method: GET
```
> if you're the admin, it will return all users

> if you're the role admin of one or more roles, it will return all users of the roles where you're the role admin

> otherwise, it will return yourself

```
path: /porper/user?role_id=<role_id>
method: GET
```
> if you're the admin or a member of the given role, it will return all users of the given role

> otherwise, it will raise an exception of 'not permitted'

```
path:
/porper/user?id=<id>
/porper/user?email=<email_address>
method: GET
```
> It will return a specific user with the given id or email address


### To assign a user to a role
```
path: /porper/user
method: POST
data:
{
  "user_id": "<user_id>",
  "role_id": "<role_id>",
  "is_admin": "<0 or 1>"
}
```


## Sungard Availability Services | Labs
[![Sungard Availability Services | Labs][labs-image]][labs-github-url]

This project is maintained by the Labs team at [Sungard Availability
Services][sungardas-url]

GitHub: [https://sungardas.github.io][sungardas-github-url]

Blog: [http://blog.sungardas.com/CTOLabs/][sungardaslabs-blog-url]

[porper-image]: https://github.com/SungardAS/porper-core/blob/develop/docs/images/logo.png?raw=true
[porper-core-url]: https://github.com/SungardAS/porper-core
[labs-github-url]: https://sungardas.github.io
[labs-image]: https://raw.githubusercontent.com/SungardAS/repo-assets/master/images/logos/sungardas-labs-logo-small.png
[sungardas-github-url]: https://sungardas.github.io
[sungardas-url]: http://sungardas.com
[sungardaslabs-blog-url]: http://blog.sungardas.com/CTOLabs/
