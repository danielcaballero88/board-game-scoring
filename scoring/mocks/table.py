from .mock_data import tables


def get_table(table_id: str) -> dict | None:
    """Get table data."""
    return tables.get(table_id)
