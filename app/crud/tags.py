# app/crud/tags.py
from sqlalchemy.orm import Session
from app.models.tags import Tag
from app.schemas.tags import TagCreate

def get_tags(session: Session, tags: List[str]):
    tag_objects = []
    for tag_name in tags:
        tag_object = session.query(Tag).filter(Tag.name == tag_name).first()
        if not tag_object:
            tag_object = Tag(name=tag_name)
            session.add(tag_object)
        tag_objects.append(tag_object)
    session.commit()
    return tag_objects