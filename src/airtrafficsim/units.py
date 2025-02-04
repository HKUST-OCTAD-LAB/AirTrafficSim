"""
SI and US Customary Units

[1] The International System of Units (SI): Text in English (updated in 2024),
9th edition 2019, V3.01 August 2024. Sèvres Cedex BIPM 2024, 2024. Available: https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf

[2] “NIST Handbook 44 - 2024 - Appendix C. General Tables of Units of
Measurement,” NIST, Available: https://www.nist.gov/document/nist-handbook-44-2024-appendix-c-pdf
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Protocol, TypeAlias, runtime_checkable


@runtime_checkable
class HasSiUnitX(Protocol):
    siunitx: str | None


class SiUnitXMixin:
    def to_siunitx(self, *, overrides: dict[Expr, str] = {}) -> str:
        return to_siunitx(self, overrides=overrides)  # type: ignore


@dataclass(frozen=True, slots=True)
class Mul(SiUnitXMixin):
    left: "Expr"
    right: "Expr"

    def __mul__(self, other: "Expr") -> "Mul":
        return Mul(self, other)

    def with_siunitx(self, siunitx: str) -> "NamedMul":
        return NamedMul(self.left, self.right, siunitx=siunitx)


@dataclass(frozen=True, slots=True)
class NamedMul(Mul):
    siunitx: str = field(kw_only=True)

    # allow renamed units to be raised to the power of something, e.g. ohm**-1
    def __pow__(self, other: int | Fraction) -> Pow:
        return Pow(self, other)


@dataclass(frozen=True, slots=True)
class Pow(SiUnitXMixin):
    base: "Unit" | NamedMul
    exp: int | Fraction
    siunitx: str | None = field(kw_only=True, default=None)

    def __mul__(self, other: "Expr") -> Mul:
        return Mul(self, other)

    def with_siunitx(self, siunitx: str) -> "Pow":
        return Pow(self.base, self.exp, siunitx=siunitx)


@dataclass(frozen=True, slots=True)
class Unit(SiUnitXMixin):
    symbol: str
    """Human readable string, ideally ASCII"""
    siunitx: str | None = field(kw_only=True, default=None)

    def __mul__(self, other: "Expr") -> Mul:
        return Mul(self, other)

    def __pow__(self, other: int | Fraction) -> Pow:
        return Pow(self, other)

    def with_siunitx(self, siunitx: str) -> "Unit":
        return Unit(self.symbol, siunitx=siunitx)


@dataclass(frozen=True, slots=True)
class Prefix(SiUnitXMixin):
    symbol: str
    base: int = field(kw_only=True)  # keeping for metadata.
    power: int = field(kw_only=True)  # keeping for metadata.
    siunitx: str | None = field(kw_only=True, default=None)

    def __mul__(self, other: Unit) -> Unit:
        return Unit(
            f"{self.symbol}{other.symbol}",
            siunitx=f"{self.siunitx}{other.siunitx}",
        )


Expr: TypeAlias = Mul | Pow | Unit


def to_siunitx(expr: Expr, *, overrides: dict[Expr, str] = {}) -> str:
    if isinstance(expr, HasSiUnitX) and expr.siunitx is not None:
        return expr.siunitx
    elif expr in overrides:
        return overrides[expr]
    elif isinstance(expr, Unit):  # unnamed bare unit
        return rf"\text{{{expr.symbol}}}"
    elif isinstance(expr, Pow):
        base_latex = to_siunitx(expr.base, overrides=overrides)
        exp = expr.exp
        if isinstance(exp, Fraction):
            if exp.denominator == 1:
                exp_str = str(exp.numerator)
            else:
                # TODO: improve negative
                exp_str = rf"\frac{{{exp.numerator}}}{{{exp.denominator}}}"
        else:  # int
            exp_str = str(exp)
        return rf"{base_latex}\tothe{{{exp_str}}}"
    elif isinstance(expr, Mul):
        left_latex = to_siunitx(expr.left, overrides=overrides)
        right_latex = to_siunitx(expr.right, overrides=overrides)
        return rf"{left_latex}{right_latex}"
    else:
        raise TypeError(f"Unsupported expression type: {type(expr)}")


#
# 2.3.1 SI base unit (page 130)
#

SECOND = Unit("s", siunitx=r"\second")
METER = Unit("m", siunitx=r"\meter")
KILOGRAM = Unit("kg").with_siunitx(r"\kilogram")
AMPERE = Unit("A", siunitx=r"\ampere")
KELVIN = Unit("K", siunitx=r"\kelvin")
MOLE = Unit("mol", siunitx=r"\mol")
CANDELA = Unit("cd", siunitx=r"\candela")

#
# 2.3.4 Derived units (page 137)
#

RADIAN = Unit("rad").with_siunitx(r"\radian")  # plane angle
STERADIAN = Unit("sr").with_siunitx(r"\steradian")  # solid angle
HERTZ = (SECOND**-1).with_siunitx(r"\hertz")  # frequency
NEWTON = (KILOGRAM * METER * SECOND**-2).with_siunitx(r"\newton")  # force
PASCAL = (KILOGRAM * METER**-1 * SECOND**-2).with_siunitx(
    r"\pascal"
)  # pressure, stress
JOULE = (KILOGRAM * METER**2 * SECOND**-2).with_siunitx(
    r"\joule"
)  # energy, work, heat
WATT = (KILOGRAM * METER**2 * SECOND**-3).with_siunitx(
    r"\watt"
)  # power, radiant flux
COULOMB = (AMPERE * SECOND).with_siunitx(r"\coulomb")  # electric charge
VOLT = (KILOGRAM * METER**2 * SECOND**-3 * AMPERE**-1).with_siunitx(
    r"\volt"
)  # electric potential, emf
FARAD = (KILOGRAM**-1 * METER**-2 * SECOND**4 * AMPERE**2).with_siunitx(
    r"\farad"
)  # capacitance
OHM = (KILOGRAM * METER**2 * SECOND**-3 * AMPERE**-2).with_siunitx(
    r"\ohm"
)  # electric resistance
SIEMENS = (KILOGRAM**-1 * METER**-2 * SECOND**3 * AMPERE**2).with_siunitx(
    r"\siemens"
)  # electric conductance
WEBER = (KILOGRAM * METER**2 * SECOND**-2 * AMPERE**-1).with_siunitx(
    r"\weber"
)  # magnetic flux
TESLA = (KILOGRAM * SECOND**-2 * AMPERE**-1).with_siunitx(
    r"\tesla"
)  # magnetic flux density
HENRY = (KILOGRAM * METER**2 * SECOND**-2 * AMPERE**-2).with_siunitx(
    r"\henry"
)  # inductance
DEGREE_CELSIUS = Unit("°C").with_siunitx(
    r"\degreeCelsius"
)  # temperature Celsius
LUMEN = (CANDELA * STERADIAN).with_siunitx(r"\lumen")  # luminous flux
LUX = (CANDELA * METER**-2).with_siunitx(r"\lux")  # illuminance
BECQUEREL = (SECOND**-1).with_siunitx(
    r"\text{Bq}"  # NOTE: siunitx does not have a dedicated one
)  # activity referred to a radionuclide
GRAY = (METER**2 * SECOND**-2).with_siunitx(
    r"\gray"
)  # absorbed dose, specific energy imparted, kerma
SIEVERT = (METER**2 * SECOND**-2).with_siunitx(r"\sievert")  # dose equivalent
KATAL = (MOLE * SECOND**-1).with_siunitx(r"\katal")  # catalytic activity

#
# 3. Decimal multiples and sub-multiples of SI units (page 143)
#

QUETTA = Prefix("Q", base=10, power=30, siunitx=r"\quetta")
RONNA = Prefix("R", base=10, power=27, siunitx=r"\ronna")
YOTTA = Prefix("Y", base=10, power=24, siunitx=r"\yotta")
ZETTA = Prefix("Z", base=10, power=21, siunitx=r"\zetta")
EXA = Prefix("E", base=10, power=18, siunitx=r"\exa")
PETA = Prefix("P", base=10, power=15, siunitx=r"\peta")
TERA = Prefix("T", base=10, power=12, siunitx=r"\tera")
GIGA = Prefix("G", base=10, power=9, siunitx=r"\giga")
MEGA = Prefix("M", base=10, power=6, siunitx=r"\mega")
KILO = Prefix("k", base=10, power=3, siunitx=r"\kilo")
HECTO = Prefix("h", base=10, power=2, siunitx=r"\hecto")
DECA = Prefix("da", base=10, power=1, siunitx=r"\deca")
DECI = Prefix("d", base=10, power=-1, siunitx=r"\deci")
CENTI = Prefix("c", base=10, power=-2, siunitx=r"\centi")
MILLI = Prefix("m", base=10, power=-3, siunitx=r"\milli")
MICRO = Prefix("μ", base=10, power=-6, siunitx=r"\micro")
NANO = Prefix("n", base=10, power=-9, siunitx=r"\nano")
PICO = Prefix("p", base=10, power=-12, siunitx=r"\pico")
FEMTO = Prefix("f", base=10, power=-15, siunitx=r"\femto")
ATTO = Prefix("a", base=10, power=-18, siunitx=r"\atto")
ZEPTO = Prefix("z", base=10, power=-21, siunitx=r"\zepto")
YOCTO = Prefix("y", base=10, power=-24, siunitx=r"\yocto")
RONTO = Prefix("r", base=10, power=-27, siunitx=r"\ronto")
QUECTO = Prefix("q", base=10, power=-30, siunitx=r"\quecto")

KIBI = Prefix("Ki", base=2, power=10, siunitx=r"\kibi")
MEBI = Prefix("Mi", base=2, power=20, siunitx=r"\mebi")
GIBI = Prefix("Gi", base=2, power=30, siunitx=r"\gibi")
TEBI = Prefix("Ti", base=2, power=40, siunitx=r"\tebi")
PEBI = Prefix("Pi", base=2, power=50, siunitx=r"\pebi")
EXBI = Prefix("Ei", base=2, power=60, siunitx=r"\exbi")
ZEBI = Prefix("Zi", base=2, power=70, siunitx=r"\zebi")
YOBI = Prefix("Yi", base=2, power=80, siunitx=r"\yobi")

#
# 4. Non-SI units accepted for use with the SI (page 145)
#

MINUTE = Unit("min").with_siunitx(r"\minute")  # time
HOUR = Unit("h").with_siunitx(r"\hour")  # time
DAY = Unit("d").with_siunitx(r"\day")  # time
DEGREE_ANGLE = Unit("°").with_siunitx(r"\degree")  # plane angle
ARCMINUTE = Unit("'").with_siunitx(r"\arcminute")  # plane angle
ARCSECOND = Unit('"').with_siunitx(r"\arcsecond")  # plane angle
HECTARE = Unit("ha").with_siunitx(r"\hectare")  # area
LITRE = Unit("L").with_siunitx(r"\litre")  # volume
TONNE = Unit("t").with_siunitx(r"\tonne")  # mass
DALTON = Unit("Da").with_siunitx(r"\dalton")  # mass
ELECTRONVOLT = Unit("eV").with_siunitx(r"\electronvolt")  # energy
NEPER = Unit("Np").with_siunitx(r"\neper")  # ratio (logarithmic)
BEL = Unit("B").with_siunitx(r"\bel")  # ratio (logarithmic)
DECIBEL = Unit("dB").with_siunitx(r"\decibel")  # ratio (logarithmic)
ASTRONOMICAL_UNIT = Unit("au").with_siunitx(r"\astronomicalunit")  # length
GAL = ((CENTI * METER) * SECOND**-2).with_siunitx(r"\text{Gal}")  # acceleration


#
# US Customary Units
#

INCH = Unit("in").with_siunitx(r"\text{in}")
FOOT = Unit("ft").with_siunitx(r"\text{ft}")
YARD = Unit("yd").with_siunitx(r"\text{yd}")
MILE = Unit("mi").with_siunitx(r"\text{mi}")
FATHOM = Unit("fathom").with_siunitx(r"\text{fathom}")
NMI = Unit("nmi").with_siunitx(r"\text{nmi}")

ACRE = Unit("acre").with_siunitx(r"\text{acre}")

GALLON = Unit("gal").with_siunitx(r"\text{gal}")  # liquid, not apothecaries

OUNCE_AVOIRDUPOIS = Unit("oz").with_siunitx(r"\text{oz}")
POUND_AVOIRDUPOIS = Unit("lb").with_siunitx(r"\text{lb}")  # not force
TON_AVOIRDUPOIS = Unit("ton").with_siunitx(r"\text{tn}")  # avoirdupois short

SLUG = Unit("slug").with_siunitx(r"\text{slug}")

KNOT = Unit("kt").with_siunitx(r"\text{kt}")
ATM = Unit("atm").with_siunitx(r"\text{atm}")
HORSEPOWER = Unit("hp").with_siunitx(r"\text{hp}")
POUND_FORCE = Unit("lbf").with_siunitx(r"\text{lbf}")
DEGREE_FAHRENHEIT = Unit("°F").with_siunitx(r"\degree\text{F}")
DEGREE_RANKINE = Unit("°R").with_siunitx(r"\degree\text{R}")
