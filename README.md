# Pokedex Application

A full-stack Pokedex application with a FastAPI backend and Next.js frontend.

## Project Structure

```
ballastlane_ht/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── core/      # Configuration and settings
│   │   ├── models/    # Database models (User, Pokemon)
│   │   ├── routes/    # API routes
│   │   ├── services/  # Business logic
│   │   └── schemas/   # Pydantic schemas
│   ├── seed_pokemon.py  # Script to populate Pokemon database
│   └── main.py        # Application entry point
└── frontend/         # Next.js frontend
    ├── app/
    │   ├── login/     # Login page
    │   └── pokemon/   # Pokemon detail pages
    ├── components/    # React components
    ├── stores/        # Zustand state management
    ├── lib/           # Utilities (API client)
    └── types/         # TypeScript type definitions
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
  - Query params: `offset`, `limit`, `query` (for search), `sort_by` (id or name)
- `GET /api/pokemon/{name_or_id}` - Get Pokemon details by name or ID

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
- ✅ Next.js 16 with App Router
- ✅ TypeScript
- ✅ CSS Modules for styling
- ✅ Zustand for state management
- ✅ JWT authentication with protected routes
- ✅ Pokemon search and sorting (by ID or name)
- ✅ Infinite scroll pagination
- ✅ Responsive design with fixed header and search bar
- ✅ Custom design system with Pokemon type colors

## Key Changes

### Database Integration
The application now uses a local SQLite database instead of making direct calls to PokeAPI:

1. **Pokemon Model** (`backend/app/models/pokemon.py`):
   - Stores Pokemon data: id, name, description, sprites, types, abilities, stats, height, weight
   - JSON fields for complex data structures
   - Description field populated from pokemon-species flavor text

2. **Seed Script** (`backend/seed_pokemon.py`):
   - Fetches all 1328+ Pokemon from PokeAPI
   - Fetches Pokemon species data for descriptions
   - Populates local database with upsert logic
   - Can be re-run safely (updates existing Pokemon)

3. **Pokemon Service** (`backend/app/services/pokemon_service.py`):
   - Single `search_pokemon` method handles all queries (with optional query parameter)
   - All methods query the database instead of PokeAPI
   - Faster response times
   - Better search functionality with database queries (by name or ID)
   - Sorting support (by ID or name)
   - No external API dependencies during runtime

### Frontend Integration
The frontend now communicates exclusively with the backend API:

1. **Environment Configuration**:
   - `NEXT_PUBLIC_API_URL` points to backend API

2. **State Management** (`frontend/stores/`):
   - `pokemonStore.ts` - Pokemon list, search, sorting, and infinite scroll
   - `authStore.ts` - JWT authentication and user management

3. **Components**:
   - `Header` - Fixed header with user info and logout
   - `SearchBar` - Debounced search with inset shadow styling
   - `SortDropdown` - Sort Pokemon by ID or name
   - `PokemonGrid` - Infinite scroll grid with fixed search controls
   - `PokemonCard` - Card with type-based color accent and Pokemon image
   - `TypeChip` - Color-coded Pokemon type badges

4. **Design System**:
   - Custom CSS variables for 18 Pokemon types
   - Poppins font family
   - Inset shadows for depth
   - Primary red color (#DC0A2D) for borders and accents

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
- **Next.js 16** - React framework with App Router
- **TypeScript** - Type safety
- **CSS Modules** - Component-scoped styling
- **Zustand** - State management
- **Intersection Observer API** - Infinite scroll implementation

## License

MIT
