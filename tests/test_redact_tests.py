import pytest
from src.utils.logger import Logger
from src.utils.mock_test_runner import MockTestRunner
from src.utils.random_generation import RandomGeneration
from src.utils.work_with_db import WorkWithDB


@pytest.fixture
def prepare_cloned_tests(db_session, test_data):
    db = WorkWithDB(db_session, test_data)

    Logger.info('Запрос списка всех существующих тестов из базы данных')
    all_tests = db.get_all_tests()
    
    Logger.info('Фильтрация ID тестов: поиск идентификаторов, содержащих повторяющиеся цифры')
    ids_with_duplicates = [
        test.id for test in all_tests if len(str(test.id)) != len(set(str(test.id)))
    ]
    Logger.info(f'Найдено {len(ids_with_duplicates)} подходящих ID с дубликатами: {ids_with_duplicates}')

    Logger.info(f'Выбор случайных {test_data.amount_of_tests_with_duplicates} ID из найденных')
    chosen_ids = RandomGeneration.choose_multiple_from_list(
        ids_with_duplicates, test_data.amount_of_tests_with_duplicates
    )
    Logger.info(f'Выбранные случайные ID для копирования: {chosen_ids}')
    
    all_new_tests = []
    Logger.info('Копирование выбранных тестов с новым автором и проектом')
    for orig_id in chosen_ids:
        Logger.info(f"Копирование теста с ID {orig_id}. Новый проект: '{test_data.project_name}', автор: '{test_data.author_name}'")
        new_test = db.copy_test(
            test_id=orig_id,
            project_name=test_data.project_name,
            author_name=test_data.author_name
        )
        Logger.info('Проверка того, что тест сохранен и ID теста был сгенерирован базой данных')
        assert new_test.id is not None, 'Тест не был сохранен в базу данных'

        all_new_tests.append(new_test)
        Logger.info(f'Временный тест успешно создан с ID: {new_test.id}')
        
    try:
        yield all_new_tests
        
    finally:
        Logger.info('Удаление созданных в ходе теста копий')
        for test in all_new_tests:
            Logger.info(f'Удаляем из БД созданную копию с ID {test.id}')
            assert db.delete_test(test_id=test.id), f'Удаление невозможно: запись о тесте с ID {test.id} не была найдена'
            Logger.info(f'Запись теста с ID {test.id} успешно удалена')


class TestRedactTests:
    def test_redact_tests(self, prepare_cloned_tests, session_key, db_session, test_data):
        Logger.info('Симуляция запуска и обновление скопированных записей')
        db = WorkWithDB(db_session, test_data)
        
        Logger.info('Перебор подготовленных временных копий тестов')
        for test in prepare_cloned_tests:
            Logger.info(f'Запуск симуляции прогона для скопированного теста с ID {test.id}')
            simulated_results = MockTestRunner.simulate_test_run(db)

            Logger.info(f'Обновление полей теста с ID {test.id} в базе данных сгенерированными мок-данными')
            updated_record = db.update_test(
                test_id=test.id, 
                session_key=session_key, 
                **simulated_results.model_dump()
            )

            Logger.info('Проверка того, что записанные в базу данных параметры обновлены')
            assert updated_record.start_time == simulated_results.start_time, \
                'Данные о тесте не были обновлены: время запуска тестов не совпадает'
            assert updated_record.browser == simulated_results.browser, \
                'Данные о тесте не были обновлены: браузер запуска тестов не совпадает'
            Logger.info(f'Тест с ID {test.id} успешно обновлен и проверен')