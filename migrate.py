import rethinkdb as rethink
from app import app
from app import schemas
from pprint import pprint
from termcolor import colored
import marshmallow
import os

# Backup DB


class Colorized:

    @staticmethod
    def failure(message):
        return colored(message, "white", "on_red", attrs=["bold"])

    @staticmethod
    def success(message, bg=True):
        if bg:
            return colored(message, "white", "on_green", attrs=["bold"])

        return colored(message, "green")

    @staticmethod
    def info(message):
        return colored(message, "white", "on_cyan")


class RethinkConnnection:
    defaults = {
        str(marshmallow.fields.String): "",
        str(marshmallow.fields.Integer): 0,
        str(marshmallow.fields.Boolean): True,
        str(marshmallow.fields.Nested): {},  # Going to be a paaaaain
        str(marshmallow.fields.List): []
    }

    def __init__(self, database=app.config["RDB_DB"],
                 host=app.config["RDB_HOST"],
                 port=app.config["RDB_PORT"],
                 blacklist=[]):
        self.db = database
        self.host = host
        self.port = port
        self.blacklist = blacklist
        try:
            self.connection = rethink.connect(
                host=self.host,
                db=self.db,
                port=self.port
            )
        except rethink.errors.ReqlDriverError as e:
            error_msg = Colorized.failure("Database connection failed!")
            print("{} {}".format(error_msg, e))
            raise SystemExit

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.connection.close()
        except AttributeError:
            pass

    def get_tables(self):
        """Get the table list"""
        return list(rethink.table_list().run(self.connection))

    def get_values(self, table):
        """Get all the objects in the table"""
        return list(rethink.table(table).run(self.connection))

    def get_fields(self, table):
        """Returns a list of all the fields in the given table"""
        return set(rethink.table(table)
                   .map(lambda val: val.keys())
                   .reduce(lambda left, right: left + right)
                   .distinct()
                   .run(self.connection))

    def update_values(self, table, update_vals):
        """
        Take a table and a dictionary of new values to update with
        and update the table
        """
        resp = rethink.table(table).update(update_vals).run(self.connection)
        return resp


if __name__ == "__main__":
    conn = RethinkConnnection()
    # A list of the tables in the database if they're not blacklisted
    tables = [
        table for table in conn.get_tables()
        if table not in conn.blacklist
    ]
    # A dictionary of the fields for each table returned
    table_fields = {
        table: conn.get_fields(table)
        for table in tables
    }

    # Iterating over the different schemas defined
    for schema, table in schemas.table_map.items():
        # Get a list of strings for the field names for this schema
        fields = set(getattr(schemas, schema)().fields.keys())
        # A list of all the keys that the database is missing
        db_missing = [
            val for val in fields if val not in table_fields[table]
        ]
        # A dictionary that will be used to update the database
        update_values = {}

        # Iterate over the missing fields (if there are any)
        for field in db_missing:
            # Get the object for the current field
            field_obj = (getattr(schemas, schema)().fields)[field]
            # Does the current field have a custom default set?
            if field_obj.default != marshmallow.missing:
                # Use that
                update_values[field] = field_obj.default
            else:
                # Go with the default as defined in RethinkConnnection
                update_values[field] = conn.defaults[str(type(field_obj))]

        print(Colorized.info("DB response:\t"),
              conn.update_values(table, update_values))
        print(Colorized.success("{} complete!".format(table.capitalize())))
        print('=' * 64)

    print(Colorized.success("Migrations complete!",
                            bg=False).center(os.get_terminal_size().columns))