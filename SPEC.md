# SPEC.md - Group Manager App

## Project Overview
- **Project Name**: OpenGroups
- **Type**: Web Application (FastAPI + Vue.js)
- **Core Functionality**: Search and join groups with fuzzy search, admin panel for creating groups
- **Target Users**: General users looking to join groups, admins to create groups

## UI/UX Specification

### Color Palette
- **Primary/Background**: `#161b22` (dark blue-gray)
- **Text Primary**: `#ffffff` (white)
- **Text Secondary**: `#8b949e` (light gray)
- **Accent/Buttons**: `#21bc62` (green)
- **Card Background**: `#21262d` (slightly lighter than primary)
- **Card Hover**: `#30363d`

### Typography
- **Font Family**: System fonts (Segoe UI, Roboto, sans-serif)
- **Heading Size**: 24px (title), 18px (card titles)
- **Body Size**: 14px
- **Font Weight**: 400 (normal), 600 (bold)

### Layout Structure
- **Header**: Fixed top, 60px height, logo/title left, create group button right
- **Search Bar**: Centered, 400px width, full-width on mobile
- **Groups Grid**: CSS Grid, 3 columns desktop, 2 tablet, 1 mobile
- **Cards**: 280px min-width, padding 20px, border-radius 12px
- **Responsive Breakpoints**: 768px (tablet), 480px (mobile)

### Components

#### Header
- Logo/Title: configurable via `APP_NAME` (default "Groups")
- Button: "Crear Grupo" (visible when admin authenticated)

#### Search Bar
- Placeholder: "Buscar grupos..."
- Icon: Search icon left
- Clear button when text present

#### Group Card
- Border-radius: 12px
- Background: `#21262d`
- Padding: 20px
- Shadow: subtle
- Content:
  - Group name (18px, bold, white)
  - Description (14px, gray)
  - "Unirse al Grupo" button (green, full width)

#### Create Group Modal
- Password input
- Group name input
- Description input
- Submit button

## Functionality Specification

### Core Features

#### 1. Group Search (fuzzy)
- Fuzzy search with typo tolerance
- Search by group name and description
- Real-time filtering as user types
- Debounce: 200ms

#### 2. Group Listing
- Display all groups as cards
- Responsive grid layout

#### 3. Join Group
- Group with a URL links out; otherwise a confirmation toast

#### 4. Admin Panel (Create Group)
- Password protection from `ADMIN_PASSWORD`
- Max 3 attempts before 24-hour lockout
- Lockout stored in memory with timestamp
- Form fields: group name, description, url
- Validation: name required, min 3 chars

### Data Model
```python
Group:
  - id: int
  - name: str
  - description: str
  - url: str
  - pinned: bool
  - created_at: datetime
  - tags: list[Tag]

Tag:
  - id: int
  - name: str
  - created_at: datetime

ImportantLink:
  - id: int
  - title: str
  - description: str
  - url: str
  - created_at: datetime
```

### API Endpoints
- `GET /api/groups` - List/search groups
- `POST /api/groups` - Create new group (requires admin)
- `POST /api/admin/login` - Verify admin password
- `GET /api/admin/status` - Check lockout status
- `GET /api/config` - Branding configuration

### Edge Cases
- Empty search results: Show "No se encontraron grupos"
- Network error: Show error toast
- Lockout active: Show countdown timer

## Acceptance Criteria

1. Search bar filters groups in real-time with fuzzy matching
2. Groups display as cards with name and join button
3. Join button opens the group URL or shows a confirmation toast
4. Admin panel accessible via password from the environment
5. 3 failed attempts = 24 hour lockout
6. Responsive design works on mobile/tablet/desktop
7. Branding is fully configurable via environment variables
8. FastAPI backend serves the Vue.js frontend
