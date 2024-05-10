from fastapi import FastAPI

# Documentation
from documentations.descriptions import api_description
from documentations.tags import tags_metadata

#import router
import routers.router_todoList
import routers.routers_auth

app = FastAPI(
    title="To do List",
    description=api_description,
    openapi_tags= tags_metadata
)

app.include_router(routers.router_todoList.router)
app.include_router(routers.routers_auth.router)

