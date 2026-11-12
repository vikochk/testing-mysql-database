import pytest

from src.utils.logger import Logger
from src.utils.work_with_db import WorkWithDB
from src.utils.mock_test_runner import MockTestRunner


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, 'rep_' + rep.when, rep)

@pytest.fixture(autouse=True)
def record_test_to_db(request, db_session, test_data, session_key):
    try:
        yield
        
    finally:
        mock_data = getattr(request.node, 'mock_data', None)
        
        if mock_data:
            db = WorkWithDB(db_session, test_data)
            
            Logger.info('Динамическое получение метаданных теста')
            method_name = f'{request.module.__name__}#{request.node.name}'
            
            test_title = getattr(request.node, 'test_title', None)
            if not test_title:
                test_title = request.node.obj.__doc__ or request.node.name
            
            Logger.info('Запись результатов симуляции в БД')
            db.create_test(
                name=test_title,
                method_name=method_name,
                status_name=mock_data.status_name,
                project_name=test_data.project_name,
                session_key=session_key,
                author_name=test_data.author_name,
                start_time=mock_data.start_time,
                end_time=mock_data.end_time,
                browser=mock_data.browser
            )


class TestAddTestToDB:
    def test_verify_summation(self, db_session, request, test_data):
        request.node.test_title = test_data.new_tests_names.summation

        db = WorkWithDB(db_session, test_data)
        
        Logger.info(f'Запуск мок-симуляции для теста {test_data.new_tests_names.summation}')
        mock_data = MockTestRunner.simulate_test_run(db)
        
        Logger.info('Передача результатов в контекст pytest для постусловия')
        request.node.mock_data = mock_data
        
        Logger.info('Имитация поведения теста в pytest на основе статуса из мока')
        if mock_data.status_name == 'FAILED':
            assert False, 'Имитация падения теста на основе мок-данных'
        elif mock_data.status_name == 'SKIPPED':
            pytest.skip('Имитация пропуска теста на основе мок-данных')
        else:
            assert True

    def test_verify_string_multiplied(self, db_session, request, test_data):
        request.node.test_title = test_data.new_tests_names.multiplication
        
        db = WorkWithDB(db_session, test_data)
        
        Logger.info(f'Запуск мок-симуляции для теста {test_data.new_tests_names.multiplication}')
        mock_data = MockTestRunner.simulate_test_run(db)

        Logger.info('Передача результатов в контекст pytest для постусловия')
        request.node.mock_data = mock_data
        
        Logger.info('Имитация поведения теста в pytest на основе статуса из мока')
        if mock_data.status_name == 'FAILED':
            assert False, 'Имитация падения теста на основе мок-данных'
        elif mock_data.status_name == 'SKIPPED':
            pytest.skip('Имитация пропуска теста на основе мок-данных')
        else:
            assert True