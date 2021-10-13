#!/usr/bin/env python3

""" Construct CREATE FUNCTION SQL statemnts from functions in a WITX file """

import witxcraft.parse as wp

DB_TYPE_MAP = {
    "f64": "double",
    "string": "varchar(256)",
    "s64": "bigint",
    "list<u8>": "varchar(256)",
}
SQL = 'CREATE OR REPLACE FUNCTION {}({}) RETURNS TABLE({}) AS WASM INFILE "{}";'


def expand_record(rec):
    """ Expand record into its individual fields """
    args = []
    for key, dtype in rec.fields.items():
        dtype, is_option = expand_option(dtype)
        args.append(
            "{} {}{}".format(
                key, DB_TYPE_MAP[str(dtype)], not is_option and " not null" or ""
            )
        )
    return args


def expand_option(dtype):
    """
    Return the inner data type of an option

    Parameters
    ----------
    dtype : any
        The type to check to see if it is an option.

    Returns
    -------
    (inner-dtype, bool)
        The first result is the inner data type of the option.
        The second result is a bool indicating whether or not the
        input argument was actually an option.

    """
    if wp.is_option(dtype):
        return dtype.inner_type, True
    return dtype, False


if __name__ == "__main__":
    import argparse

    cli_args = argparse.ArgumentParser(description=__doc__)
    cli_args.add_argument("witx_file", metavar="<path>", help="path to file or URL")
    cli_args.add_argument(
        "wasm_file", metavar="<path>", help="path to WASM file to include in SQL"
    )
    cli_args = cli_args.parse_args()

    data = wp.parse_witx(cli_args.witx_file)

    for func in data["functions"].values():
        args = []
        for name, dtype in func.args.items():
            if wp.is_record(dtype):
                args.extend(expand_record(data["records"][str(dtype)]))
            else:
                args.append("{} {}".format(name, DB_TYPE_MAP[str(dtype)]))
        args = ", ".join(args)

        if wp.is_list(func.results[0]):
            results = ", ".join(expand_record(func.results[0].dtype))
        else:
            results = ", ".join(expand_record(func.results[0]))

        print(SQL.format(func.name, args, results, cli_args.wasm_file))
