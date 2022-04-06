from pydantic.fields import ModelField


def validate_id(id_: int, field: ModelField) -> int:
    assert id_ > 0, f"{field.name} is not a valid id."
    return id_


def validate_amount(amount: float, field: ModelField) -> float:
    assert amount > 0, f"{field.name} must be greater than zero."
    return amount
