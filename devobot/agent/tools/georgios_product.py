from langchain_core.tools import tool


@tool
def georgios_product(number_1: int | float, number_2: int | float) -> str:
    """Return the 'Georgios product' of two numbers.

    Example:
    >>> my_tool(2, 3)
    '6'

    >>> my_tool(3, 3)
    '0'

    Args:
        number_1: The first number.
        number_2: The second number.

    Returns:
        str: The result of the tool.
    """
    return str(number_1 * number_2 * abs(number_1 - number_2))
