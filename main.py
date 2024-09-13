#172.20.1.197
#uvicorn main:app --reload --host 172.20.1.197 --port 8000
from fastapi import FastAPI
import motor.motor_asyncio
from starlette.middleware.cors import CORSMiddleware
from env import MONGODB_URL, FRONTEND_ORIGINS
from typing import Annotated, Optional, List
from pydantic import BaseModel, BeforeValidator, Field, ConfigDict


app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.get_database('Portfolio')
projectCollection = db.get_collection('Projects')
PyObjectId = Annotated[str, BeforeValidator(str)]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGINS],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class ProjectModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    description: str = Field(...)
    imagePath: str = Field(...)
    timeFrame: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

class ProjectCollection(BaseModel):
    projects: List[ProjectModel]


@app.get("/projects/", response_description="List of projects", response_model=ProjectCollection,response_model_by_alias=False)
async def list_projects():
    projects = await projectCollection.find().to_list(1000)
    return ProjectCollection(projects=projects)


@app.get("/")
async def root():
    return {"Hello World"}