#!/usr/bin/env python3

""" Tests for WITX parsing """

import os
import unittest
import witxcraft.parse as wp

WITX_DIR = os.path.join(os.path.dirname(__file__), "witx-bindgen", "codegen")


class TestParse(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def parse_witx(self, witx_file):
        """ Parse the given WITX file and return the parsed object """
        with open(os.path.join(WITX_DIR, witx_file), "r") as in_file:
            return wp.parse_witx(in_file.read())

    def test_char(self):
        out = self.parse_witx("char.witx")
        funcs = out["functions"]
        self.assertEqual(set(funcs.keys()), set(["take_char", "return_char"]))
        self.assertEqual(str(funcs["take_char"]), "function(x: char)")
        self.assertEqual(str(funcs["return_char"]), "function() -> char")

    def test_conventions(self):
        out = self.parse_witx("conventions.witx")

        funcs = out["functions"]
        self.assertEqual(
            set(funcs.keys()),
            set(
                [
                    "camelCase",
                    "snake_case",
                    "SHOUTY_SNAKE_CASE",
                    "foo",
                    "function with space",
                    "function~with$weird&characters",
                    "function again with space",
                ]
            ),
        )

        records = out["records"]
        self.assertEqual(
            set(records.keys()), set(["LUDICROUS_speed", "record with space"])
        )

        types = out["types"]
        self.assertEqual(set(types.keys()), set(["type with space"]))

        variants = out["variants"]
        self.assertEqual(set(variants.keys()), set(["variant with space"]))

        resources = out["resources"]
        self.assertEqual(set(resources.keys()), set(["resource with space"]))

    def test_empty(self):
        out = self.parse_witx("empty.witx")
        self.assertEqual(len(out["functions"]), 0)
        self.assertEqual(len(out["records"]), 0)
        self.assertEqual(len(out["types"]), 0)
        self.assertEqual(len(out["variants"]), 0)
        self.assertEqual(len(out["resources"]), 0)
        self.assertEqual(len(out["flags"]), 0)

    def test_flags(self):
        out = self.parse_witx("flags.witx")

        def gen_flags(n):
            out = []
            for i in range(n):
                out.append("b{}".format(i))
            return ", ".join(out) + ","

        flags = out["flags"]
        self.assertEqual(
            set(flags.keys()),
            set(["flag1", "flag2", "flag4", "flag8", "flag16", "flag32", "flag64"]),
        )
        self.assertEqual(
            repr(flags["flag1"]), "flags flag1 {{ {} }}".format(gen_flags(1))
        )
        self.assertEqual(
            repr(flags["flag2"]), "flags flag2 {{ {} }}".format(gen_flags(2))
        )
        self.assertEqual(
            repr(flags["flag4"]), "flags flag4 {{ {} }}".format(gen_flags(4))
        )
        self.assertEqual(
            repr(flags["flag8"]), "flags flag8 {{ {} }}".format(gen_flags(8))
        )
        self.assertEqual(
            repr(flags["flag16"]), "flags flag16 {{ {} }}".format(gen_flags(16))
        )
        self.assertEqual(
            repr(flags["flag32"]), "flags flag32 {{ {} }}".format(gen_flags(32))
        )
        self.assertEqual(
            repr(flags["flag64"]), "flags flag64 {{ {} }}".format(gen_flags(64))
        )

        funcs = out["functions"]
        self.assertEqual(
            set(funcs.keys()),
            set(
                [
                    "roundtrip_flag1",
                    "roundtrip_flag2",
                    "roundtrip_flag4",
                    "roundtrip_flag8",
                    "roundtrip_flag16",
                    "roundtrip_flag32",
                    "roundtrip_flag64",
                ]
            ),
        )
        self.assertEqual(str(funcs["roundtrip_flag1"]), "function(x: flag1) -> flag1")
        self.assertEqual(str(funcs["roundtrip_flag2"]), "function(x: flag2) -> flag2")
        self.assertEqual(str(funcs["roundtrip_flag4"]), "function(x: flag4) -> flag4")
        self.assertEqual(str(funcs["roundtrip_flag8"]), "function(x: flag8) -> flag8")
        self.assertEqual(
            str(funcs["roundtrip_flag16"]), "function(x: flag16) -> flag16"
        )
        self.assertEqual(
            str(funcs["roundtrip_flag32"]), "function(x: flag32) -> flag32"
        )
        self.assertEqual(
            str(funcs["roundtrip_flag64"]), "function(x: flag64) -> flag64"
        )

    def test_floats(self):
        out = self.parse_witx("floats.witx")

        funcs = out["functions"]

        self.assertEqual(
            set(funcs.keys()),
            set(["f32_param", "f64_param", "f32_result", "f64_result"]),
        )
        self.assertEqual(str(funcs["f32_param"]), "function(x: f32)")
        self.assertEqual(str(funcs["f64_param"]), "function(x: f64)")
        self.assertEqual(str(funcs["f32_result"]), "function() -> f32")
        self.assertEqual(str(funcs["f64_result"]), "function() -> f64")

    def test_integers(self):
        out = self.parse_witx("integers.witx")

        funcs = out["functions"]

        self.assertEqual(
            set(funcs),
            set(
                [
                    "a1",
                    "a2",
                    "a3",
                    "a4",
                    "a5",
                    "a6",
                    "a7",
                    "a8",
                    "a9",
                    "r1",
                    "r2",
                    "r3",
                    "r4",
                    "r5",
                    "r6",
                    "r7",
                    "r8",
                    "pair_ret",
                    "multi_ret",
                ]
            ),
        )

        self.assertEqual(str(funcs["a1"]), "function(x: u8)")
        self.assertEqual(str(funcs["a2"]), "function(x: s8)")
        self.assertEqual(str(funcs["a3"]), "function(x: u16)")
        self.assertEqual(str(funcs["a4"]), "function(x: s16)")
        self.assertEqual(str(funcs["a5"]), "function(x: u32)")
        self.assertEqual(str(funcs["a6"]), "function(x: s32)")
        self.assertEqual(str(funcs["a7"]), "function(x: u64)")
        self.assertEqual(str(funcs["a8"]), "function(x: s64)")

        self.assertEqual(
            str(funcs["a9"]),
            "function(p1: u8, p2: s8, p3: u16, p4: s16, "
            + "p5: u32, p6: s32, p7: u64, p8: s64)",
        )

        self.assertEqual(str(funcs["r1"]), "function() -> u8")
        self.assertEqual(str(funcs["r2"]), "function() -> s8")
        self.assertEqual(str(funcs["r3"]), "function() -> u16")
        self.assertEqual(str(funcs["r4"]), "function() -> s16")
        self.assertEqual(str(funcs["r5"]), "function() -> u32")
        self.assertEqual(str(funcs["r6"]), "function() -> s32")
        self.assertEqual(str(funcs["r7"]), "function() -> u64")
        self.assertEqual(str(funcs["r8"]), "function() -> s64")

        self.assertEqual(str(funcs["pair_ret"]), "function() -> tuple<s64, u8>")
        self.assertEqual(str(funcs["multi_ret"]), "function() -> (s64, u8)")

    def test_legacy(self):
        """ Legacy parsing not implemented """
        return

    def test_lists(self):
        out = self.parse_witx("lists.witx")

        funcs = out["functions"]
        records = out["records"]
        variants = out["variants"]
        types = out["types"]

        #
        # Functions
        #
        self.assertEqual(
            set(funcs.keys()),
            set(
                [
                    "list_u8_param",
                    "list_u16_param",
                    "list_u32_param",
                    "list_u64_param",
                    "list_s8_param",
                    "list_s16_param",
                    "list_s32_param",
                    "list_s64_param",
                    "list_f32_param",
                    "list_f64_param",
                    "list_u8_ret",
                    "list_u16_ret",
                    "list_u32_ret",
                    "list_u64_ret",
                    "list_s8_ret",
                    "list_s16_ret",
                    "list_s32_ret",
                    "list_s64_ret",
                    "list_f32_ret",
                    "list_f64_ret",
                    "tuple_list",
                    "string_list_arg",
                    "string_list_ret",
                    "tuple_string_list",
                    "string_list",
                    "record_list",
                    "variant_list",
                    "load_store_everything",
                ]
            ),
        )

        self.assertEqual(str(funcs["list_u8_param"]), "function(x: list<u8>)")
        self.assertTrue(wp.is_list(funcs["list_u8_param"].args["x"]))
        self.assertTrue(wp.is_u8(funcs["list_u8_param"].args["x"].dtype))
        self.assertEqual(str(funcs["list_u16_param"]), "function(x: list<u16>)")
        self.assertEqual(str(funcs["list_u32_param"]), "function(x: list<u32>)")
        self.assertEqual(str(funcs["list_u64_param"]), "function(x: list<u64>)")
        self.assertEqual(str(funcs["list_s8_param"]), "function(x: list<s8>)")
        self.assertEqual(str(funcs["list_s16_param"]), "function(x: list<s16>)")
        self.assertEqual(str(funcs["list_s32_param"]), "function(x: list<s32>)")
        self.assertEqual(str(funcs["list_s64_param"]), "function(x: list<s64>)")
        self.assertEqual(str(funcs["list_f32_param"]), "function(x: list<f32>)")
        self.assertEqual(str(funcs["list_f64_param"]), "function(x: list<f64>)")

        self.assertEqual(str(funcs["list_u8_ret"]), "function() -> list<u8>")
        self.assertEqual(str(funcs["list_u16_ret"]), "function() -> list<u16>")
        self.assertEqual(str(funcs["list_u32_ret"]), "function() -> list<u32>")
        self.assertEqual(str(funcs["list_u64_ret"]), "function() -> list<u64>")
        self.assertEqual(str(funcs["list_s8_ret"]), "function() -> list<s8>")
        self.assertEqual(str(funcs["list_s16_ret"]), "function() -> list<s16>")
        self.assertEqual(str(funcs["list_s32_ret"]), "function() -> list<s32>")
        self.assertEqual(str(funcs["list_s64_ret"]), "function() -> list<s64>")
        self.assertEqual(str(funcs["list_f32_ret"]), "function() -> list<f32>")
        self.assertEqual(str(funcs["list_f64_ret"]), "function() -> list<f64>")

        self.assertEqual(
            str(funcs["tuple_list"]),
            "function(x: list<tuple<u8, s8>>) -> list<tuple<s64, u32>>",
        )
        self.assertEqual(str(funcs["string_list_arg"]), "function(a: list<string>)")
        self.assertEqual(str(funcs["string_list_ret"]), "function() -> list<string>")
        self.assertEqual(
            str(funcs["tuple_string_list"]),
            "function(x: list<tuple<u8, string>>) -> list<tuple<string, u8>>",
        )
        self.assertEqual(
            str(funcs["string_list"]), "function(x: list<string>) -> list<string>"
        )
        self.assertEqual(
            str(funcs["record_list"]),
            "function(x: list<some_record>) -> list<other_record>",
        )
        self.assertEqual(
            str(funcs["variant_list"]),
            "function(x: list<some_variant>) -> list<other_variant>",
        )
        self.assertEqual(
            str(funcs["load_store_everything"]),
            "function(a: load_store_all_sizes) -> load_store_all_sizes",
        )

        #
        # Records
        #
        self.assertEqual(
            repr(records["some_record"]),
            "record some_record { x: string, y: other_record, "
            + "c1: u32, c2: u64, c3: s32, c4: s64, }",
        )
        self.assertEqual(
            repr(records["other_record"]),
            "record other_record { a1: u32, a2: u64, a3: s32, "
            + "a4: s64, b: string, c: list<u8>, }",
        )

        #
        # Variants
        #
        self.assertEqual(
            repr(variants["some_variant"]),
            "variant some_variant { a(string), b, c(u32), d(list<other_variant>), }",
        )
        self.assertEqual(
            repr(variants["other_variant"]),
            "variant other_variant { a, b(u32), c(string), }",
        )

        #
        # Types
        #
        self.assertEqual(
            repr(types["load_store_all_sizes"]),
            "list<tuple<string, u8, s8, u16, s16, u32, s32, u64, s64, f32, f64, char>>",
        )

    def test_records(self):
        out = self.parse_witx("records.witx")

        funcs = out["functions"]
        records = out["records"]
        types = out["types"]

        self.assertEqual(str(funcs["tuple_arg"]), "function(x: tuple<char, u32>)")
        self.assertEqual(str(funcs["tuple_result"]), "function() -> tuple<char, u32>")

        self.assertEqual(repr(records["empty"]), "record empty {}")
        self.assertEqual(str(funcs["empty_arg"]), "function(x: empty)")
        self.assertEqual(str(funcs["empty_result"]), "function() -> empty")

        self.assertEqual(repr(records["scalars"]), "record scalars { a: u32, b: u32, }")
        self.assertEqual(str(funcs["scalar_arg"]), "function(x: scalars)")
        self.assertEqual(str(funcs["scalar_result"]), "function() -> scalars")

        self.assertEqual(
            repr(records["really_flags"]),
            "record really_flags { a: bool, b: bool, c: bool, d: bool, "
            + "e: bool, f: bool, g: bool, h: bool, i: bool, }",
        )
        self.assertEqual(str(funcs["flags_arg"]), "function(x: really_flags)")
        self.assertEqual(str(funcs["flags_result"]), "function() -> really_flags")

        self.assertEqual(
            repr(records["aggregates"]),
            "record aggregates { a: scalars, b: u32, c: empty, "
            + "d: string, e: really_flags, }",
        )
        self.assertEqual(str(funcs["aggregate_arg"]), "function(x: aggregates)")
        self.assertEqual(str(funcs["aggregate_result"]), "function() -> aggregates")

        self.assertEqual(repr(types["tuple_typedef"]), "tuple<s32>")
        self.assertEqual(repr(types["int_typedef"]), "s32")
        self.assertEqual(repr(types["tuple_typedef2"]), "tuple<int_typedef>")
        self.assertEqual(
            str(funcs["typedef_inout"]), "function(e: tuple_typedef2) -> s32"
        )

    def test_resource(self):
        out = self.parse_witx("resource.witx")

        funcs = out["functions"]
        resources = out["resources"]

        self.assertEqual(repr(resources["x"]), "resource x")

        self.assertEqual(str(funcs["acquire_an_x"]), "function() -> x")
        self.assertEqual(str(funcs["receive_an_x"]), "function(val: x)")

        self.assertEqual(
            repr(resources["y"]),
            "resource y {\n  method_on_y: function()\n  method_with_param: "
            + "function(x: u32)\n  method_with_result: function() -> string\n  "
            + "static some_constructor: function() -> y\n}",
        )

    def test_simple_functions(self):
        out = self.parse_witx("simple_functions.witx")

        funcs = out["functions"]

        self.assertEqual(set(funcs.keys()), set(["f1", "f2", "f3", "f4", "f5", "f6"]))

        self.assertEqual(str(funcs["f1"]), "function()")
        self.assertEqual(str(funcs["f2"]), "function(a: u32)")
        self.assertEqual(str(funcs["f3"]), "function(a: u32, b: u32)")

        self.assertEqual(str(funcs["f4"]), "function() -> u32")
        self.assertEqual(str(funcs["f5"]), "function() -> (u32, u32)")

        self.assertEqual(
            str(funcs["f6"]), "function(a: u32, b: u32, c: u32) -> (u32, u32, u32)"
        )

    def test_simple_lists(self):
        out = self.parse_witx("simple_lists.witx")

        funcs = out["functions"]

        self.assertEqual(
            set(funcs.keys()),
            set(["simple_list1", "simple_list2", "simple_list3", "simple_list4"]),
        )

        self.assertEqual(str(funcs["simple_list1"]), "function(l: list<u32>)")
        self.assertEqual(str(funcs["simple_list2"]), "function() -> list<u32>")
        self.assertEqual(
            str(funcs["simple_list3"]),
            "function(a: list<u32>, b: list<u32>) -> (list<u32>, list<u32>)",
        )
        self.assertEqual(
            str(funcs["simple_list4"]),
            "function(l: list<list<u32>>) -> list<list<u32>>",
        )

    def test_smoke(self):
        out = self.parse_witx("smoke.witx")
        funcs = out["functions"]
        self.assertEqual(set(funcs.keys()), set(["y"]))
        self.assertEqual(str(funcs["y"]), "function()")

    def test_strings(self):
        out = self.parse_witx("strings.witx")

        funcs = out["functions"]

        self.assertEqual(set(funcs.keys()), set(["a", "b", "c"]))

        self.assertEqual(str(funcs["a"]), "function(x: string)")
        self.assertEqual(str(funcs["b"]), "function() -> string")
        self.assertEqual(str(funcs["c"]), "function(a: string, b: string) -> string")

    def test_variants(self):
        out = self.parse_witx("variants.witx")

        funcs = out["functions"]
        variants = out["variants"]
        enums = out["enums"]
        unions = out["unions"]

        # enum
        self.assertEqual(repr(enums["e1"]), "enum e1 { a, }")
        self.assertEqual(str(funcs["e1_arg"]), "function(x: e1)")
        self.assertEqual(str(funcs["e1_result"]), "function() -> e1")
        self.assertTrue(wp.is_enum(funcs["e1_arg"].args["x"]))
        self.assertTrue(wp.is_enum(funcs["e1_result"].results[0]))

        # union
        self.assertEqual(repr(unions["u1"]), "union u1 { u32, f32, }")
        self.assertEqual(str(funcs["u1_arg"]), "function(x: u1)")
        self.assertEqual(str(funcs["u1_result"]), "function() -> u1")
        self.assertTrue(wp.is_union(funcs["u1_arg"].args["x"]))
        self.assertTrue(wp.is_union(funcs["u1_result"].results[0]))

        # variant
        self.assertEqual(
            repr(variants["v1"]),
            "variant v1 { a, b(u1), c(e1), d(string), e(empty), f, g(u32), }",
        )
        self.assertEqual(str(funcs["v1_arg"]), "function(x: v1)")
        self.assertEqual(str(funcs["v1_result"]), "function() -> v1")
        self.assertTrue(wp.is_variant(funcs["v1_arg"].args["x"]))
        self.assertTrue(wp.is_variant(funcs["v1_result"].results[0]))

        self.assertFalse(wp.is_record(funcs["v1_arg"].args["x"]))
        self.assertFalse(wp.is_record(funcs["v1_result"].results[0]))

        # bool
        self.assertEqual(str(funcs["bool_arg"]), "function(x: bool)")
        self.assertEqual(str(funcs["bool_result"]), "function() -> bool")
        self.assertTrue(wp.is_bool(funcs["bool_arg"].args["x"]))
        self.assertTrue(wp.is_bool(funcs["bool_result"].results[0]))

        # option
        self.assertEqual(
            str(funcs["option_arg"]),
            "function(a: option<bool>, b: option<tuple<>>, c: option<u32>, "
            + "d: option<e1>, e: option<f32>, f: option<u1>, g: option<option<bool>>)",
        )
        self.assertEqual(
            str(funcs["option_result"]),
            "function() -> (option<bool>, option<tuple<>>, option<u32>, "
            + "option<e1>, option<f32>, option<u1>, option<option<bool>>)",
        )
        self.assertTrue(wp.is_option(funcs["option_arg"].args["a"]))
        self.assertTrue(wp.is_bool(funcs["option_arg"].args["a"], include_option=True))

        # variant casts
        self.assertEqual(repr(variants["casts1"]), "variant casts1 { a(s32), b(f32), }")
        self.assertEqual(repr(variants["casts2"]), "variant casts2 { a(f64), b(f32), }")
        self.assertEqual(repr(variants["casts3"]), "variant casts3 { a(f64), b(u64), }")
        self.assertEqual(repr(variants["casts4"]), "variant casts4 { a(u32), b(s64), }")
        self.assertEqual(repr(variants["casts5"]), "variant casts5 { a(f32), b(s64), }")
        self.assertEqual(
            repr(variants["casts6"]),
            "variant casts6 { a(tuple<f32, u32>), b(tuple<u32, u32>), }",
        )
        self.assertEqual(
            str(funcs["casts"]),
            "function(a: casts1, b: casts2, c: casts3, d: casts4, e: casts5, "
            + "f: casts6) -> (casts1, casts2, casts3, casts4, casts5, casts6)",
        )

        self.assertTrue(wp.is_variant(variants["casts1"]))
        self.assertTrue(wp.is_variant(variants["casts2"]))
        self.assertTrue(wp.is_variant(variants["casts3"]))
        self.assertTrue(wp.is_variant(variants["casts4"]))
        self.assertTrue(wp.is_variant(variants["casts5"]))
        self.assertTrue(wp.is_variant(variants["casts6"]))

        self.assertTrue(wp.is_variant(funcs["casts"].args["a"]))
        self.assertTrue(wp.is_variant(funcs["casts"].args["b"]))
        self.assertTrue(wp.is_variant(funcs["casts"].args["c"]))
        self.assertTrue(wp.is_variant(funcs["casts"].args["d"]))
        self.assertTrue(wp.is_variant(funcs["casts"].args["e"]))
        self.assertTrue(wp.is_variant(funcs["casts"].args["f"]))

        # expected
        self.assertEqual(
            str(funcs["expected_arg"]),
            "function(a: expected<_, _>, b: expected<_, e1>, "
            + "c: expected<e1, _>, d: expected<tuple<>, tuple<>>, "
            + "e: expected<u32, v1>, f: expected<string, list<u8>>)",
        )
        self.assertEqual(
            str(funcs["expected_result"]),
            "function() -> (expected<_, _>, expected<_, e1>, "
            + "expected<e1, _>, expected<tuple<>, tuple<>>, "
            + "expected<u32, v1>, expected<string, list<u8>>)",
        )

        self.assertTrue(wp.is_expected(funcs["expected_arg"].args["a"]))
        self.assertTrue(wp.is_expected(funcs["expected_arg"].args["b"]))
        self.assertTrue(wp.is_expected(funcs["expected_arg"].args["c"]))
        self.assertTrue(wp.is_expected(funcs["expected_arg"].args["d"]))
        self.assertTrue(wp.is_expected(funcs["expected_arg"].args["e"]))
        self.assertTrue(wp.is_expected(funcs["expected_arg"].args["f"]))

        self.assertTrue(wp.is_expected(funcs["expected_result"].results[0]))
        self.assertTrue(wp.is_expected(funcs["expected_result"].results[1]))
        self.assertTrue(wp.is_expected(funcs["expected_result"].results[2]))
        self.assertTrue(wp.is_expected(funcs["expected_result"].results[3]))
        self.assertTrue(wp.is_expected(funcs["expected_result"].results[4]))
        self.assertTrue(wp.is_expected(funcs["expected_result"].results[5]))

        # enum
        self.assertEqual(repr(enums["my_errno"]), "enum my_errno { bad1, bad2, }")

        # expected
        self.assertEqual(
            str(funcs["return_expected_sugar"]), "function() -> expected<s32, my_errno>"
        )
        self.assertEqual(
            str(funcs["return_expected_sugar2"]), "function() -> expected<_, my_errno>"
        )
        self.assertEqual(
            str(funcs["return_expected_sugar3"]),
            "function() -> expected<my_errno, my_errno>",
        )
        self.assertEqual(
            str(funcs["return_expected_sugar4"]),
            "function() -> expected<tuple<s32, u32>, my_errno>",
        )
        self.assertEqual(str(funcs["return_option_sugar"]), "function() -> option<s32>")
        self.assertEqual(
            str(funcs["return_option_sugar2"]), "function() -> option<my_errno>"
        )
        self.assertEqual(
            str(funcs["expected_simple"]), "function() -> expected<u32, s32>"
        )

        self.assertTrue(wp.is_expected(funcs["return_expected_sugar"].results[0]))
        self.assertTrue(wp.is_expected(funcs["return_expected_sugar2"].results[0]))
        self.assertTrue(wp.is_expected(funcs["return_expected_sugar3"].results[0]))
        self.assertTrue(wp.is_expected(funcs["return_expected_sugar4"].results[0]))

        self.assertTrue(wp.is_option(funcs["return_option_sugar"].results[0]))
        self.assertTrue(wp.is_option(funcs["return_option_sugar2"].results[0]))
        self.assertTrue(
            wp.is_s32(funcs["return_option_sugar"].results[0], include_option=True)
        )
        self.assertTrue(
            wp.is_enum(funcs["return_option_sugar2"].results[0], include_option=True)
        )
        self.assertTrue(wp.is_expected(funcs["expected_simple"].results[0]))
        self.assertTrue(wp.is_u32(funcs["expected_simple"].results[0].dtype1))
        self.assertTrue(wp.is_s32(funcs["expected_simple"].results[0].dtype2))


if __name__ == "__main__":
    unittest.main()
