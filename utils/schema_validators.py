from pydantic.fields import ModelField


def validate_id(id_: int, field: ModelField) -> int:
    """

    :param id_:
    :param field:
    :return:
    """
    if id_ < 0:
        raise ValueError(f"{field.name} is not a valid id.")
    return id_


def validate_amount(amount: float, field: ModelField) -> float:
    """

    :param amount:
    :param field:
    :return:
    """
    if amount < 0:
        raise ValueError(f"{field.name} must be greater than zero.")
    return amount
