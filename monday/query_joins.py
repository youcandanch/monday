import json
from monday.utils import python_json_stringify


# Eventually I will organize this file better but you know what today is not that day.

# ITEM RESOURCE QUERIES
def mutate_item_query(board, group, item, column_values):
    if column_values is None:
        column_values = {}

    query = '''mutation
    {
        create_item (
            board_id: %s,
            group_id: %s,
            item_name: "%s",
            column_values: %s
        ) {
            id
        }
    }''' % (board, group, item, python_json_stringify(column_values))

    return query


def get_item_query(board, column, value):
    query = '''query
        {
            items_by_column_values(
                board_id: %s,
                column_id: %s,
                column_value: "%s"
            ) {
                id
                name
                updates {
                    id
                    body
                }
                group {
                    id
                    title
                }
                column_values {
                    id
                    text
                    value
                }
            }
        }''' % (board, column, value)

    return query


def get_item_by_id_query(ids):
    query = '''query
        {
            items (ids: %s) {
                name,
                group {
                    id
                    title
                }
                column_values {
                    id,
                    text,
                    value
                }
            }
        }''' % ids

    return query


def update_item_query(board, item, column, value):
    query = '''mutation
        {
            change_column_value(
                board_id: %s,
                item_id: %s,
                column_id: %s,
                value: %s
            ) {
                id
                name
                column_values {
                    id
                    text
                    value
                }
            }
        }''' % (board, item, column, python_json_stringify(value))

    return query


def update_multiple_column_values_query(board_id, item_id, column_values):

   query = '''mutation
        {
            change_multiple_column_values (
                board_id: %s,
                item_id: %s,
                column_values: %s
            ) {
                id
                name
                column_values {
                  id
                  text
                }
            }
        }''' % (board_id, item_id, python_json_stringify(column_values))

   return query


# UPDATE RESOURCE QUERIES
def create_update_query(item_id, update_value):
    query = '''mutation
        {
            create_update(
                item_id: %s,
                body: %s
            ) {
                id
            }
        }''' % (item_id, json.dumps(update_value))

    return query


def get_update_query(limit, page):
    query = '''query
        {
            updates (
                limit: %s,
                page: %s
            ) {
                id,
                body
            }
        }''' % (limit, page if page else 1)

    return query


# TAG RESOURCE QUERIES
def get_tags_query(tags):
    if tags is None:
        tags = []

    query = '''query
        {
            tags (ids: %s) {
                name,
                color,
                id
            }
        }''' % tags

    return query


# BOARD RESOURCE QUERIES
def get_board_items_query(board_id):
    query = '''query
    {
        boards(ids: %s) {
            name
            items {
                id
                name
                column_values {
                  id
                  text
                  type
                  value
                }
            }
        }
    }''' % board_id

    return query


def get_boards_query(**kwargs):
    query = '''query
    {
        boards (%s) {
            id
            name
            permissions
            tags {
              id
              name
            }
            groups {
                id
                title
            }
            columns {
                id
                title
                type
            }
        }
    }''' % ', '.join(["%s: %s" % (arg, kwargs.get(arg)) for arg in kwargs])
    return query


def get_boards_by_id_query(board_ids):
    return '''query
    {
        boards (ids: %s) {
            id
            name
            permissions
            tags {
              id
              name
            }
            groups {
                id
                title
            }
            columns {
                id
                title
                type
                settings_str
            }
        }
    }''' % board_ids


def get_columns_by_board_query(board_ids):
    return '''query
        {
            boards(ids: %s) {
                id
                name
                groups {
                    id
                    title
                }
                columns {
                    title
                    id
                    type
                    settings_str
                 }
            }
        }''' % board_ids


# USER RESOURCE QUERIES
def get_users_query(**kwargs):
    query = '''query
    {
        users (%s) {
            id
            name
            email
            enabled
            teams {
              id
              name
            }
        }
    }''' % ', '.join(["%s: %s" % (arg, kwargs.get(arg)) for arg in kwargs])
    return query
