"""
A system for representing units of measurement using an AST, with a code
generator for `siunitx`.

Current limitations:

- missing division: `m/s` is not allowed - use `m * s**-1` instead.
    - future versions may include a `Ratio` class for use in unit conversions
- no unit canonicalisation: `m * s * s` will not be simplified,
`m * (s**-1)**2` is not supported.

Contains a selection of commonly used SI and US Customary Units

[1] The International System of Units (SI): Text in English (updated in 2024),
9th edition 2019, V3.01 August 2024. Sèvres Cedex BIPM 2024, 2024. Available: https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf

[2] “NIST Handbook 44 - 2024 - Appendix C. General Tables of Units of
Measurement,” NIST, Available: https://www.nist.gov/document/nist-handbook-44-2024-appendix-c-pdf
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import TypeAlias

Exponent: TypeAlias = int | Fraction


class UnitBase:
    """Base class for all unit expressions."""

    def to_siunitx(self) -> str:
        """Convert the expression into a LaTeX `siunitx` string."""

        # recursively traverse from the root unit expression.

        def _to_siunitx(expr: UnitBase) -> str:
            # operator precendence as follows:
            if isinstance(expr, Mul):
                return f"{_to_siunitx(expr.lhs)}{_to_siunitx(expr.rhs)}"
            if isinstance(expr, Pow):
                if expr.exponent == 1:
                    return _to_siunitx(expr.base)
                exponent = _format_exponent_latex(expr.exponent)
                return rf"{_to_siunitx(expr.base)}\tothe{{{exponent}}}"
            if isinstance(expr, Prefix):
                return expr.siunitx
            if isinstance(expr, Named):
                return expr.siunitx
            if isinstance(expr, Unit):
                return expr.siunitx
            raise NotImplementedError(expr)

        return _to_siunitx(self)


def _format_exponent_latex(exponent: Exponent) -> str:
    if isinstance(exponent, int):
        return str(exponent)
    elif isinstance(exponent, Fraction):
        if exponent.denominator == 1:
            return str(exponent.numerator)
        # now a fraction
        prefix = "-" if exponent < 1 else ""
        return rf"{prefix}\frac{{{abs(exponent.numerator)}}}{{{exponent.denominator}}}"  # noqa: E501
    raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Unit(UnitBase):
    """A unit of measurement (e.g. `meter`, `slug`), acting as a leaf node."""

    symbol: str
    siunitx: str

    def __mul__(
        self, rhs: "Unit" | "Named" | "Mul" | "Pow" | "Prefix"
    ) -> "Mul":
        if isinstance(rhs, (Unit, Named, Mul, Pow, Prefix)):
            return Mul(lhs=self, rhs=rhs)
        return NotImplemented

    def __pow__(self, rhs: Exponent) -> "Pow":
        if isinstance(rhs, (int, Fraction)):
            return Pow(base=self, exponent=rhs)
        raise TypeError(
            f"Cannot raise a `Named` to the power of {rhs}\n"
            "help: must be an integer or fraction."
        )


@dataclass(frozen=True, slots=True)
class Named(UnitBase):
    """
    Provides aliases for a group of expressions (e.g. `Newton` for `kg·m·s⁻²`)
    """

    inner: UnitBase
    symbol: str
    siunitx: str

    def __post_init__(self) -> None:
        if isinstance(self.inner, Prefix):
            raise ValueError("cannot rename a prefix.")  # otherwise it allows ^

    def __mul__(
        self, rhs: "Unit" | "Named" | "Mul" | "Pow" | "Prefix"
    ) -> "Mul":
        if isinstance(rhs, (Unit, Named, Mul, Prefix)):
            return Mul(lhs=self, rhs=rhs)
        return NotImplemented

    def __pow__(self, rhs: Exponent) -> "Pow":
        if isinstance(rhs, (int, Fraction)):
            return Pow(base=self, exponent=rhs)
        raise TypeError(
            f"Cannot raise a `Named` to the power of {rhs}\n"
            "help: must be an integer or fraction."
        )


@dataclass(frozen=True, slots=True)
class Prefix(UnitBase):
    """Modifiers to units (e.g. `kilo`, `milli`)"""

    symbol: str
    siunitx: str
    # the following are used for metadata storage, and is not used for codegen.
    base: int = field(kw_only=True)
    power: int = field(kw_only=True)

    def __mul__(self, other: "Unit" | "Named") -> "Mul":
        if isinstance(other, (Unit, Named)):
            return Mul(lhs=self, rhs=other)
        elif isinstance(other, Prefix):
            # kilo * kilo
            raise TypeError("Cannot multiply two prefixes together.")
        elif isinstance(other, Mul):
            # kilo * (meter * s)
            raise TypeError("Cannot multiply a prefix with a Mul expression.")
        elif isinstance(other, Pow):
            # kilo * (meter ^ 2)
            raise TypeError("Cannot multiply a prefix with a Pow expression.")
        return NotImplemented

    # __pow__: cannot raise a prefix to the power of another prefix.


@dataclass(frozen=True, slots=True)
class Pow(UnitBase):
    """Represents exponentiation of a unit"""

    base: UnitBase
    exponent: Exponent

    def __mul__(self, other: "Unit" | "Named" | "Mul" | "Pow") -> "Mul":
        if isinstance(other, (Unit, Named, Mul, Pow)):
            return Mul(lhs=self, rhs=other)
        return NotImplemented

    # __pow__: cannot raise a (meter ^ 2) ^ 2, not implemented.


@dataclass(frozen=True, slots=True)
class Mul(UnitBase):
    """Represents non-commutative multiplication of units."""

    lhs: UnitBase
    rhs: UnitBase

    def __mul__(self, other: "Unit" | "Named" | "Mul" | "Pow") -> "Mul":
        if isinstance(other, (Unit, Named, Mul, Pow)):
            return Mul(lhs=self, rhs=other)
        return NotImplemented

    # __pow__: cannot raise a group of units to the power, it must be `Named`.


#
# 2.3.1 SI base unit (page 130)
#

SECOND = Unit("s", siunitx=r"\second")
METER = Unit("m", siunitx=r"\meter")
KILOGRAM = Unit("kg", siunitx=r"\kilogram")
AMPERE = Unit("A", siunitx=r"\ampere")
KELVIN = Unit("K", siunitx=r"\kelvin")
MOLE = Unit("mol", siunitx=r"\mol")
CANDELA = Unit("cd", siunitx=r"\candela")

GRAM = Unit("g", siunitx=r"\gram")  # technically not base, but for convenience

#
# 2.3.4 Derived units (page 137)
#

RAD = Unit("rad", r"\radian")  # plane angle
STERADIAN = Unit("sr", r"\steradian")  # solid angle
HERTZ = Named((SECOND**-1), "Hz", r"\hertz")  # frequency
NEWTON = Named((KILOGRAM * METER * SECOND**-2), "N", r"\newton")  # force
PASCAL = Named(
    (KILOGRAM * METER**-1 * SECOND**-2), "Pa", r"\pascal"
)  # pressure, stress
JOULE = Named(
    (KILOGRAM * METER**2 * SECOND**-2), "J", r"\joule"
)  # energy, work, heat
WATT = Named(
    (KILOGRAM * METER**2 * SECOND**-3), "W", r"\watt"
)  # power, radiant flux
COULOMB = Named((AMPERE * SECOND), "C", r"\coulomb")  # electric charge
VOLT = Named(
    (KILOGRAM * METER**2 * SECOND**-3 * AMPERE**-1), "V", r"\volt"
)  # electric potential, emf
FARAD = Named(
    (KILOGRAM**-1 * METER**-2 * SECOND**4 * AMPERE**2), "F", r"\farad"
)  # capacitance
OHM = Named(
    (KILOGRAM * METER**2 * SECOND**-3 * AMPERE**-2), "Ω", r"\ohm"
)  # electric resistance
SIEMENS = Named(
    (KILOGRAM**-1 * METER**-2 * SECOND**3 * AMPERE**2), "S", r"\siemens"
)  # electric conductance
WEBER = Named(
    (KILOGRAM * METER**2 * SECOND**-2 * AMPERE**-1), "Wb", r"\weber"
)  # magnetic flux
TESLA = Named(
    (KILOGRAM * SECOND**-2 * AMPERE**-1), "T", r"\tesla"
)  # magnetic flux density
HENRY = Named(
    (KILOGRAM * METER**2 * SECOND**-2 * AMPERE**-2), "H", r"\henry"
)  # inductance
CELSIUS = Unit("°C", r"\degreeCelsius")  # temperature Celsius
LUMEN = Named((CANDELA * STERADIAN), "lm", r"\lumen")  # luminous flux
LUX = Named((CANDELA * METER**-2), "lx", r"\lux")  # illuminance
BECQUEREL = Named(
    (SECOND**-1), "Bq", r"\text{Bq}"
)  # activity referred to a radionuclide
GRAY = Named(
    (METER**2 * SECOND**-2), "Gy", r"\gray"
)  # absorbed dose, specific energy imparted, kerma
SIEVERT = Named((METER**2 * SECOND**-2), "Sv", r"\sievert")  # dose equivalent
KATAL = Named((MOLE * SECOND**-1), "kat", r"\katal")  # catalytic activity

#
# 3. Decimal multiples and sub-multiples of SI units (page 143)
#

QUETTA = Prefix("Q", r"\quetta", base=10, power=30)
RONNA = Prefix("R", r"\ronna", base=10, power=27)
YOTTA = Prefix("Y", r"\yotta", base=10, power=24)
ZETTA = Prefix("Z", r"\zetta", base=10, power=21)
EXA = Prefix("E", r"\exa", base=10, power=18)
PETA = Prefix("P", r"\peta", base=10, power=15)
TERA = Prefix("T", r"\tera", base=10, power=12)
GIGA = Prefix("G", r"\giga", base=10, power=9)
MEGA = Prefix("M", r"\mega", base=10, power=6)
KILO = Prefix("k", r"\kilo", base=10, power=3)
HECTO = Prefix("h", r"\hecto", base=10, power=2)
DECA = Prefix("da", r"\deca", base=10, power=1)
DECI = Prefix("d", r"\deci", base=10, power=-1)
CENTI = Prefix("c", r"\centi", base=10, power=-2)
MILLI = Prefix("m", r"\milli", base=10, power=-3)
MICRO = Prefix("μ", r"\micro", base=10, power=-6)
NANO = Prefix("n", r"\nano", base=10, power=-9)
PICO = Prefix("p", r"\pico", base=10, power=-12)
FEMTO = Prefix("f", r"\femto", base=10, power=-15)
ATTO = Prefix("a", r"\atto", base=10, power=-18)
ZEPTO = Prefix("z", r"\zepto", base=10, power=-21)
YOCTO = Prefix("y", r"\yocto", base=10, power=-24)
RONTO = Prefix("r", r"\ronto", base=10, power=-27)
QUECTO = Prefix("q", r"\quecto", base=10, power=-30)

KIBI = Prefix("Ki", r"\kibi", base=2, power=10)
MEBI = Prefix("Mi", r"\mebi", base=2, power=20)
GIBI = Prefix("Gi", r"\gibi", base=2, power=30)
TEBI = Prefix("Ti", r"\tebi", base=2, power=40)
PEBI = Prefix("Pi", r"\pebi", base=2, power=50)
EXBI = Prefix("Ei", r"\exbi", base=2, power=60)
ZEBI = Prefix("Zi", r"\zebi", base=2, power=70)
YOBI = Prefix("Yi", r"\yobi", base=2, power=80)

#
# 4. Non-SI units accepted for use with the SI (page 145)
#

MINUTE = Unit("min", r"\minute")  # time
HOUR = Unit("h", r"\hour")  # time
DAY = Unit("d", r"\day")  # time
DEGREE = Unit("°", r"\degree")  # plane angle
ARCMINUTE = Unit("'", r"\arcminute")  # plane angle
ARCSECOND = Unit('"', r"\arcsecond")  # plane angle
HECTARE = Unit("ha", r"\hectare")  # area
LITRE = Unit("L", r"\litre")  # volume
TONNE = Unit("t", r"\tonne")  # mass
DALTON = Unit("Da", r"\dalton")  # mass
ELECTRONVOLT = Unit("eV", r"\electronvolt")  # energy
NEPER = Unit("Np", r"\neper")  # ratio (logarithmic)
BEL = Unit("B", r"\bel")  # ratio (logarithmic)
DECIBEL = Unit("dB", r"\decibel")  # ratio (logarithmic)
ASTRONOMICAL_UNIT = Unit("au", r"\astronomicalunit")  # length
GAL = Named(
    ((CENTI * METER) * SECOND**-2), "Gal", r"\text{Gal}"
)  # acceleration


#
# US Customary Units
#

INCH = Unit("in", r"\text{in}")
FOOT = Unit("ft", r"\text{ft}")
YARD = Unit("yd", r"\text{yd}")
MILE = Unit("mi", r"\text{mi}")
FATHOM = Unit("fathom", r"\text{fathom}")
NMI = Unit("nmi", r"\text{nmi}")

ACRE = Unit("acre", r"\text{acre}")

GALLON = Unit("gal", r"\text{gal}")  # liquid, not apothecaries

OUNCE = Unit("oz", r"\text{oz}")  # avoirdupois
POUND = Unit("lb", r"\text{lb}")  # avoirdupois, not force
TON = Unit("ton", r"\text{tn}")  # avoirdupois, short

SLUG = Unit("slug", r"\text{slug}")

#
# common aerospace units
#

KT = Unit("kt", r"\text{kt}")
ATM = Unit("atm", r"\text{atm}")
HORSEPOWER = Unit("hp", r"\text{hp}")
POUND_FORCE = Unit("lbf", r"\text{lbf}")
FAHRENHEIT = Unit("°F", r"\degree\text{F}")
RANKINE = Unit("°R", r"\degree\text{R}")
INHG = Unit("inHg", r"\text{inHg}")

# useful aliases
MPS = METER * SECOND**-1
MPS2 = METER * SECOND**-2  # acceleration
FPS = FOOT * SECOND**-1
FPM = FOOT * MINUTE**-1
MPH = MILE * HOUR**-1
KPH = KILO * METER * HOUR**-1
KGM3 = KILOGRAM * METER**-3  # density

HPA = HECTO * PASCAL
PSI = POUND_FORCE * INCH**-2


JMOLK = JOULE * MOLE**-1 * KELVIN**-1  # gas constant
JKGK = JOULE * KILOGRAM**-1 * KELVIN**-1  # specific gas constant
KGNS = KILOGRAM * SECOND**-1 * NEWTON**-1  # tsfc
LBLBFH = POUND * POUND_FORCE**-1 * HOUR**-1  # tsfc
