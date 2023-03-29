from typing import Tuple, Any, Set


class InvalidRootContainerError(Exception):
    pass


class MissingMappingKeyError(Exception):
    pass


class UnknownMappingKeyError(Exception):
    pass


class MappingsSyntaxValidator:
    """
    Validates the syntax of the mapping config data.
    """

    SUPPORTED_MAPPING_KEYS: Set[str] = {"table_key", "template_key"}

    @staticmethod
    def check(data: Any):
        if not isinstance(data, list):  # the root container has to be list
            raise InvalidRootContainerError(f"Expected the root container to be a list got {type(data)}")

        supported_keys = MappingsSyntaxValidator.SUPPORTED_MAPPING_KEYS
        for mapping in data:
            mapping = set(mapping)

            if len(mapping & supported_keys) != len(supported_keys):
                raise MissingMappingKeyError(f"Missing following keys: {supported_keys - mapping}")

            if len(mapping) > len(supported_keys):
                raise UnknownMappingKeyError(f"Unknown mapping keys: {mapping - supported_keys} "
                                        f"only {supported_keys} are supported.")
