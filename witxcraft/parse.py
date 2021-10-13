#!/usr/bin/env python3

"""
WITX Parsing Utilities

This module includes utilities to parse the WITX syntax used by the `witx-bindgen`
tool at https://github.com/bytecodealliance/witx-bindgen.

Example::

    import witxcraft.parse as wp

    out = wp.parse_witx("my_func: function(a: s32) -> u64")

    my_func = out["functions"]["my_func"]

    print(my_func)
    print(wp.is_function(my_func))
    print([(x, str(y)) for x, y in my_func.args.items()])
    print([str(x) for x in my_func.results])
    print(wp.is_s32(my_func.args["a"]))
    print(wp.is_u64(my_func.results[0]))

"""

import collections
import os
import re
import typing
import urllib
from dataclasses import dataclass
from parsimonious import Grammar, NodeVisitor


INTERTYPES = set(
    [
        "u8",
        "u16",
        "u32",
        "u64",
        "s8",
        "s16",
        "s32",
        "s64",
        "f32",
        "f64",
        "char",
        "string",
        "bool",
    ]
)


def _flatten(nested):
    """ Flatten nested lists """
    for item in nested:
        if isinstance(item, collections.abc.Iterable) and not isinstance(
            item, (str, bytes)
        ):
            yield from _flatten(item)
        else:
            yield item


GRAMMAR = Grammar(
    r"""
    expr = (compound / function / type / ws)*
    ws = ~"\s*"
    name = ~"([A-Z_][A-Z0-9_-]*|\"[^\"]+\")"i
    id = ~"([A-Z_][A-Z0-9_-]*|\"[^\"]+\")"i
    intername = (intertype / collection / name)
    intertype = "f32" / "f64"
       / "s8" / "u8" / "s16" / "u16" / "s32" / "u32" / "s64" / "u64"
       / "char" / "string" / option / bool / expected
    collection = list / tuple
    compound = record / variant / flags / enum / union / resource
    list = ("list" ws "<" ws intername ws ">")
    record = ("record" ws name ws "{" ws ((name ws ":" ws intername)
        (ws "," ws name ws ":" ws intername)* ws)? ws ","? ws "}")
    variant_value = (ws name ws ("(" ws intername ws ")" ws)?)
    variant = ("variant" ws name ws "{" variant_value
        (ws "," variant_value)* ws ","? ws "}")
    tuple = ("tuple" ws "<" ws intername? ws (ws "," ws intername)* ws ","? ws ">")
    flags = ("flags" ws name ws "{" ws name (ws "," ws name)* ws ","? ws "}")
    bool = "true" / "false"
    enum = ("enum" ws name ws "{" ws name (ws "," ws name)* ws ","? ws "}")
    option = ("option" ws "<" ws intername ws ">")
    union = ("union" ws name ws "{" ws intername (ws "," ws intername)* ws ","? ws "}")
    expected = ("expected" ws "<" ws (intername / "_") ws "," ws intername ws ">")
    type = ("type" ws name ws "=" ws (intername / collection))
    func_type = "static"
    resource = ("resource" ws name ws ("{" (ws func_type? ws function)* ws "}")? ws)
    arg = (ws name ws ":" ws intername ws)
    return_value = (ws intername ws)
    function = (name ws ":" ws "function" ws "(" arg? ("," arg)* ws ","? ws ")" ws
        ("->" ws (return_value / ("(" (return_value
        ("," return_value)*) ws ","? ws ")")) ws)?)
"""
)


ValueType = typing.TypeVar(
    "ValueType",
    "InterType",
    "Option",
    "List",
    "Tuple",
    "Expected",
    "Variant",
    "Enum",
    "Flags",
    "Record",
)


@dataclass
class InterType:
    """ Structure for all scalar data types """

    name: str

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)


def is_intertype(obj, include_option=False):
    """
    Is the given object an interface type

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return isinstance(obj, InterType)


def is_f32(obj, include_option=False):
    """
    Is the given object an f32?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return is_intertype(obj) and obj.name == "f32"


def is_f64(obj, include_option=False):
    """
    Is the given object an f64?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return is_intertype(obj) and obj.name == "f64"


def is_u8(obj, include_option=False):
    """
    Is the given object an u8?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return is_intertype(obj) and obj.name == "u8"


