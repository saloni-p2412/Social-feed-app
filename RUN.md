# How to run the app (fix "Network Error")

You need **two terminals** running at the same time.

---

## Terminal 1 — Backend (required)

```bash
cd /Users/salonipatel/social-feed-app
./start-backend.sh
```

**Leave this terminal open.** You should see:

```
Starting development server at http://127.0.0.1:8000/
```

If the script fails, try instead:

```bash
cd /Users/salonipatel/social-feed-app/backend
./venv/bin/pip install -r requirements.txt
./venv/bin/python manage.py migrate
./venv/bin/python manage.py runserver
```

---

## Terminal 2 — Frontend

```bash
cd /Users/salonipatel/social-feed-app/frontend
npm run dev
```

**Leave this terminal open.** You should see:

```
Local:   http://localhost:5173/
```

---

## Browser

Open: **http://localhost:5173**

Create a post. If you see "Network Error", the backend (Terminal 1) is not running — start it and try again.
