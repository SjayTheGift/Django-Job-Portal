from django import template

register = template.Library()

@register.filter
def money(value, arg=None):
    """
    Converts a number into a money format.

    Usage:
        {{ number|money }}
        {{ number|money:"R" }}
        {{ number|money:"R,2" }}
        {{ number|money:"R,2,m" }}
    """
    if not value:
        return ''

    try:
        amount = float(value)
    except (TypeError, ValueError):
        return value

    currency = 'R'
    decimal_places = 2
    suffix = ''

    if arg:
        parts = arg.split(',')
        currency = parts[0] if parts else currency
        decimal_places = int(parts[1]) if len(parts) > 1 else decimal_places
        suffix = parts[2].strip().lower() if len(parts) > 2 else ''

    if abs(amount) >= 1000000000000:
        amount /= 1000000000000
        suffix = 't'
    elif abs(amount) >= 1000000000:
        amount /= 1000000000
        suffix = 'b'
    elif abs(amount) >= 1000000:
        amount /= 1000000
        suffix = 'm'
    elif abs(amount) >= 1000:
        amount /= 1000
        suffix = 'k'

    return f"{currency}{amount:,.{decimal_places}f}{suffix}"