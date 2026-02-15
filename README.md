# Real-time-Leaderboard

Backend system for a real-time leaderboard service. The service will allow users to compete in various games or activities, track their scores, and view their rankings on a leaderboard

The system includes tic tac toe game for two players
After match end winner receive 15 pts and loser receive 5 points

Project based on <https://roadmap.sh/projects/realtime-leaderboard-system> challenge

---

## How to run the project

Requirements:

* Python 3.8=>

* PostgreSQL

* pip

* virtualenv

* Redis

---

### 1. Clone the repository

```bash
git clone https://github.com/xenoqd/Real-time-Leaderboard.git
cd Real-time-Leaderboard
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Linus / MacOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/leaderboard_service

POSTGRES_DB=leaderboard_service
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

SECRET_KEY = 
REFRESH_SECRET_KEY = 

ACCESS_TOKEN_EXPIRE_MINUTES = 120
REFRESH_TOKEN_EXPIRE_DAYS = 30
```

### 5. Apply database migrations

```bash
alembic upgrade head
```

### 6. Run development server

```bash
fastapi dev main.py
```

---

## Features

User Authentication

* User registration and login

* JWT based authentication stored in cookies

Leaderboard

* Top users in leaderboard by rank(score)

* Current user rank in leaderbaord

Match

* Create match in tic tac toe game

* Join match for second player

* Move in tic tak toe game

Scores

* You can check any other user points

Report

* You can check top players by specific period. If date not specified then usually it 7 days

## API Endpoints

Authentication
POST   /auth/register
POST   /auth/login

Match
POST   /match/
POST   /match/join/{match_id}
POST   /match/{match_id}/move

Leaderboard
GET    /leaderboard/top
GET    /leaderboard/me

Reports
GET    /reports?start_date=&end_date=
