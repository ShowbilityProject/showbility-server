# app/crud/tags.py
from sqlalchemy.orm import Session
from app.models.tags import Tag
from app.schemas.tags import TagResponse
from typing import List

def get_tags(session: Session, tags: List[str]) -> List[TagResponse]:
    tags = [tag.strip() for tag in tags[0].split(',')]
    tag_objects = []

    for tag_name in tags:
        tag_object = session.query(Tag).filter(Tag.name == tag_name).first()

        if tag_object:
            tag_objects.append(TagResponse(id=tag_object.id, name=tag_object.name))

    return tag_objects