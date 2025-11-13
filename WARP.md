# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Голосовой банковский ассистент (Voice Banking Assistant) - a full-stack application that provides AI-powered voice and text interactions for banking services. The system uses neural networks for context analysis, speech recognition, and user satisfaction scoring.

## Architecture

### Monorepo Structure
- `api/` - Flask-based REST API backend with MVC architecture
- `client/` - React + TypeScript frontend with Vite

### Backend (Flask + PostgreSQL)
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: PostgreSQL (via Docker)
- **Pattern**: MVC architecture
  - `Models/` - SQLAlchemy models (User, Message, Role, Department, RefreshToken, etc.)
  - `Controllers/` - Business logic handlers (UserController, MessageController, AudioController, RoleController, DepartmentController)
  - `utils/` - Helper functions (auth_helpers.py, jwt_utils.py)
- **Authentication**: JWT-based auth with refresh tokens and bcrypt password hashing
- **API Documentation**: Swagger/Flasgger at `/apidocs`
- **AI Integration**: 
  - GPT-based conversational AI via g4f library
  - Speech recognition using Google Speech Recognition (ru-RU)
  - Text-to-speech using gTTS

### Frontend (React + Vite)
- **Stack**: React 18, TypeScript, Vite, MUI (Material-UI)
- **Architecture**: Feature-based structure
  - `app/` - App setup, providers, router
  - `features/` - Feature modules (chat, auth, navigation, etc.)
  - `pages/` - Page components
  - `shared/` - Shared utilities and UI components
  - `entities/` - Business entities
- **Styling**: MUI theming for consistent design system
- **Linting**: ESLint (Airbnb config), Prettier, commitlint with Husky pre-commit hooks
- **Package Manager**: Yarn 4.1.1 (Berry)

## Development Commands

### Backend (API)
```bash
# From api/ directory
# Install dependencies
pip install -r requirements.txt

# Run with Docker (recommended)
docker-compose up --build -d

# Run locally (requires PostgreSQL)
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend (Client)
```bash
# From client/ directory
# Install dependencies
yarn install

# Development server with HMR
yarn dev

# Production build
yarn build

# Lint code
yarn lint

# Format code
yarn format

# Preview production build
yarn preview
```

Frontend development server runs on `http://localhost:5173` (default Vite port)

### Docker
```bash
# From api/ directory
docker-compose up --build -d    # Start all services (frontend on :80, backend on :5000, PostgreSQL on :5432)
docker-compose down              # Stop all services
```

## Database

### Connection
PostgreSQL connection string: `postgresql://root:root@db:5432/dbuild`

Environment variables should be configured in `api/.env`:
- Database credentials (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)

### Models and Relationships
- **User**: Many-to-many relationships with Role and Department via junction tables (UserRole, UserDepartment)
- **Message**: Stores conversation history with type (text/audio), sender (user/server), and session code
- **Role/Department**: User authorization entities
- **RefreshToken**: JWT refresh token management

Tables are auto-created via `db.create_all()` in app.py

## API Endpoints

Key endpoints (see `/apidocs` for full Swagger documentation):

**Users**: `/api/users/` (GET, POST), `/api/users/<id>` (GET, PUT)
**Roles**: `/api/roles/` (GET, POST), `/api/roles/<id>` (GET, PUT, DELETE)
**Departments**: `/api/departments/` (GET, POST), `/api/departments/<id>` (GET, PUT, DELETE)
**Auth**: `/api/auth/login`, `/api/auth/register`, `/api/auth/refresh`
**Messages**: `/api/messages/` (GET, POST), `/api/messages/<id>` (GET)
**Audio**: `/api/converttexttoaudio/` (POST)

## Code Standards

### Frontend
- **TypeScript**: Strict mode, no explicit `any`, no unused variables
- **Component Style**: Arrow functions for all components (functional components only)
- **Import Order**: Enforced by `simple-import-sort` (external → internal → relative)
- **Linting**: Airbnb + TypeScript rules, security checks, SonarJS cognitive complexity checks
- **Commits**: Conventional commits enforced via commitlint + Husky

### Backend
- **Language**: Python 3
- **ORM**: Use SQLAlchemy models, avoid raw SQL
- **Password Security**: Always use bcrypt hashing via User.set_password()
- **JWT**: Use utility functions from jwt_utils.py and auth_helpers.py
- **API Responses**: Return JSON with `{status, message, data}` structure

## Neural Network Integration

The AI system uses multiple neural networks:
1. **Context Analysis**: Determines dialog theme from text/audio input
2. **Topic-Specific Handlers**: Each banking topic has dedicated processing logic
3. **Satisfaction Scoring**: Analyzes conversation quality on 100-point scale
4. **Multi-format Support**: Text, audio-to-text (speech recognition), text-to-audio (gTTS)

Key functions:
- `audio_to_text()` - Converts audio to Russian text via Google Speech Recognition
- `request_gpt_simple()` - Sends prompts to GPT for banking assistant responses
- `text_to_audio()` - Converts text responses to Russian audio

## Common Development Workflows

### Adding a New API Endpoint
1. Create/modify model in `api/Models/` if needed
2. Add controller function in appropriate `api/Controllers/*Controller.py`
3. Add Swagger documentation via `@swag_from` decorator
4. Register route in `api/app.py`
5. Test via Swagger UI at `/apidocs`

### Adding a New Frontend Feature
1. Create feature directory in `client/src/features/`
2. Implement components using MUI and TypeScript
3. Export feature from `index.ts`
4. Integrate into router/pages as needed
5. Ensure ESLint passes: `yarn lint`

### Working with Docker Compose
The docker-compose.yml in api/ orchestrates three services:
- `webclieng` (frontend container on port 80)
- `web` (backend container on port 5000)
- `db` (PostgreSQL on port 5432)

Backend depends on database; changes to api/ directory are volume-mounted for development.

## Notes

- The frontend was originally developed in a separate repository (see README for link)
- Russian language is used throughout the application (prompts, speech recognition, responses)
- Session management uses 4-character codes stored with messages
- Audio files are temporarily stored as `output_audio.wav` in api directory
