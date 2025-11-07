# Pokédex Frontend Application

A modern Pokémon application built with Next.js, featuring authentication and Pokémon search functionality.

## Features

- **Authentication**: Secure login using JWT tokens from the backend API
- **Pokémon Search**: Search and browse Pokémon with real-time filtering
- **Detailed Views**: View detailed information about each Pokémon including stats, abilities, and types
- **Responsive Design**: Mobile-first design that works on all screen sizes
- **Type-based Theming**: Dynamic colors based on Pokémon types
- **Infinite Scroll**: Automatically loads more Pokémon as you scroll

## Design System

The application uses a light theme with the Poppins font family and follows a Pokédex-inspired design:

### Colors
- Primary: #DC0A2D (Pokédex Red)
- 18 Pokémon type colors (grass, fire, water, etc.)
- Grayscale palette for UI elements

### Typography
- Font Family: Poppins (Regular 400, Medium 500, Bold 700)
- Clear hierarchy with defined sizes for headings and body text

## Tech Stack

- **Framework**: Next.js 16.0.1 with App Router
- **State Management**: Zustand
- **Styling**: CSS Modules
- **Language**: TypeScript
- **API Client**: Custom fetch-based client

## Getting Started

### Prerequisites

- Node.js (using nvm)
- Backend API running at `http://localhost:8000`

### Installation

```bash
npm install
```

### Environment Variables

Create a `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Running the Application

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Default Credentials

For testing, use these credentials:
- Username: `admin`
- Password: `admin123`

Or:
- Username: `testuser`
- Password: `test1234`

## Project Structure

```
frontend/
├── app/
│   ├── pokemon/[id]/     # Dynamic Pokémon details page
│   ├── globals.css       # Design system & CSS variables
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Home page with auth check
├── components/           # React components
│   ├── Header.tsx
│   ├── LoginForm.tsx
│   ├── PokemonCard.tsx
│   ├── PokemonGrid.tsx
│   ├── SearchBar.tsx
│   └── TypeChip.tsx
├── lib/
│   └── api.ts           # API client
├── stores/              # Zustand stores
│   ├── authStore.ts     # Authentication state
│   └── pokemonStore.ts  # Pokémon data state
└── types/
    └── index.ts         # TypeScript type definitions
```

## Key Features

### Authentication Flow
1. User lands on home page
2. If not authenticated, shows login form
3. On successful login, token is stored in localStorage
4. User sees Pokémon grid with search functionality
5. Can sign out via header button

### Pokémon Features
- **Search**: Real-time search with 300ms debounce
- **Infinite Scroll**: Automatically loads next page when scrolling to bottom
- **Details Page**: Click any Pokémon to see detailed stats, abilities, and information
- **Type-based Styling**: Each Pokémon card and detail page uses colors matching its primary type

## API Integration

The frontend integrates with the following backend endpoints:

- `POST /auth/login/json` - User login
- `GET /auth/me` - Get current user
- `GET /pokemon` - List Pokémon (with pagination and search)
- `GET /pokemon/{name_or_id}` - Get Pokémon details
