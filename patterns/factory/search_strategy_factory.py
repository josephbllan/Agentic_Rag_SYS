from typing import Dict, Type
import logging
from domain.base_classes import BaseSearchStrategy


class SearchStrategyFactory:
    _strategy_classes: Dict[str, Type[BaseSearchStrategy]] = {}
    _logger = logging.getLogger("SearchStrategyFactory")

    @classmethod
    def register_strategy(cls, strategy_type: str, strategy_class: Type[BaseSearchStrategy]) -> None:
        cls._strategy_classes[strategy_type] = strategy_class

    @classmethod
    def create_strategy(cls, strategy_type: str, **kwargs) -> BaseSearchStrategy:
        if strategy_type not in cls._strategy_classes:
            raise ValueError(f"Unknown strategy: {strategy_type}. Available: {list(cls._strategy_classes.keys())}")
        return cls._strategy_classes[strategy_type](**kwargs)

    @classmethod
    def get_supported_strategies(cls) -> list[str]:
        return list(cls._strategy_classes.keys())
