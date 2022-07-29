from pydantic import BaseModel


class sites(BaseModel):
    id: int
    url_site: str


class all_json(BaseModel):
    sites: list[sites]
    limit_news: int 