def is_u16(obj, include_option=False):
    """
    Is the given object an u16?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return is_intertype(obj) and obj.name == "u16"


def is_u32(obj, include_option=False):
    """
    Is the given object an u32?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return is_intertype(obj) and obj.name == "u32"


def is_u64(obj, include_option=False):
    """
    Is the given object an u64?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return is_intertype(obj) and obj.name == "u64"


def is_s8(obj, include_option=False):
    """
    Is the given object an s8?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return is_intertype(obj) and obj.name == "s8"


def is_s16(obj, include_option=False):
    """
    Is the given object an s16?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return is_intertype(obj) and obj.name == "s16"


def is_s32(obj, include_option=False):
    """
    Is the given object an s32?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return is_intertype(obj) and obj.name == "s32"


def is_s64(obj, include_option=False):
    """
    Is the given object an s64?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return is_intertype(obj) and obj.name == "s64"


def is_bool(obj, include_option=False):
    """
    Is the given object an bool?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return is_intertype(obj) and obj.name == "bool"


@dataclass
class Option:
    """ Structure for holding `option<...>` types """

    dtype: ValueType

    def __str__(self):
        return "option<{}>".format(self.dtype)

    def __repr__(self):
        return str(self)

    @property
    def inner_type(self):
        """ Return the type of the innermost non-Option type """
        inner = self.dtype
        while is_option(inner):
            inner = inner.dtype
        return inner


def is_option(obj):
    """
    Is the given object an option?

    Parameters
    ----------
    obj : any
        The object to test.

    Returns
    -------
    bool

    """
    return isinstance(obj, Option)


@dataclass
class Flags:
    """ Structure for holding `flags x { ... }` types """

    name: str
    values: typing.List[str]

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        items = ", ".join([str(x) for x in self.values])
        return "flags {} {{ {}, }}".format(self.name, items).replace("{ , }", "{}")


