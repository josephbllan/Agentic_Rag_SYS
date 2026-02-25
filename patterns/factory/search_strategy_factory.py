from typing import Dict, Type
import logging
from domain.base_classes import BaseSearchStrategy


class SearchStrategyFactory:
    _strategy_classes: Dict[str, Type[BaseSearchStrategy]] = {}
    _logger = logging.getLogger("SearchStrategyFactory")

    @classmethod
    def register_strategy(cls, strategy_type: str, strategy_class: Type[BaseSearchStrategy]) -> None:
        """Registers a search strategy class under the given strategy type identifier."""
        cls._strategy_classes[strategy_type] = strategy_class

    @classmethod
    def create_strategy(cls, strategy_type: str, **kwargs) -> BaseSearchStrategy:
        """Creates and returns a search strategy instance of the specified type.
        Raises ValueError if the strategy type has not been registered.
        """
        if strategy_type not in cls._strategy_classes:
            raise ValueError(f"Unknown strategy: {strategy_type}. Available: {list(cls._strategy_classes.keys())}")
        return cls._strategy_classes[strategy_type](**kwargs)

    @classmethod
    def get_supported_strategies(cls) -> list[str]:
        """Returns a list of all registered strategy type identifiers."""
        return list(cls._strategy_classes.keys())
