TEST_REGISTRY = {}


def register_test_module(code: str, module):
    TEST_REGISTRY[code] = module


def get_test_module(code: str):
    return TEST_REGISTRY.get(code)