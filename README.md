# Jewellery_Backend
Backend set up for Jewellery store search

endpoints:
# API / Endpoints Documentation

## Public Endpoints

| Endpoint       | Method(s)    | Destination (View)  | Description                                                      |
|----------------|-------------|-------------------|------------------------------------------------------------------|
| `/`            | GET         | `welcome_view`     | Shows the welcome page (landing page).                           |
| `/register/`   | GET, POST   | `register_view`    | Displays registration form (GET) and handles user signup (POST). |
| `/login/`      | GET, POST   | `login_view`       | Displays login form (GET) and authenticates user (POST).         |
| `/logout/`     | POST        | `logout_view`      | Logs out the current user and redirects to welcome page.         |

## Authenticated User Endpoints (require login)

| Endpoint       | Method(s)    | Destination (View)  | Description                                         |
|----------------|-------------|-------------------|-----------------------------------------------------|
| `/dashboard/`  | GET         | `dashboard_view`  | Shows user’s dashboard with personal info and items. |
| `/insert/`     | POST        | `insert_item`     | Inserts/creates a new item.                         |
| `/update/`     | POST / PUT  | `update_item`     | Updates an existing item.                            |
| `/delete/`     | POST / DELETE | `delete_item`   | Deletes an existing item.                            |

**Note:** For better REST-style design, consider using `/items/` endpoints:
- `POST /items/` → create item  
- `PUT /items/<id>/` → update item  
- `DELETE /items/<id>/` → delete item  
- `GET /items/` → list items
