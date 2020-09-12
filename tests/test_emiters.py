
import importlib
import pkgutil

import pytest

import datagenerator

emitters = [importlib.import_module('datagenerator.' + name) for _, name, _ in pkgutil.iter_modules(
    datagenerator.__path__) if name.endswith('_emitter')]


@pytest.mark.parametrize('tested_emitter', emitters)
class TestValidateEmitter:

    def test_generator_has_Emitter_class(self, tested_emitter):
        assert 'Emitter' in dir(tested_emitter)

    def test_generator_has_send_message(self, tested_emitter):
        assert 'send_message' in dir(tested_emitter.Emitter)
