from apps.tests.registry import register_test_module

from .config import CARS2HFModule


register_test_module(CARS2HFModule.code, CARS2HFModule())
