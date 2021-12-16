from __future__ import annotations

import typing
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from io import StringIO

YEAR = 2021
DAY = 16

import time
from aocd import get_data, submit
from rich.console import Console

start_time = time.perf_counter()
c = Console()


data = "D2FE28"  # 2021 in decimal.
data = "38006F45291200"  # length type ID 0 that contains two sub-packets
data = "EE00D40C823060"  # length type ID 1 that contains three sub-packets:
data = "8A004A801A8002F478"  # 16
data = "620080001611562C8802118E34"  # 12
data = "C0015000016115A2E0802F182340"  # 23
data = "A0016C880162017C3686B18A3D4780"  # 31

data = "C200B40A82"  # 3
data = "C200B40A82"  # finds the sum of 1 and 2, resulting in the value 3.
data = "04005AC33890"  # finds the product of 6 and 9, resulting in the value 54.
data = "880086C3E88112"  # finds the minimum of 7, 8, and 9, resulting in the value 7.
data = "CE00C43D881120"  # finds the maximum of 7, 8, and 9, resulting in the value 9.
data = "D8005AC2A8F0"  # produces 1, because 5 is less than 15.
data = "F600BC2D8F"  # produces 0, because 5 is not greater than 15.
data = "9C005AC2F8F0"  # produces 0, because 5 is not equal to 15.
data = "9C0141080250320F1802104A08"  # produces 1, because 1 + 3 = 2 * 2.

data = get_data(year=YEAR, day=DAY)

c.rule("START")


def hex_to_bin_char(char: str) -> str:
    assert len(char) == 1
    i = int(char, 16)
    return f"{i:>04b}"


def hex_to_bin(s: str) -> str:
    return "".join(hex_to_bin_char(c) for c in s)


class PacketType(Enum):
    literal = 0b100

    sum = 0
    product = 1
    min = 2
    max = 3
    gt = 5
    lt = 6
    eq = 7


@dataclass(frozen=True)
class ParseResult:
    packet: Packet
    remainder: str


@dataclass
class Packet:
    version: Optional[int] = None
    type: Optional[PacketType] = None

    literal_value: Optional[int] = None
    subpackets: List[Packet] = field(default_factory=list)

    def value(self):
        if self.type is PacketType.literal:
            return self.literal_value
        elif self.type is PacketType.sum:
            return sum(self.subpacket_values())
        elif self.type is PacketType.product:
            result = 1
            for value in self.subpacket_values():
                result *= value
            return result
        elif self.type is PacketType.min:
            return min(self.subpacket_values())
        elif self.type is PacketType.max:
            return max(self.subpacket_values())
        elif self.type is PacketType.gt:
            a, b = self.subpacket_values()
            return 1 if a > b else 0
        elif self.type is PacketType.lt:
            a, b = self.subpacket_values()
            return 1 if a < b else 0
        elif self.type is PacketType.eq:
            a, b = self.subpacket_values()
            return 1 if a == b else 0

    def subpacket_values(self) -> typing.Generator[int, None, None]:
        return (subpacket.value() for subpacket in self.subpackets)

    def sum_version_numbers(self) -> int:
        total = 0
        if self.subpackets:
            total += sum(sub.sum_version_numbers() for sub in self.subpackets)
        assert self.version is not None
        total += self.version
        return total

    @classmethod
    def _read_literal_value(cls, binary) -> int:
        chunks = []
        while True:
            chunk = binary.read(5)
            more = int(chunk[0], 2)
            chunks.append(chunk[1:])
            if not more:
                break
        return int("".join(chunks), 2)

    @classmethod
    def _read_type_0_packets(cls, binary: StringIO) -> List[Packet]:
        packets = []
        total_length = int(binary.read(15), 2)
        finished_at = binary.tell() + total_length
        while binary.tell() < finished_at:
            packets.append(cls.read(binary))
            # c.print(f"{packets = }")
        assert binary.tell() == finished_at
        return packets

    @classmethod
    def _read_type_1_packets(cls, binary: StringIO) -> List[Packet]:
        packets: List[Packet] = []
        n_packets = int(binary.read(11), 2)
        while len(packets) < n_packets:
            packets.append(cls.read(binary))
            # c.print(f"{packets = }")
        assert len(packets) == n_packets
        return packets

    @classmethod
    def read(cls, binary: StringIO) -> Packet:
        p = Packet()
        p.version = int(binary.read(3), 2)
        p.type = PacketType(int(binary.read(3), 2))
        if p.type is PacketType.literal:
            p.literal_value = cls._read_literal_value(binary)
        else:  # operator packet
            length_type_id = int(binary.read(1), 2)
            if length_type_id == 0:
                p.subpackets = cls._read_type_0_packets(binary)
            else:
                p.subpackets = cls._read_type_1_packets(binary)
        return p


binary = StringIO(hex_to_bin(data))
packet = Packet.read(binary)
c.print(packet)
c.print(f"{packet.sum_version_numbers() = }")
c.print(f"{packet.value() = }")

c.rule(f"FINISH {time.perf_counter() - start_time}")
