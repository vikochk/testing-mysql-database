import string

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.test_data_model import TestData, ConfigData
from src.utils.logger import Logger
from src.utils.random_generation import RandomGeneration
from src.utils.test_data_provider import TestDataProvider
from src.utils.work_with_db import WorkWithDB


@pytest.fixture(scope='session')
def config_data():
    return TestDataProvider.get_test_data(
        TestDataProvider.CONFIG_DATA_FILENAME, ConfigData
    )

@pytest.fixture(scope='session')
def test_data():
    return TestDataProvider.get_test_data(
        TestDataProvider.TEST_DATA_FILENAME, TestData
    )

@pytest.fixture(scope='session')
def session_key():
    return RandomGeneration.generate_string(base_chars=string.digits)

@pytest.fixture(scope='session')
def db_engine(config_data):
    DB_URL = (
        f"mysql+pymysql://{config_data.db_username}:{config_data.db_password}@"
        f"{config_data.db_host}:{config_data.db_port}/{config_data.db_name}"
    )
    engine = create_engine(DB_URL)
    yield engine
    engine.dispose()

@pytest.fixture(scope='function')
def db_session(db_engine):
    session_factory = sessionmaker(bind=db_engine)
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()