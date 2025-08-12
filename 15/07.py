import rich.console
from aocd.models import Puzzle
from functools import partial, cache
import pyparsing as pp

YEAR = 2015
DAY = 7

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")


wires = {}


@cache
def eval_wire(id):
    return wires[id]()


def eval_and(left, right):
    return left() & right()


def eval_or(left, right):
    return left() | right()


def eval_not(right):
    return 0xFFFF - right()


def eval_rshift(left, right):
    return left() >> right()


def eval_lshift(left, right):
    return left() << right()


signal = pp.common.integer


@signal.set_parse_action
def signal_parse_action(tokens):
    value = int(tokens[0])
    return partial(int, value)


wire_id = pp.Word(pp.srange("[a-z]"))("wire_id")
wire = wire_id.copy()


@wire.set_parse_action
def wire_parse_action(tokens):
    return partial(eval_wire, tokens.wire_id)


gate_input = signal | wire
and_ = (gate_input + pp.Suppress(pp.Keyword("AND")) + gate_input).set_name("AND")
or_ = (gate_input + pp.Suppress(pp.Keyword("OR")) + gate_input).set_name("OR")
not_ = (pp.Suppress(pp.Keyword("NOT")) + gate_input).set_name("NOT")
rshift = (gate_input + pp.Suppress(pp.Keyword("RSHIFT")) + gate_input).set_name(
    "RSHIFT"
)
lshift = (gate_input + pp.Suppress(pp.Keyword("LSHIFT")) + gate_input).set_name(
    "LSHIFT"
)


@and_.set_parse_action
def and_parse_action(tokens):
    left, right = tokens
    return partial(eval_and, left, right)


@rshift.set_parse_action
def rshift_parse_action(tokens):
    left, right = tokens
    return partial(eval_rshift, left, right)


@lshift.set_parse_action
def lshift_parse_action(tokens):
    left, right = tokens
    return partial(eval_lshift, left, right)


@or_.set_parse_action
def or_parse_action(tokens):
    left, right = tokens
    return partial(eval_or, left, right)


@not_.set_parse_action
def not_parse_action(tokens):
    right = tokens[0]
    return partial(eval_not, right)


src = (and_ | or_ | not_ | rshift | lshift | gate_input)("src")
conn = src + pp.Suppress(pp.Literal("->")) + wire_id("output")


@conn.set_parse_action
def conn_parse_action(tokens):
    src_func, output_wire_id = tokens
    wires[output_wire_id] = src_func


conns = conn[1, ...]
print(conns)

conns.parse_string(puzzle.input_data, parse_all=True)
result = wires["a"]()
puzzle.answer_a = result
print(f"{puzzle.answer_a=}")

c.rule()
new_line = f" {puzzle.answer_a} -> b "
new_input = "\n".join([puzzle.input_data, new_line])
print(new_input)

wires = {}
eval_wire.cache_clear()
conns.parse_string(new_input, parse_all=True)

print(wires)
result = wires["a"]()
print(f"{result=}")
puzzle.answer_b = result
c.rule()
