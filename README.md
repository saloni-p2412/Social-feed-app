# Social Feed Application

A simple social feed experience built with Django (backend) and Vue.js (frontend) that allows users to view posts, create new posts, and consume rich media content.

## Features

- **Feed View**: View all published posts in chronological order (latest first)
- **Create Post**: Create new posts with text content and multiple images/videos
- **Media Rendering**: 
  - Images displayed in a gallery with modal preview
  - Videos playable inline
  - Lazy loading for optimized performance
- **File Validation**: Validates file formats and size limits

## Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Frontend**: Vue.js 3, Vite
- **Deployment**: 
  - Backend: Render.com
  - Frontend: Vercel.com

## Project Structure

```
social-feed-app/
├── backend/          # Django backend API
│   ├── socialfeed/   # Django project settings
│   ├── posts/        # Posts app with models, views, serializers
│   └── requirements.txt
└── frontend/         # Vue.js frontend
    ├── src/
    │   ├── components/
    │   ├── views/
    │   └── api/
    └── package.json
```

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API URL
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173/`

## API Endpoints

### GET /api/posts/
Returns a list of all published posts in chronological order.

### POST /api/posts/
Creates a new post.

**Request:**
- `text_content` (string, optional): Text content of the post
- `media` (file[], optional): Multiple image/video files
- `published` (boolean, default: true): Whether the post is published

**Supported formats:**
- Images: JPEG, PNG, GIF, WebP
- Videos: MP4, WebM, OGG
- Max file size: 50MB

## Deployment

### Backend (Render.com)

1. Push your code to a Git repository
2. Connect the repository to Render.com
3. Create a new Web Service
4. Use the following settings:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn socialfeed.wsgi:application`
   - Environment Variables: Set `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, and `CORS_ALLOWED_ORIGINS`

### Frontend (Vercel.com)

1. Push your code to a Git repository
2. Connect the repository to Vercel
3. Set environment variable `VITE_API_BASE_URL` to your backend API URL
4. Deploy

## Development Notes

- The backend uses SQLite for development (change to PostgreSQL for production)
- Media files are stored in the `media/` directory
- CORS is configured to allow requests from the frontend
- Images use lazy loading for performance
- Videos use `preload="metadata"` to optimize loading
