"""
AirTrafficSim v0.2
"""

import logging

logger = logging.getLogger(__name__)

try:
    # register our polars extension
    import airtrafficsim._polars_array_api  # noqa
except ImportError:
    pass
