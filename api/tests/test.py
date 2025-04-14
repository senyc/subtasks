import pytest
from datetime import datetime
from sqlmodel import Session, create_engine
from ..shared.shared import parse_ids_from_search
from ..db.db import Tag, TaskTag, Task

# Assuming you have a test database URL
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def test_db():
    engine = create_engine(TEST_DATABASE_URL)
    # Create the database tables
    Tag.metadata.create_all(engine)
    TaskTag.metadata.create_all(engine)
    Task.metadata.create_all(engine)

    with Session(engine) as session:
        # Add sample data
        tag = Tag(id=1, name="Daily", description="daily tasks")
        tag1 = Tag(id=2, name="Chores", description="chores")
        session.add(tag)
        session.add(tag1)
        session.commit()

        task1 = Task(
            id=1,
            title="Buy groceries",
            body="",
            due_date=datetime.strptime("2025-04-30", "%Y-%m-%d"),
            completed_date=datetime.strptime("2025-04-30", "%Y-%m-%d"),
        )
        task2 = Task(
            id=2,
            title="Read a book",
            body="",
            due_date=datetime.strptime("2025-04-30", "%Y-%m-%d"),
            completed_date=datetime.strptime("2025-04-30", "%Y-%m-%d"),
        )
        task3 = Task(
            id=3,
            title="Read another book",
            body="",
            due_date=datetime.strptime("2025-04-30", "%Y-%m-%d"),
            completed_date=datetime.strptime("2025-04-30", "%Y-%m-%d"),
        )
        session.add(task1)
        session.add(task2)
        session.add(task3)
        session.commit()

        task_tag1 = TaskTag(task_id=task1.id, tag_id=tag.id)
        task_tag2 = TaskTag(task_id=task2.id, tag_id=tag.id)
        task_tag3 = TaskTag(task_id=task3.id, tag_id=tag1.id)
        session.add(task_tag1)
        session.add(task_tag2)
        session.add(task_tag3)
        session.commit()

        yield session  # Provide the session to the test

        # Clean up the database after tests
        Tag.metadata.drop_all(engine)
        TaskTag.metadata.drop_all(engine)
        Task.metadata.drop_all(engine)


def test_get_ids_from_search(test_db):
    session = test_db
    search_input = "tag:Daily"

    # Call the function
    task_ids = parse_ids_from_search(search_input, session)[0]

    # Assert the expected output
    assert task_ids == [1, 2]  # Assuming task IDs are 1 and 2

    search_input = "tag:Chores,tag:Daily test"

    # Call the function
    task_ids = parse_ids_from_search(search_input, session)[0]

    # Assert the expected output
    assert task_ids == [3, 1, 2]  # Assuming task IDs are 1 and 2
