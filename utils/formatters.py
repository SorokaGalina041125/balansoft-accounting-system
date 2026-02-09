"""Formatting utilities for Balansoft."""


def format_currency(amount: float, currency: str = "RUB") -> str:
    """Format amount as currency."""
    return f"{amount:,.0f} {currency}".replace(",", " ")
