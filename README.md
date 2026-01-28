# Reiya-Real-Estate-Full-Stack-Analyzer-Project
It is a full-stack AI platform that converts raw real estate data into investment intelligence and the property, street,
neighborhood, and ISD level.

Features:
- Property Intelligence Report: Deep analysis of individual properties and their history.
- Street Comparision: Compare properties with other properties on the street in terms of size and valuation (No one wants the smallest house in the street !)
- Neighborhood Analysis: Macro level trend analysis of neighborhoods and their trends
- AI Audit Reports: Investment-grade analysis with ML predictions
- Interactive Maps: Visual property exploration with Mapbox
- Demand & Supply Modeling: Predictive analusis for market trends and property future.

Tech Stack:
Frontend:
-Next.js
-TypeScript
-Tailwind CSS
-Framer Motion
-D3.js
-Mapbox Gl JS

Backend:
-FastAPI
-PostgreSQL + PostGIS
-Redis
-OpenAI API
-Multiple Real Estate APIs

Required API: (More can be added but these are required)
-ATTOM API
-OpenAI API
-Mapbox
-Realtor API
-Google Places API
-US Census API

Project Structure:
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

This was a project I developed during the winter storm in January 2026, it is a good experiment that involves me playing with multiple APIs involving complex analytical features as well as intuitive and functional UI.
Built with love for real estate enthusiasts!!
