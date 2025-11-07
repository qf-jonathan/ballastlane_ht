# Pokedex Application

A full-stack Pokedex application with a FastAPI backend and Next.js frontend.

## Project Structure

```
ballastlane_ht/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── models/   # Database models (User, Pokemon)
│   │   ├── routes/   # API routes
│   │   ├── services/ # Business logic
│   │   └── schemas/  # Pydantic schemas
│   └── seed_pokemon.py  # Script to populate Pokemon database
└── frontend/         # Next.js frontend
    └── app/
        ├── components/    # React components
        ├── store/         # Zustand state management
        └── pokedex/       # Pokedex pages
```

## Backend Setup

### Prerequisites
- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies (uv will automatically create a virtual environment):
   ```bash
   uv sync
   ```

3. Initialize the database and seed Pokemon data:
   ```bash
   uv run python seed_pokemon.py
   ```
   This will fetch all Pokemon from PokeAPI and store them in the local database.

4. Start the backend server:
   ```bash
   uv run serve
   # or
   uv run python main.py
   ```

   The backend will be available at `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

### Backend API Endpoints

#### Pokemon Endpoints
- `GET /api/pokemon` - Get paginated list of Pokemon
  - Query params: `offset`, `limit`, `query` (for search)
- `GET /api/pokemon/{name_or_id}` - Get Pokemon details

#### Auth Endpoints
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

#### Admin Endpoints
- `GET /api/admin/users` - Get all users (admin only)
- `DELETE /api/admin/users/{user_id}` - Delete user (admin only)

## Frontend Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment configuration (already created):
   ```bash
   # .env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## Running the Full Application

1. **Start the Backend** (in one terminal):
   ```bash
   cd backend
   uv run serve
   ```

2. **Start the Frontend** (in another terminal):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Features

### Backend
- ✅ FastAPI with async/await support
- ✅ SQLite database with Tortoise ORM
- ✅ JWT authentication
- ✅ User management (registration, login)
- ✅ Pokemon data stored in local database
- ✅ Search and filter Pokemon
- ✅ Pagination support
- ✅ CORS enabled for frontend

### Frontend
- ✅ Next.js 15 with App Router
- ✅ TypeScript
- ✅ Tailwind CSS for styling
- ✅ Zustand for state management
- ✅ Server-side rendering for Pokemon details
- ✅ Client-side search and filtering
- ✅ Responsive design
- ✅ Image optimization with Next.js Image

## Key Changes

### Database Integration
The application now uses a local SQLite database instead of making direct calls to PokeAPI:

1. **Pokemon Model** (`backend/app/models/pokemon.py`):
   - Stores Pokemon data: id, name, sprites, types, abilities, stats
   - JSON fields for complex data structures

2. **Seed Script** (`backend/seed_pokemon.py`):
   - Fetches all 1328+ Pokemon from PokeAPI
   - Populates local database
   - Can be re-run safely (skips existing Pokemon)

3. **Pokemon Service** (`backend/app/services/pokemon_service.py`):
   - All methods now query the database instead of PokeAPI
   - Faster response times
   - Better search functionality with database queries
   - No external API dependencies

### Frontend Integration
The frontend now communicates exclusively with the backend API:

1. **Environment Configuration**:
   - `NEXT_PUBLIC_API_URL` points to backend API

2. **Pokemon Store** (`frontend/app/store/pokemonStore.ts`):
   - Updated to use backend API endpoints
   - Added search functionality

3. **Components**:
   - Updated to use backend API for all Pokemon data
   - Server-side rendering still works for SEO

## Development Notes

### Backend Commands
```bash
# Run server
uv run serve

# Seed database
uv run python seed_pokemon.py

# Run Python shell with app context
uv run python shell.py

# Run tests (if available)
uv run pytest
```

### Frontend Commands
```bash
# Development
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint
npm run lint
```

## Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **Tortoise ORM** - Async ORM for Python
- **SQLite** - Lightweight database
- **Pydantic** - Data validation
- **JWT** - Authentication
- **HTTPX** - Async HTTP client (for initial data seeding)

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **Zustand** - State management
- **Next.js Image** - Image optimization

## License

MIT
