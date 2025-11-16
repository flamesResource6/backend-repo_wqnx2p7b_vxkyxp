from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Inquiry

app = FastAPI(
    title="Impact Avenue API",
    description="Backend API for Impact Avenue website",
    version="1.0.0",
)

# CORS configuration - allow frontend URL to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"status": "ok", "service": "Impact Avenue API"}

@app.get("/test")
def test_db():
    # Basic DB connectivity check
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    return {"status": "ok", "db": True}

# Contact / Inquiry endpoint
@app.post("/inquiries")
def create_inquiry(inquiry: Inquiry):
    try:
        inquiry_id = create_document("inquiry", inquiry)
        return {"success": True, "id": inquiry_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Public content endpoints (static for MVP)
class Program(BaseModel):
    id: str
    category: str
    name: str
    duration: str
    description: str

PROGRAMS: List[Program] = [
    Program(id="p1", category="Technical", name="Networking Essentials", duration="3 days", description="Hands-on fundamentals of modern networks, security, and troubleshooting."),
    Program(id="p2", category="Technical", name="Introduction to AI", duration="2 days", description="Practical AI concepts, prompting, and responsible implementation."),
    Program(id="p3", category="Leadership", name="Leading with Impact", duration="2 days", description="Core leadership frameworks, influence and communication skills."),
    Program(id="p4", category="Soft Skills", name="High-Impact Communication", duration="1 day", description="Storytelling, presentation and stakeholder engagement."),
    Program(id="p5", category="Corporate Programs", name="Manager Accelerator", duration="6 weeks", description="Blended learning program to upskill first-time managers."),
]

@app.get("/programs", response_model=List[Program])
def list_programs(category: Optional[str] = None):
    if category:
        return [p for p in PROGRAMS if p.category.lower() == category.lower()]
    return PROGRAMS

class Testimonial(BaseModel):
    name: str
    role: str
    quote: str
    photo: Optional[str] = None

TESTIMONIALS: List[Testimonial] = [
    Testimonial(name="Ama Boateng", role="HR Director, FinServe", quote="Impact Avenue transformed our leadership bench. The facilitation was world-class."),
    Testimonial(name="Kwesi Mensah", role="IT Manager, TechHub", quote="The technical training was practical and immediately applicable."),
    Testimonial(name="Nana Adjei", role="Founder, GrowthX", quote="Our teams are communicating better than ever. Highly recommend."),
]

@app.get("/testimonials", response_model=List[Testimonial])
def list_testimonials():
    return TESTIMONIALS
