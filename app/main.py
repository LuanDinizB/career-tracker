from fastapi import FastAPI
from app.routes import companies, jobs, applications, metrics

app = FastAPI(
    title="Career Tracker API",
    description="API para controle de candidaturas e vagas",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(companies.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(metrics.router)