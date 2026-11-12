import random
import string
from typing import TypeVar, List

from src.utils.logger import Logger

T = TypeVar('T')


class RandomGeneration:
    @staticmethod
    def generate_string(
        length: int = 10, 
        required_groups: list[str] | None = None,
        mandatory_symbols: str = '',
        base_chars: str = string.ascii_lowercase
    ):
        if not isinstance(length, int) or length <= 0:
            Logger.warn('Длина имени имеет некорректный формат, берем значение по умолчанию')
            length = 10

        required_groups = required_groups or []
        result = []

        for group in required_groups:
            if group:
                result.append(random.choice(group))
                base_chars += group

        if mandatory_symbols:
            result.extend(list(mandatory_symbols))
            base_chars += mandatory_symbols

        if len(result) < length:
            while len(result) < length:
                result.append(random.choice(base_chars))
        elif len(result) > length:
            result = result[:length]

        random.shuffle(result)
        return ''.join(result)

    @classmethod
    def choose_multiple_from_list(cls, lst: list[T], count: int) -> list[T]:
        unique_list = list(set(lst))

        if count > len(unique_list):
            Logger.fatal(
                f'Запрошено {count} уникальных элементов, но доступно только {len(unique_list)}', 
                ValueError
            )
        
        return random.sample(unique_list, count)

    @classmethod
    def choose_single_from_list(cls, lst: list[T]) -> T:
        return cls.choose_multiple_from_list(lst, 1)[0]