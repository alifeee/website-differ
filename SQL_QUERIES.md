# SQL Queries

Some helpful queries for development.

## Requirements

You can use [SQLite VSCode extension](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite) to run these queries.

Alternatively, you can use the [SQLite CLI](https://sqlite.org/cli.html).

## Queries

### Reassign snapshot IDs

This is useful if you want to test what happens when website content changes.

It will probably need to be modified based on the current state of the database.

### Assign all queries to snapshot 1

```sql
UPDATE queries
SET snapshot_id = 1
WHERE snapshot_id != 1;
```

### Assign specific queries to snapshot 1

```sql
UPDATE queries
SET snapshot_id = 1
WHERE id IN (1, 2, 3);
```
