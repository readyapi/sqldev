import uuid
from typing import Optional

from sqldev import Field, Session, SQLDev, create_engine, select

from tests.conftest import needs_pydanticv2


@needs_pydanticv2
def test_annotated_optional_types(clear_sqldev) -> None:
    from pydantic import UUID4

    class Hero(SQLDev, table=True):
        # Pydantic UUID4 is: Annotated[UUID, UuidVersion(4)]
        id: Optional[UUID4] = Field(default_factory=uuid.uuid4, primary_key=True)

    engine = create_engine("sqlite:///:memory:")
    SQLDev.metadata.create_all(engine)
    with Session(engine) as db:
        hero = Hero()
        db.add(hero)
        db.commit()
        statement = select(Hero)
        result = db.exec(statement).all()
    assert len(result) == 1
    assert isinstance(hero.id, uuid.UUID)
