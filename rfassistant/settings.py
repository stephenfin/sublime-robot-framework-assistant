#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sublime imports
import sublime

# Plugin imports
try:
    from rfassistant import six
except ImportError:
    from ..rfassistant import six

if six.PY2:
    from rfassistant import settings_filename, rfdocs_update_url, rfdocs_manifest_path, \
        rfdocs_dir_path, scanner_config_path, python_libs_dir_path, resources_dir_path
    from utils import Singleton
else:
    from ..rfassistant import settings_filename, rfdocs_update_url, rfdocs_manifest_path, \
        rfdocs_dir_path, scanner_config_path, python_libs_dir_path, resources_dir_path
    from .utils import Singleton


class SettingsManager(six.with_metaclass(Singleton, object)):
    def init(self):
        self._settings = sublime.load_settings(settings_filename)
        self._defaults = {
            'rfdocs_update_url': rfdocs_update_url,
            'show_version_in_autocomplete_box': True,
            'log_level': 'error',
            'python_interpreter': 'python'  # should be path to python interpreter with robot installed.
        }
        for prop, value in self._defaults.items():
            if not self._settings.has(prop):
                self._settings.set(prop, value)
        self.save()
        # kind of hidden settings, that are needed permanently
        self.rfdocs_dir = rfdocs_dir_path
        self.rfdocs_manifest = rfdocs_manifest_path
        self.scanner_config = scanner_config_path
        self.python_libs_dir = python_libs_dir_path
        self.resources_dir = resources_dir_path

    def load(self):
        self._settings = sublime.load_settings(settings_filename)

    def set(self, name, value):
        self._settings.set(name, value)

    def get(self, name):
        return self._settings.get(name) or self._defaults[name]

    def save(self):
        sublime.save_settings(settings_filename)

    def __getattr__(self, name):
        return self.get(name)

settings = SettingsManager()

if six.PY2:
    settings.init()
else:
    # fix for async behaviour in ST3
    def plugin_loaded():
        global settings
        settings.init()
