
def is_float_of_str(value: str) -> bool:
    try:
        _ = float(value)
        return True
    except ValueError:
        return False
