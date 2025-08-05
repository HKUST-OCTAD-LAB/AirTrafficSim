"""AirTrafficSim v0.2"""

try:
    # register our polars extension
    import airtrafficsim._polars_array_api  # noqa
except ImportError:
    pass

from .utils import hook as hook
