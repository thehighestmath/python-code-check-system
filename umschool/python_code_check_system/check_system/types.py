from dataclasses import dataclass, field


# used for stdin/stdout check
@dataclass(kw_only=True, frozen=True)
class DataInOut:
    input_data: list[str]
    output_data: list[str]


# used for class test
@dataclass(kw_only=True, frozen=True)
class DataArgs:
    input_args: list = field(default_factory=list)
    input_kwargs: dict = field(default_factory=dict)
    output_data: ...
