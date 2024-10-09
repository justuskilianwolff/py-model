from dataclasses import dataclass


@dataclass
class AccessLevel:
    pass


class Public(AccessLevel):
    pass


class Private(AccessLevel):
    pass


class Protected(AccessLevel):
    pass
