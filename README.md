# Todo API
simple Todo list API built with **python** and **django rest framework**

## *API Endpoint*
### for accounts app
| Method | Endpoint | Description |
| ------ | ------ | ------ |
| POST | accounts/register/ | to register user |
| POST | accounts/login/ | to login user |
| POST | accounts/logout/ | to logout user |
| GET | accounts/users/ | list of all users |
| GET | accounts/users/{id}/ | info of one user |
| PATCH | accounts/users/{id}/ | update user info |
| DELETE | accounts/users/{id}/ | delete user |

### for todos app
| Method | Endpoint | Description |
| ------ | ------ | ------ |
| GET | / | list of all todos |
| POST | /{id} | info of one todo |
| POST | /create/ | create a todo |
| PATCH | /update/{id}/ | update todo info |
| DELETE | /delete/{id}/ | delete todo |
| GET | /schema/(redoc OR swagger-ui) | document |




