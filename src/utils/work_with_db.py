from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.author_model import Author
from src.models.project_model import Project
from src.models.session_model import SessionModel
from src.models.status_model import Status
from src.models.test_model import Test
from src.utils.logger import Logger


class WorkWithDB:
    def __init__(self, session: Session, test_data):
        self.session = session
        self.test_data = test_data

    def _get_status_id_by_name(self, status_name: str) -> int:
        normalized_name = status_name.upper()

        status = self.session.query(Status).filter(Status.name == normalized_name).first()
        if not status:
            Logger.fatal(f'Указанный статус "{normalized_name}" не существует в таблице со статусами') 
            
        return status.id

    def _get_or_create_project_id_by_name(self, project_name: str) -> int:
        normalized_name = project_name.upper()
        
        project = self.session.query(Project).filter(Project.name == normalized_name).first()
        if not project:
            project = Project(name=normalized_name)
            self.session.add(project)
            self.session.commit()
            
        return project.id

    def _get_or_create_author_id_by_name(self, author_name: str) -> int:
        author = self.session.query(Author).filter(Author.name == author_name).first()
        if not author:
            login = self.test_data.author_login if self.test_data.author_login else author_name.lower()
            email = self.test_data.author_email if self.test_data.author_email else f'{author_name.lower()}@tquality.ru'

            existing_login = self.session.query(Author).filter(Author.login == login).first()
            if existing_login:
                Logger.info(
                    f"Логин '{login}' уже занят автором '{existing_login.name}' (ID {existing_login.id}). "
                    f"Используем существующего автора во избежание ошибки уникальности."
                )
                return existing_login.id

            author = Author(
                name=author_name, 
                login=login, 
                email=email
            )
            self.session.add(author)
            self.session.commit()
        return author.id

    def _get_or_create_session_id_by_key(self, session_key: str) -> int:
        session = self.session.query(SessionModel).filter(SessionModel.session_key == session_key).first()
        if not session:
            max_build = self.session.query(func.max(SessionModel.build_number)).scalar()
            next_build_number = (max_build or 0) + 1 

            session = SessionModel(
                session_key=session_key, 
                created_time=datetime.now(), 
                build_number=next_build_number
            )
            self.session.add(session)
            self.session.commit()
        return session.id

    def _save_test(self, test_id: int | None = None, update_in_place: bool = False, **fields) -> Test:
        if test_id is not None:
            db_test = self.get_test_by_id(test_id)
            if not db_test:
                Logger.fatal(f'Исходный тест с ID {test_id} не найден')
            
            target_test = db_test if update_in_place else None
            
            base_name = db_test.name
            base_method = db_test.method_name
            base_status_id = db_test.status_id
            base_project_id = db_test.project_id
            base_session_id = db_test.session_id
            base_author_id = db_test.author_id
            base_start_time = db_test.start_time
            base_end_time = db_test.end_time
            base_browser = db_test.browser
            base_env = db_test.env
        else:
            target_test = None
            base_name = None
            base_method = None
            base_status_id = None
            base_project_id = None
            base_session_id = None
            base_author_id = None
            base_start_time = None
            base_end_time = None
            base_browser = 'chrome'
            base_env = 'local'

        status_id = fields.get('status_id')
        if not status_id and 'status_name' in fields:
            status_id = self._get_status_id_by_name(fields['status_name'])
        status_id = status_id or base_status_id

        project_id = fields.get('project_id')
        if not project_id and 'project_name' in fields:
            project_id = self._get_or_create_project_id_by_name(fields['project_name'])
        project_id = project_id or base_project_id

        author_id = fields.get('author_id')
        if not author_id and 'author_name' in fields:
            author_id = self._get_or_create_author_id_by_name(fields['author_name'])
        author_id = author_id or base_author_id

        session_id = fields.get('session_id')
        if not session_id and 'session_key' in fields:
            session_id = self._get_or_create_session_id_by_key(fields['session_key'])
        session_id = session_id or base_session_id

        if update_in_place and target_test:
            target_test.name = fields.get('name', base_name)
            target_test.method_name = fields.get('method_name', base_method)
            target_test.status_id = status_id
            target_test.project_id = project_id
            target_test.session_id = session_id
            target_test.author_id = author_id
            target_test.start_time = fields.get('start_time', base_start_time)
            target_test.end_time = fields.get('end_time', base_end_time)
            target_test.browser = fields.get('browser', base_browser)
            target_test.env = fields.get('env', base_env)
            
            self.session.commit()
            return target_test
        else:
            new_test = Test(
                name=fields.get('name', base_name),
                method_name=fields.get('method_name', base_method),
                status_id=status_id,
                project_id=project_id,
                session_id=session_id,
                author_id=author_id,
                start_time=fields.get('start_time', base_start_time),
                end_time=fields.get('end_time', base_end_time),
                browser=fields.get('browser', base_browser),
                env=fields.get('env', base_env)
            )
            self.session.add(new_test)
            self.session.commit()
            return new_test

    def create_test(self, name: str, status_name: str, method_name: str, 
                    project_name: str, start_time: datetime, end_time: datetime,
                    author_name: str, session_key: str, browser: str = 'chrome') -> Test:
        return self._save_test(
            test_id=None,
            update_in_place=False,
            name=name,
            status_name=status_name,
            method_name=method_name,
            project_name=project_name,
            start_time=start_time,
            end_time=end_time,
            author_name=author_name,
            session_key=session_key,
            browser=browser
        )

    def copy_test(self, test_id: int, **overrides) -> Test:
        return self._save_test(test_id=test_id, update_in_place=False, **overrides)

    def update_test(self, test_id: int, **updates) -> Test:
        return self._save_test(test_id=test_id, update_in_place=True, **updates)
    
    def get_all_tests(self):
        return self.session.query(Test).all()

    def get_test_by_id(self, test_id: int) -> Test | None:
        return self.session.query(Test).filter(Test.id == test_id).first()

    def delete_test(self, test_id: int) -> bool:
        test = self.get_test_by_id(test_id)
        if test:
            self.session.delete(test)
            self.session.commit()
            return True
        else:
            return False
        
    def get_unique_statuses(self) -> list[str]:
        results = self.session.query(Status.name).distinct().all()
        return [name for (name,) in results if name]

    def get_unique_browsers(self) -> list[str]:
        results = self.session.query(Test.browser).distinct().all()
        return [browser for (browser,) in results if browser is not None]