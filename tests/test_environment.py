import pytest
import pandas as pd
from importlib import import_module

def test_demoenv():
    Env = getattr(import_module('airtrafficsim.data.environment.DemoEnv', '...'), "DemoEnv")
    env = Env()
    env.run()
    df = pd.read_csv(env.file_path)
    assert df.shape[0] > 1 and df.isnull().values.any() == False

def test_fullflightdemo():
    Env = getattr(import_module('airtrafficsim.data.environment.FullFlightDemo', '...'), "FullFlightDemo")
    env = Env()
    env.run()
    df = pd.read_csv(env.file_path)
    assert df.shape[0] > 1 and df.isnull().values.any() == False

def test_weatherdemo():
    Env = getattr(import_module('airtrafficsim.data.environment.WeatherDemo', '...'), "WeatherDemo")
    env = Env()
    env.run()
    df = pd.read_csv(env.file_path)
    assert df.shape[0] > 1 and df.isnull().values.any() == False

def test_converthistoricdemo():
    Env = getattr(import_module('airtrafficsim.data.environment.ConvertHistoricDemo', '...'), "ConvertHistoricDemo")
    env = Env()
    env.run()
    df = pd.read_csv(env.file_path)
    assert df.shape[0] > 1 and df.isnull().values.any() == False