def is_flags(obj, include_option=False):
    """
    Is the given object a flags structure?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return isinstance(obj, Flags)


@dataclass
class Enum:
    """ Structure for holding `enum x { ... } types """

    name: str
    values: typing.List[str]

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return "enum {} {{ {}, }}".format(
            self.name, ", ".join([str(x) for x in self.values])
        ).replace("{ , }", "{}")


def is_enum(obj, include_option=False):
    """
    Is the given object an enum?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return isinstance(obj, Enum)


@dataclass
class Expected:
    """ Structure for holding `expected<x, y>` types """

    dtype1: typing.Union[ValueType, None]
    dtype2: typing.Union[ValueType, None]

    def __str__(self):
        return "expected<{}, {}>".format(
            self.dtype1 is None and "_" or self.dtype1,
            self.dtype2 is None and "_" or self.dtype2,
        )

    def __repr__(self):
        return str(self)


def is_expected(obj, include_option=False):
    """
    Is the given object an expected structure?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return isinstance(obj, Expected)


@dataclass
class Tuple:
    """ Structure for holding `tuple<...>` types """

    items: typing.List[ValueType]

    def __str__(self):
        items = ", ".join([str(x) for x in self.items])
        return "tuple<{}>".format(items)

    def __repr__(self):
        return str(self)


def is_tuple(obj, include_option=False):
    """
    Is the given object a tuple?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return isinstance(obj, Tuple)


@dataclass
class List:
    """ Structure for holding list<...> types """

    dtype: ValueType

    def __str__(self):
        return "list<{}>".format(self.dtype)

    def __repr__(self):
        return str(self)


def is_list(obj, include_option=False):
    """
    Is the given object a list?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return isinstance(obj, List)


@dataclass
class Record:
    """ Structure for holding `record x { ... }` types """

    name: str
    fields: typing.OrderedDict[str, ValueType]

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        fields = ", ".join(["{}: {}".format(k, v) for k, v in self.fields.items()])
        return "record {} {{ {}, }}".format(self.name, fields).replace("{ , }", "{}")


def is_record(obj, include_option=False):
    """
    Is the given object a record?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return isinstance(obj, Record)


@dataclass
class Union:
    """ Structure for holding `union x { ... }` types """

    name: str
    dtypes: typing.List[ValueType]

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return "union {} {{ {}, }}".format(
            self.name, ", ".join([str(x) for x in self.dtypes])
        ).replace("{ , }", "{}")


def is_union(obj, include_option=False):
    """
    Is the given object a union?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return isinstance(obj, Union)


@dataclass
class Variant:
    """ Structure for holding `variant x { ... }` types """

    name: str
    values: typing.OrderedDict[str, typing.Union[ValueType, None]]

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        values = []
        for key, val in self.values.items():
            if val is None:
                values.append("{}".format(key))
            else:
                values.append("{}({})".format(key, val))
        return "variant {} {{ {}, }}".format(self.name, ", ".join(values)).replace(
            "{ , }", "{}"
        )


def is_variant(obj, include_option=False):
    """
    Is the given object a variant?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return isinstance(obj, Variant)


@dataclass
class _VariantValue:
    """ Temporary structure for parsing variants """

    name: str
    dtype: typing.Optional[ValueType]


@dataclass
class _FunctionArg:
    """ Temporary structure for parsing function arguments """

    name: str
    dtype: typing.Union[ValueType]


@dataclass
class _FunctionResult:
    """ Temporary structure for parsing function results """

    dtype: typing.Union[ValueType]


@dataclass
class Function:
    """ Structure for holding `function()` types """

    name: str
    args: typing.OrderedDict[str, ValueType]
    results: typing.List[ValueType]

    def __str__(self):
        args = ", ".join(["{}: {}".format(k, str(v)) for k, v in self.args.items()])
        results = ", ".join([str(x) for x in self.results])
        if self.results:
            if len(self.results) > 1:
                return "function({}) -> ({})".format(args, results)
            return "function({}) -> {}".format(args, results)
        else:
            return "function({})".format(args)

    def __repr__(self):
        return "{}: {}".format(self.name, str(self))


def is_function(obj, include_option=False):
    """
    Is the given object a function?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return isinstance(obj, Function)


@dataclass
class Resource:
    """ Structure for holding `resource x { ... }` types """

    name: str
    methods: typing.Mapping[str, typing.Mapping[str, Function]]

    def __str__(self):
        funcs = []
        for method_type in self.methods:
            for value in self.methods[method_type].values():
                if method_type == "instance":
                    funcs.append(repr(value))
                else:
                    funcs.append("{} {}".format(method_type, repr(value)))
        if not funcs:
            return "resource {}".format(self.name)
        return "resource {} {{\n  {}\n}}".format(self.name, "\n  ".join(funcs))

    def __repr__(self):
        return str(self)


def is_resource(obj, include_option=False):
    """
    Is the given object a resource?

    Parameters
    ----------
    obj : any
        The object to test.
    include_option : bool, optional
        Should any `option<...>` elements be traversed when checking the type?

    Returns
    -------
    bool

    """
    if include_option and is_option(obj):
        obj = obj.inner_type
    return isinstance(obj, Resource)


class WITXVisitor(NodeVisitor):
    """ Class to traverse a NodeVisitor tree """

    def __init__(self):
        self.all_values = {}
        self.enums = {}
        self.flags = {}
        self.functions = {}
        self.records = {}
        self.resources = {}
        self.types = {}
        self.unions = {}
        self.variants = {}
        super(NodeVisitor, self).__init__()

    def _get_type(self, name):
        if not isinstance(name, str):
            return name
        if name in self.all_values:
            return self.all_values[name]
        if name in INTERTYPES:
            return InterType(name)
        #       print("Unknown data type: {}".format(name))
        return name

    def visit_function(self, node, visited_children):
        name, *rest = list(_flatten(visited_children))
        args = collections.OrderedDict(
            (x.name, x.dtype) for x in rest if isinstance(x, _FunctionArg)
        )
        results = [x.dtype for x in rest if isinstance(x, _FunctionResult)]
        assert (len(args) + len(results)) == len(
            rest
        ), "Unknown value type in function components: {}".format(rest)
        self.functions[name] = Function(name, args, results)
        return self.functions[name]

    def visit_arg(self, node, visited_children):
        args = list(_flatten(visited_children))
        return _FunctionArg(name=args[0], dtype=self._get_type(args[1]))

    def visit_return_value(self, node, visited_children):
        return _FunctionResult(self._get_type(list(_flatten(visited_children))[0]))

    def visit_type(self, node, visited_children):
        name, value = list(_flatten(visited_children))
        self.types[name] = self._get_type(value)

    #       self.all_values[name] = self.types[name]

    def visit_option(self, node, visited_children):
        return Option(self._get_type(list(_flatten(visited_children))[0]))

    def visit_expected(self, node, visited_children):
        val1, val2 = list(_flatten(visited_children))
        val1 = val1 != "_" and self._get_type(val1) or None
        val2 = val2 != "_" and self._get_type(val2) or None
        return Expected(val1, val2)

    def visit_name(self, node, visited_children):
        out = node.text
        if out.startswith('"') and out.endswith('"'):
            return out[1:-1].replace('\\"', '"')
        return out

    def visit_id(self, node, visited_children):
        out = node.text
        if out.startswith('"') and out.endswith('"'):
            return out[1:-1].replace('\\"', '"')
        return out

    def visit_intertype(self, node, visited_children):
        vals = list(_flatten(visited_children))
        if vals:
            assert len(vals) == 1, "nested intertypes must only contain one value"
            assert not isinstance(
                vals[0], str
            ), "nested types should be intertypes, not strings"
            return vals[0]
        return self._get_type(node.text)

    def visit_intername(self, node, visited_children):
        return list(_flatten(visited_children))[0]

    def visit_func_type(self, node, visited_children):
        return node.text.strip()

    def visit_record(self, node, visited_children):
        name, *rest = list(_flatten(visited_children))
        fields = collections.OrderedDict()
        while rest:
            fields[rest.pop(0)] = rest.pop(1)
        self.records[name] = Record(name, fields)
        self.all_values[name] = self.records[name]

    def visit_flags(self, node, visited_children):
        name, *flags = list(_flatten(visited_children))
        self.flags[name] = Flags(name, flags)
        self.all_values[name] = self.flags[name]

    def visit_union(self, node, visited_children):
        name, *dtypes = list(_flatten(visited_children))
        self.unions[name] = Union(name, dtypes)
        self.all_values[name] = self.unions[name]

    def visit_enum(self, node, visited_children):
        name, *values = list(_flatten(visited_children))
        self.enums[name] = Enum(name, values)
        self.all_values[name] = self.enums[name]

    def visit_variant_value(self, node, visited_children):
        name, *value = list(_flatten(visited_children))
        if value:
            return _VariantValue(name, value[0])
        return _VariantValue(name, None)

    def visit_variant(self, node, visited_children):
        name, *values = list(_flatten(visited_children))
        values = collections.OrderedDict((item.name, item.dtype) for item in values)
        self.variants[name] = Variant(name, values)
        self.all_values[name] = self.variants[name]

    def visit_list(self, node, visited_children):
        return List(dtype=self._get_type(list(_flatten(visited_children))[0]))

    def visit_tuple(self, node, visited_children):
        return Tuple(tuple(_flatten(visited_children)))

    def visit_resource(self, node, visited_children):
        name, *funcs = list(_flatten(visited_children))
        methods = {"instance": {}, "static": {}}
        method_type = "instance"
        for value in funcs:
            if isinstance(value, str):
                method_type = value
            else:
                methods[method_type][value.name] = value
                method_type = "instance"
        self.resources[name] = Resource(name, methods)

    def generic_visit(self, node, visited_children):
        return [x for x in visited_children]


def parse_witx(witx):
    """
    Parse WITX content and return definitions

    Parameters
    ----------
    witx : str or file-like or URL
        WITX content to parse.

    Returns
    -------
    dict containing all parsed components

    """
    if isinstance(witx, bytes):
        witx = witx.decode("utf-8")

    # Read content from various possibilities.
    if hasattr(witx, "read"):
        witx = witx.read()
        if isinstance(witx, bytes):
            witx = witx.decode("utf-8")
    elif re.match(r"^(https?|ftp):", witx):
        with urllib.request.urlopen(witx) as inurl:
            witx = inurl.read().decode("utf-8")
    elif os.path.isfile(witx):
        with open(witx, "r") as infile:
            witx = infile.read()

    # Parse the WITX content.
    visitor = WITXVisitor()
    visitor.visit(GRAMMAR.parse(witx))
    return dict(
        enums=visitor.enums,
        flags=visitor.flags,
        functions=visitor.functions,
        records=visitor.records,
        resources=visitor.resources,
        types=visitor.types,
        unions=visitor.unions,
        variants=visitor.variants,
    )
