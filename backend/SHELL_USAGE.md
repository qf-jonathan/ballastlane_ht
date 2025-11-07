# Interactive Shell Usage Guide

The Pokedex API includes an IPython-based interactive shell (similar to Django's `python manage.py shell`) that provides direct access to all models, services, and utilities.

## Starting the Shell

```bash
python shell.py
```

## Features

- ✅ **Auto-imported models** - All models are pre-loaded
- ✅ **Services available** - AuthService and UserService ready to use
- ✅ **Async/await support** - Top-level await enabled
- ✅ **Syntax highlighting** - IPython color coding
- ✅ **Tab completion** - Auto-complete for all objects
- ✅ **Command history** - Navigate previous commands with arrow keys

## Available Objects

### Models
- `User` - User model with full ORM access

### Services
- `AuthService` - Authentication operations
- `UserService` - User CRUD operations

### Schemas
- `UserCreate`, `UserUpdate`, `UserResponse`
- `UserLogin`, `Token`

### Security Utilities
- `create_access_token(data: dict) -> str`
- `decode_access_token(token: str) -> dict`
- `get_password_hash(password: str) -> str`
- `verify_password(plain: str, hashed: str) -> bool`

### Configuration
- `settings` - Application settings

## Common Tasks

### 1. Query Users

```python
# Get all users
users = await User.all()
print(users)

# Get specific user
admin = await User.filter(username="admin").first()
print(admin)

# Get user by ID
user = await User.get(id=1)

# Filter users
active_users = await User.filter(is_active=True)
admins = await User.filter(is_admin=True)

# Count users
total = await User.all().count()
print(f"Total users: {total}")
```

### 2. Create Users

```python
# Create a regular user
user = await User.create(
    username="newuser",
    email="newuser@example.com",
    hashed_password=get_password_hash("password123"),
    is_active=True,
    is_admin=False
)
print(f"Created user: {user.username}")

# Create an admin user
admin = await User.create(
    username="newadmin",
    email="newadmin@example.com",
    hashed_password=get_password_hash("admin123"),
    is_active=True,
    is_admin=True
)
```

### 3. Update Users

```python
# Get and update user
user = await User.get(username="testuser")
user.email = "newemail@example.com"
await user.save()

# Update multiple fields
user.is_admin = True
user.is_active = False
await user.save()
```

### 4. Delete Users

```python
# Delete a user
user = await User.get(username="testuser")
await user.delete()

# Or using filter
await User.filter(username="testuser").delete()
```

### 5. Authentication Testing

```python
# Login user
token = await AuthService.login("admin", "admin123")
print(f"Access token: {token.access_token}")

# Verify token
user = await AuthService.get_current_user(token.access_token)
print(f"Authenticated as: {user.username}")

# Check if user is admin
try:
    admin = await AuthService.get_current_admin_user(token.access_token)
    print(f"{admin.username} is an admin")
except Exception as e:
    print(f"Not an admin: {e}")
```

### 6. Password Operations

```python
# Hash a password
hashed = get_password_hash("mypassword")
print(f"Hashed: {hashed}")

# Verify password
is_valid = verify_password("mypassword", hashed)
print(f"Password valid: {is_valid}")

# Change user password
user = await User.get(username="testuser")
user.hashed_password = get_password_hash("newpassword")
await user.save()
```

### 7. Using UserService

```python
# Create user via service
from app.schemas.user import UserCreate

user_data = UserCreate(
    username="serviceuser",
    email="service@example.com",
    password="password123",
    is_admin=False
)
user = await UserService.create_user(user_data)

# Get all users
users = await UserService.get_all_users()

# Update user
from app.schemas.user import UserUpdate

update_data = UserUpdate(email="updated@example.com")
updated = await UserService.update_user(user.id, update_data)

# Delete user
await UserService.delete_user(user.id)
```

### 8. Complex Queries

```python
# Get users with multiple filters
recent_admins = await User.filter(
    is_admin=True,
    is_active=True,
    created_at__gte="2024-01-01"
)

# Use Q objects for OR queries
from tortoise.expressions import Q

users = await User.filter(
    Q(is_admin=True) | Q(username="testuser")
)

# Order results
users = await User.all().order_by("-created_at")

# Limit results
first_5 = await User.all().limit(5)

# Offset and limit (pagination)
page_2 = await User.all().offset(10).limit(10)
```

### 9. Bulk Operations

```python
# Bulk create
users_data = [
    {
        "username": f"user{i}",
        "email": f"user{i}@example.com",
        "hashed_password": get_password_hash("password"),
        "is_active": True,
        "is_admin": False
    }
    for i in range(10)
]

await User.bulk_create([User(**data) for data in users_data])

# Bulk update
await User.filter(is_active=False).update(is_active=True)

# Bulk delete
await User.filter(username__startswith="user").delete()
```

### 10. Token Operations

```python
# Create custom token
token = create_access_token({"sub": "admin", "custom": "data"})

# Decode token
payload = decode_access_token(token)
print(payload)

# Check token expiration
import datetime
token_with_expiry = create_access_token(
    {"sub": "admin"},
    expires_delta=datetime.timedelta(hours=1)
)
```

## Tips

1. **Tab Completion**: Press `Tab` to auto-complete model names, methods, etc.
2. **History**: Use ↑↓ arrow keys to navigate command history
3. **Help**: Type `help(User)` or `User?` for documentation
4. **Variables**: Assigned variables persist throughout the session
5. **Exit**: Type `exit` or press `Ctrl+D` to exit

## Common Errors

### "RuntimeError: Event loop is closed"
This happens if you try to run async code after the loop closes. Restart the shell.

### "tortoise.exceptions.OperationalError"
Database connection issue. Make sure `db.sqlite3` is accessible.

### "AttributeError: 'NoneType' object has no attribute..."
Usually means a query returned `None`. Always check if object exists:

```python
user = await User.filter(username="nonexistent").first()
if user:
    print(user.email)
else:
    print("User not found")
```

## Example Session

```python
# Start shell
$ python shell.py

# Create a test user
In [1]: user = await User.create(
   ...:     username="shelltest",
   ...:     email="shell@test.com",
   ...:     hashed_password=get_password_hash("test123"),
   ...:     is_active=True
   ...: )

# Login
In [2]: token = await AuthService.login("shelltest", "test123")

In [3]: print(token.access_token)
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Verify authentication
In [4]: current = await AuthService.get_current_user(token.access_token)

In [5]: print(f"Logged in as: {current.username}")
Logged in as: shelltest

# Clean up
In [6]: await user.delete()

In [7]: exit
```

## Advanced Usage

### Database Transactions

```python
from tortoise.transactions import in_transaction

async with in_transaction() as conn:
    user = await User.create(
        username="transactional",
        email="trans@example.com",
        hashed_password=get_password_hash("password"),
        using_db=conn
    )
    # If exception occurs, changes are rolled back
```

### Raw SQL

```python
from tortoise import connections

conn = connections.get("default")
results = await conn.execute_query_dict(
    "SELECT * FROM users WHERE is_admin = ?", [True]
)
print(results)
```

### Performance Profiling

```python
import time

start = time.time()
users = await User.all()
elapsed = time.time() - start
print(f"Query took {elapsed:.4f} seconds")
```

## Troubleshooting

If the shell doesn't start or behaves unexpectedly:

1. Make sure the database is initialized: `python seed_db.py`
2. Check that IPython is installed: `uv list | grep ipython`
3. Verify the database file exists: `ls db.sqlite3`
4. Try restarting the shell

For more help, check the main README or API documentation at `/docs` when the server is running.
