from typing import Any, List, Union

import pytest
from sqldev import Field, Relationship, SQLDev


def test_ondelete_requires_nullable(clear_sqldev: Any) -> None:
    with pytest.raises(RuntimeError) as exc:

        class Team(SQLDev, table=True):
            id: Union[int, None] = Field(default=None, primary_key=True)

            heroes: List["Hero"] = Relationship(
                back_populates="team", passive_deletes="all"
            )

        class Hero(SQLDev, table=True):
            id: Union[int, None] = Field(default=None, primary_key=True)
            name: str = Field(index=True)
            secret_name: str
            age: Union[int, None] = Field(default=None, index=True)

            team_id: int = Field(foreign_key="team.id", ondelete="SET NULL")
            team: Team = Relationship(back_populates="heroes")

    assert 'ondelete="SET NULL" requires nullable=True' in str(exc.value)


def test_ondelete_requires_foreign_key(clear_sqldev: Any) -> None:
    with pytest.raises(RuntimeError) as exc:

        class Team(SQLDev, table=True):
            id: Union[int, None] = Field(default=None, primary_key=True)

            age: int = Field(ondelete="CASCADE")

    assert "ondelete can only be used with foreign_key" in str(exc.value)
