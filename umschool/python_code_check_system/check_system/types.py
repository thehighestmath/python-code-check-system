from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class DataInOut:
    input_data: list[str]
    output_data: str # TODO: it can be list[str]
