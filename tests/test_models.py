from sqlalchemy.orm import configure_mappers

from app.models import Base


def test_all_mappers_configure():
    configure_mappers()
    assert len(Base.metadata.tables) == 20
