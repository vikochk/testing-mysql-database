import random
import socket
from typing import ClassVar
from datetime import datetime, timedelta

from pydantic import BaseModel

from src.utils.logger import Logger
from src.utils.random_generation import RandomGeneration


class SimulatedTestRun(BaseModel):
    status_name: str
    start_time: datetime
    end_time: datetime
    browser: str
    env: str


class MockTestRunner:
    DURATION_RANGE: ClassVar[tuple[int, int]] = (1, 15)

    @classmethod
    def simulate_test_run(cls, db) -> SimulatedTestRun:
        end_time = datetime.now().replace(microsecond=0)
        start_time = end_time - timedelta(seconds=random.randint(*cls.DURATION_RANGE))
        
        statuses = db.get_unique_statuses()
        chosen_status = RandomGeneration.choose_single_from_list(statuses)
        
        browsers = db.get_unique_browsers()
        chosen_browser = RandomGeneration.choose_single_from_list(browsers)
        
        computer_name = socket.gethostname()

        result = {
            'status_name': chosen_status,
            'start_time': start_time,
            'end_time': end_time,
            'browser': chosen_browser,
            'env': computer_name
        }
        Logger.info(f'Сгенерированы данные для теста: {", ".join([f"{key}: {value}" for key, value in result.items()])}')

        return SimulatedTestRun(
            status_name=chosen_status,
            start_time=start_time,
            end_time=end_time,
            browser=chosen_browser,
            env=computer_name
        )