from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, Union, cast
from soc.problem import Problem
from itertools import count
from functools import reduce
from dataclasses import dataclass, field
import re
from pprint import pprint


@dataclass
class Passport:
    lineno: int
    # Birth Year
    byr: Optional[str] = field(default=None)

    # Issue Year
    iyr: Optional[str] = field(default=None)

    # Expiration Year
    eyr: Optional[str] = field(default=None)

    # Height
    hgt: Optional[str] = field(default=None)

    # Hair Color
    hcl: Optional[str] = field(default=None)

    # Eye Color
    ecl: Optional[str] = field(default=None)

    # Passport ID
    pid: Optional[str] = field(default=None)

    # Country ID
    cid: Optional[str] = field(default=None)

    _errors: List[str] = field(default_factory=list)
    _validated: bool = field(default=False)

    def error(self, src: str, issue: str) -> bool:
        self._errors.append(f"{src}: {issue}")
        return False

    def validate_byr(self) -> bool:
        """
        byr (Birth Year) - four digits; at least 1920 and at most 2002.
        """
        if self.byr is None:
            return self.error("byr", "is None")
        elif 1920 <= int(self.byr) <= 2002:
            return True
        return self.error("byr", f"1920 <= {int(self.byr)} <= 2002")

    def validate_iyr(self) -> bool:
        """
        iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        """
        if self.iyr is None:
            return self.error("iyr", "is None")
        if 2010 <= int(self.iyr) <= 2020:
            return True
        return self.error("iyr", f"2010 <= {int(self.iyr)} <= 2020")

    def validate_eyr(self) -> bool:
        """
        eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        """
        if self.eyr is None:
            return self.error("eyr", "is None")
        if 2020 <= int(self.eyr) <= 2030:
            return True
        return self.error("eyr", f"2020 <= {int(self.eyr)} <= 2030")

    def validate_hgt(self) -> bool:
        """
        hgt (Height) - a number followed by either cm or in: If cm, the number must be at least 150 and at most 193. If in, the number must be at least 59 and at most 76.
        """
        if self.hgt is None:
            return self.error("hgt", "is None")

        height, unit = self.hgt[:-2], self.hgt[-2:]
        if not height.isdigit():
            return self.error("hgt", f"is not a number {self.hgt}")

        if unit == "in":
            lo, hi = 59, 76
        elif unit == "cm":
            lo, hi = 150, 193
        else:
            return self.error("hgt", f"bad unit {unit} from {self.hgt}")
        if lo <= int(height) <= hi:
            return True
        return self.error("hgt", f"is not in range lo <= {int(height)} <= hi")

    def validate_hcl(self) -> bool:
        """
        hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        """
        if self.hcl is None:
            return self.error("hcl", "is None")
        if bool(re.match(r"#[0-9a-f]{6}", self.hcl)):
            return True
        return self.error("hcl", f"{self.hcl} is not #[0-9a-f]{{6}}")

    def validate_ecl(self) -> bool:
        """
        ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        """
        if self.ecl is None:
            return self.error("ecl", "is None")
        if self.ecl in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
            return True
        return self.error("ecl", f"{self.ecl} not in (amb blu brn gry grn hzl oth)")

    def validate_pid(self) -> bool:
        """
        pid (Passport ID) - a nine-digit number, including leading zeroes.
        """
        if self.pid is None:
            return self.error("pid", "is None")
        if self.pid.isdigit() and len(self.pid) == 9:
            return True
        return self.error("pid", f"{self.pid} is not a 9 digit number")

    def validate_cid(self) -> bool:
        """
        cid (Country ID) - ignored, missing or not.
        """
        return True

    def validate_all(self) -> None:
        if not self._validated:
            self.validate_byr()
            self.validate_iyr()
            self.validate_eyr()
            self.validate_hgt()
            self.validate_hcl()
            self.validate_ecl()
            self.validate_pid()
            self.validate_cid()
            self._validated = True

    def __bool__(self) -> bool:
        self.validate_all()
        return not self._errors

    @property
    def errors(self):
        print(f"---- from {self.lineno} ----")
        pprint(self._errors)


class App(Problem):
    lineno = 1

    newline_delimiter: str = "\n\n"

    def transformer(self, line: str) -> Optional[Passport]:
        # calculate line no for debug
        lineno = self.lineno
        self.lineno += 2 + sum(_ == '\n' for _ in line)

        if not line.strip():
            return None

        line = line.replace("\n", " ")
        return Passport(
            lineno=lineno,
            **{a.split(":")[0]: a.split(":")[1] for a in line.split()},
        )

    def run(self):
        valid_count = 0
        total_count = 0
        for passport in self:
            if passport is None:
                continue
            total_count += 1
            passport = cast(Passport, passport)
            if not passport:
                passport.errors
            else:
                print(passport)
            valid_count += bool(passport)

        print(valid_count, 'of', total_count)
