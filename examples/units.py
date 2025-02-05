"""
Define arbitary units of measure.
"""

from airtrafficsim.units import Unit

usd = Unit("USD", siunitx=r"\text{USD}")
worker = Unit("worker", siunitx=r"\text{worker}")
airport = Unit("airport", siunitx=r"\text{airport}")

print((worker * airport**-1).to_siunitx())
print((usd * worker**-1).to_siunitx())

"""
\text{worker}\text{airport}\tothe{-1}
\text{USD}\text{worker}\tothe{-1}
"""
