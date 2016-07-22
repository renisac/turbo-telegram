COLUMNS = ['name', 'status', 'domains', 'prefixes', 'asns', 'created_at', 'updated_at']
MAX_FIELD_SIZE = 30

from ri_registry.format.table import Table

FORMATS = {'table': Table}
