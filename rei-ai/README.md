# REI-AI: Real Estate Intelligence & Analytics Platform

A full-stack AI platform that converts raw real estate data into quantitative investment intelligence at the property, street, neighborhood, and ISD level.

## 🚀 Features

- **Property Intelligence**: Deep analysis of individual properties
- **Street Comparison**: Compare properties against street averages
- **Neighborhood Analytics**: Macro-level trend analysis
- **AI Audit Reports**: Investment-grade analysis with ML predictions
- **Interactive Maps**: Visual property exploration with Mapbox
- **Demand-Supply Modeling**: Predictive analytics for market trends

## 🏗️ Tech Stack

### Frontend
- Next.js 14 (React)
- TypeScript
- Tailwind CSS
- Framer Motion
- D3.js & Recharts
- Mapbox GL JS

### Backend
- FastAPI (Python)
- PostgreSQL + PostGIS
- Redis (caching)
- OpenAI API (AI analysis)
- Multiple real estate data APIs

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 14+ with PostGIS extension
- Redis (optional, for caching)

## 🔑 Required API Keys

1. **ATTOM API** (Primary data source)
   - Sign up at: https://api.attomdata.com/
   - Get API key from dashboard

2. **OpenAI API** (AI analysis)
   - Sign up at: https://platform.openai.com/
   - Create API key

3. **Mapbox** (Maps)
   - Sign up at: https://www.mapbox.com/
   - Get access token

4. **Optional APIs**:
   - Realtor API (RapidAPI)
   - Google Places API
   - US Census API (free, no key needed for basic use)

## ⚡ Quick Start

### 1. Clone and Install

```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### 2. Configure Environment Variables

**Backend** (`backend/.env`):
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/rei_ai
REDIS_URL=redis://localhost:6379

# APIs
ATTOM_API_KEY=your_attom_key_here
OPENAI_API_KEY=your_openai_key_here
REALTOR_API_KEY=your_realtor_key_here
GOOGLE_PLACES_API_KEY=your_google_key_here

# App Settings
ENVIRONMENT=development
DEBUG=True
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token_here
```

### 3. Initialize Database

```bash
cd backend
python scripts/init_db.py
```

### 4. Run the Application

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

Visit: http://localhost:3000

## 📁 Project Structure

```
rei-ai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # Database connection
│   │   ├── models/              # Database models
│   │   ├── services/            # Business logic
│   │   │   ├── property_service.py
│   │   │   ├── analytics_service.py
│   │   │   ├── ai_service.py
│   │   │   └── data_service.py
│   │   ├── routers/             # API endpoints
│   │   └── utils/               # Utilities
│   ├── scripts/
│   │   └── init_db.py           # Database initialization
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js app directory
│   │   ├── components/          # React components
│   │   ├── lib/                 # Utilities
│   │   └── types/               # TypeScript types
│   ├── public/
│   └── package.json
└── README.md
```

## 🎯 Usage

### 1. Search for Properties
- Enter a city (Plano, Frisco, Richardson)
- Browse properties on the interactive map
- Filter by price, size, features

### 2. View Property Analysis
- Click any property for deep analysis
- See street-level comparisons
- Review neighborhood trends
- Check AI valuation scores

### 3. Generate AI Audit
- Click "Generate AI Audit" on property page
- Get comprehensive investment analysis
- Download PDF report
- Compare multiple properties

## 🔧 Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Backend
black app/
flake8 app/

# Frontend
npm run lint
npm run type-check
```

## 🚢 Deployment

### Backend (Railway/Render/Fly.io)
1. Set environment variables
2. Deploy from GitHub
3. Run migrations

### Frontend (Vercel)
1. Connect GitHub repo
2. Set environment variables
3. Deploy

## 📊 Sample Data

The system includes sample data for Plano, TX to demonstrate features without API keys.

## 🤝 Contributing

This is a portfolio project. Feel free to fork and customize!

## 📄 License

MIT License - See LICENSE file

## 🙋 Support

For issues or questions, create a GitHub issue.

---

**Built with ❤️ for real estate investors**
