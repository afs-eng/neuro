from apps.tests.registry import register_test_module

from .config import MCHATModule


register_test_module(MCHATModule.code, MCHATModule())
