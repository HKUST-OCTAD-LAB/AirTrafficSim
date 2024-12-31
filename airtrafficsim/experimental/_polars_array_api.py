import math

import polars as pl

abs = pl.Expr.abs
acos = pl.Expr.arccos
acosh = pl.Expr.arccosh
add = pl.Expr.add
all = pl.Expr.all
any = pl.Expr.any
arange = pl.arange  # !
argmax = pl.Expr.arg_max
argmin = pl.Expr.arg_min
argsort = pl.Expr.arg_sort
asarray = pl.Series  # ! not exactly the same
asin = pl.Expr.arcsin
asinh = pl.Expr.arcsinh
astype = pl.Expr.cast
atan = pl.Expr.arctan
atan2 = pl.arctan2  # !
atanh = pl.Expr.arctanh
bitwise_and = pl.Expr.bitwise_and
bitwise_invert = pl.Expr.__invert__
bitwise_or = pl.Expr.bitwise_or
bitwise_xor = pl.Expr.bitwise_xor
bool = pl.Boolean
ceil = pl.Expr.ceil
clip = pl.Expr.clip
concat = pl.concat
cumulative_sum = pl.Expr.cum_sum
cos = pl.Expr.cos
cosh = pl.Expr.cosh
diff = pl.Expr.diff
divide = pl.Expr.truediv
e = math.e
exp = pl.Expr.exp
equal = pl.Expr.eq
flip = pl.Expr.reverse
float32 = pl.Float32
float64 = pl.Float64
floor = pl.Expr.floor
floor_divide = pl.Expr.floordiv
greater = pl.Expr.gt
greater_equal = pl.Expr.ge


def hypot(x1: pl.Expr, x2: pl.Expr) -> pl.Expr:
    return pl.Expr.sqrt(x1**2 + x2**2)


inf = math.inf
int16 = pl.Int16
int32 = pl.Int32
int64 = pl.Int64
int8 = pl.Int8
isfinite = pl.Expr.is_finite
isinf = pl.Expr.is_infinite
isnan = pl.Expr.is_nan
less = pl.Expr.lt
less_equal = pl.Expr.le


def log2(x: pl.Expr) -> pl.Expr:
    return pl.Expr.log(x, base=2)


def logaddexp(x1: pl.Expr, x2: pl.Expr) -> pl.Expr:
    return pl.Expr.log(pl.Expr.exp(x1) + pl.Expr.exp(x2))


log = pl.Expr.log
log10 = pl.Expr.log10
log1p = pl.Expr.log1p
logical_and = pl.Expr.and_
logical_not = pl.Expr.not_
logical_or = pl.Expr.or_
logical_xor = pl.Expr.xor
max = pl.Expr.max
maximum = pl.Expr.max
mean = pl.Expr.mean
min = pl.Expr.min
minimum = pl.Expr.min
multiply = pl.Expr.mul
nan = math.nan
negative = pl.Expr.neg
nonzero = pl.Expr.arg_true
not_equal = pl.Expr.ne
ones = pl.ones
pi = math.pi
positive = pl.Expr.__pos__
pow = pl.Expr.pow
prod = pl.Expr.product


def reciprocal(x: pl.Expr) -> pl.Expr:
    return 1 / x


remainder = pl.Expr.mod
repeat = pl.Expr.repeat_by
reshape = pl.Expr.reshape
round = pl.Expr.round
searchsorted = pl.Expr.search_sorted
signbit = pl.Expr.sign
sin = pl.Expr.sin
sign = pl.Expr.sign
sinh = pl.Expr.sinh
sort = pl.Expr.sort
sqrt = pl.Expr.sqrt


def square(x: pl.Expr) -> pl.Expr:
    return x * x


stack = pl.concat
std = pl.Expr.std
subtract = pl.Expr.sub
sum = pl.Expr.sum
tan = pl.Expr.tan
tanh = pl.Expr.tanh
take = pl.Expr.gather  # ! get?
take_along_axis = pl.Expr.gather_every
uint16 = pl.UInt16
uint32 = pl.UInt32
uint64 = pl.UInt64
uint8 = pl.UInt8
unique_counts = pl.Expr.unique_counts
unique_inverse = pl.Expr.arg_unique
unique_values = pl.Expr.unique
var = pl.Expr.var
vecdot = pl.Expr.dot


def where(condition: pl.Expr, x: pl.Expr, y: pl.Expr) -> pl.Expr:
    return pl.when(condition).then(x).otherwise(y)


zeros = pl.zeros
