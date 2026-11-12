from pydantic import BaseModel


class ConfigData(BaseModel):
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str


class TestName(BaseModel):
    summation: str
    multiplication: str


class TestData(BaseModel):
    author_name: str
    project_name: str
    amount_of_tests_with_duplicates: int
    new_tests_names: TestName
    author_login: str | None = None
    author_email: str | None = None