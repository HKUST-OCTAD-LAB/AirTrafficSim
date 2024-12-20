import pandas as pd


def test_demoenv() -> None:
    from airtrafficsim.data.environment.DemoEnv import DemoEnv

    env = DemoEnv()
    env.run()
    df = pd.read_csv(env.file_path)
    assert df.shape[0] > 1 and df.isnull().values.any() is False


def test_openapdemo() -> None:
    from airtrafficsim.data.environment.OpenApDemo import OpenApDemo

    env = OpenApDemo()
    env.run()
    df = pd.read_csv(env.file_path)
    assert df.shape[0] > 1 and df.isnull().values.any() is False


def test_fullflightdemo() -> None:
    from airtrafficsim.data.environment.FullFlightDemo import FullFlightDemo

    env = FullFlightDemo()
    env.run()
    df = pd.read_csv(env.file_path)
    assert df.shape[0] > 1 and df.isnull().values.any() is False


def test_weatherdemo() -> None:
    from airtrafficsim.data.environment.WeatherDemo import WeatherDemo

    env = WeatherDemo()
    env.run()
    df = pd.read_csv(env.file_path)
    assert df.shape[0] > 1 and df.isnull().values.any() is False


def test_converthistoricdemo() -> None:
    from airtrafficsim.data.environment.ConvertHistoricDemo import (
        ConvertHistoricDemo,
    )

    env = ConvertHistoricDemo()
    env.run()
    df = pd.read_csv(env.file_path)
    assert df.shape[0] > 1 and df.isnull().values.any() is False
