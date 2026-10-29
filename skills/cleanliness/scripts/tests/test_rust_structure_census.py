from __future__ import annotations

import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace

SCRIPT = Path(__file__).parents[1] / "rust-structure-census.py"
SPEC = importlib.util.spec_from_file_location("rust_structure_census", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
CENSUS = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CENSUS
SPEC.loader.exec_module(CENSUS)


class MaskingTests(unittest.TestCase):
    def test_masks_comments_and_literals_but_preserves_lines(self) -> None:
        source = '''//! Charter.
fn real() {
    let normal = "fn fake() { match x { A => { 1 } } }";
    let raw = r###"|x| { fake }"###;
    let byte = b'{';
    // fn commented() { }
    /* outer { /* nested => { } */ } */
}
'''
        masked = CENSUS.mask_non_code(source)

        self.assertEqual(source.count("\n"), masked.count("\n"))
        self.assertIn("fn real() {", masked)
        self.assertNotIn("fake", masked)
        self.assertNotIn("commented", masked)
        self.assertEqual(1, masked.count("{"))

    def test_does_not_treat_lifetime_as_character_literal(self) -> None:
        source = "fn borrow<'a>(value: &'a str) -> &'a str { value }\n"
        masked = CENSUS.mask_non_code(source)
        self.assertIn("'a", masked)


class AnalysisTests(unittest.TestCase):
    SOURCE = '''//! Owns the fixture behavior.

fn dispatch(value: Value) -> Result<()> {
    let callback = |writer: &mut Writer| {
        writer.line("start");
        if value.ready() {
            writer.line("ready");
        }
    };

    match value {
        Value::First(item) => {
            use_item(item);
            finish_item(item);
        }
        Value::Second(item) => emit_second(item),
    }
}

trait Contract {
    fn declaration_only(&self);
}
'''

    def test_finds_defined_functions_closures_and_braced_match_arms(self) -> None:
        analysis = CENSUS.analyze_source("src/example.rs", self.SOURCE)

        self.assertTrue(analysis.file.starts_with_charter)
        self.assertEqual(1, analysis.file.functions)
        self.assertEqual(1, analysis.file.closures)
        self.assertEqual(1, analysis.file.match_arms)
        self.assertEqual("dispatch", analysis.functions[0].name)
        self.assertGreaterEqual(analysis.functions[0].nesting, 2)
        self.assertGreater(analysis.closures[0].lines, 1)
        self.assertGreater(analysis.match_arms[0].lines, 1)

    def test_thresholds_are_independent_review_triggers(self) -> None:
        analysis = CENSUS.analyze_source("src/example.rs", self.SOURCE)
        records = CENSUS.threshold_records(
            [analysis],
            file_lines=1,
            function_lines=10_000,
            nesting=2,
            closure_lines=1,
            match_arm_lines=1,
        )

        self.assertEqual(1, len(records["files"]))
        self.assertEqual(0, len(records["not_starting_with_charters"]))
        self.assertEqual(0, len(records["functions"]))
        self.assertEqual(1, len(records["deep_functions"]))
        self.assertEqual(1, len(records["closures"]))
        self.assertEqual(1, len(records["match_arms"]))

    def test_const_generics_do_not_truncate_function_body(self) -> None:
        source = '''fn render<T: Trait<{ 8 }>>(value: T)
where
    T: Other<{ 16 }>,
{
    if value.ready() {
    }
}
'''
        analysis = CENSUS.analyze_source("src/generic.rs", source)

        self.assertEqual(1, len(analysis.functions))
        self.assertEqual("render", analysis.functions[0].name)
        self.assertEqual(1, analysis.functions[0].start_line)
        self.assertEqual(7, analysis.functions[0].end_line)
        self.assertEqual(7, analysis.functions[0].lines)
        self.assertEqual(1, analysis.functions[0].nesting)

    def test_finds_destructuring_and_typed_array_closures(self) -> None:
        source = '''fn use_all() {
    let first = |Record { id, value }| {
        consume(id, value);
    };
    let second = async move |buffer: [u8; 32]| -> Result<Vec<u8>> {
        consume(buffer);
    };
}
'''
        analysis = CENSUS.analyze_source("src/closures.rs", source)

        self.assertEqual(2, len(analysis.closures))
        self.assertEqual([3, 3], [item.lines for item in analysis.closures])

    def test_reports_raw_and_unicode_function_names(self) -> None:
        decomposed = "cafe\N{COMBINING ACUTE ACCENT}"
        source = f"fn r#type() {{}}\nfn café() {{}}\nfn {decomposed}() {{}}\n"
        analysis = CENSUS.analyze_source("src/names.rs", source)

        self.assertEqual(
            ["r#type", "café", decomposed],
            [item.name for item in analysis.functions],
        )

    def test_output_discloses_per_category_truncation(self) -> None:
        analysis = CENSUS.analyze_source("src/example.rs", self.SOURCE)
        analyses = [analysis, analysis]
        records = CENSUS.threshold_records(
            analyses,
            file_lines=1,
            function_lines=1,
            nesting=1,
            closure_lines=1,
            match_arm_lines=1,
        )
        args = SimpleNamespace(
            path=[],
            include_tests=False,
            limit=1,
            file_lines=1,
            function_lines=1,
            nesting=1,
            closure_lines=1,
            match_arm_lines=1,
        )
        document = CENSUS.output_document(Path("/repo"), args, analyses, records)

        self.assertEqual(1, document["schema_version"])
        self.assertEqual(
            {
                "schema_version",
                "notice",
                "scope",
                "thresholds",
                "summary",
                "trigger_counts",
                "selection",
                "records",
            },
            set(document),
        )
        self.assertEqual(
            {
                "files",
                "not_starting_with_charters",
                "functions",
                "deep_functions",
                "closures",
                "match_arms",
            },
            set(document["records"]),
        )
        self.assertEqual(1, document["selection"]["limit"])
        self.assertTrue(document["selection"]["truncated"]["functions"])
        output = io.StringIO()
        with redirect_stdout(output):
            CENSUS.print_table(document)
        self.assertIn("Large functions (showing 1 of 2 triggers)", output.getvalue())

    def test_charter_must_start_the_file_preamble(self) -> None:
        self.assertTrue(CENSUS.starts_with_module_charter("\n//! Charter.\nfn item() {}\n"))
        self.assertTrue(CENSUS.starts_with_module_charter("#!/usr/bin/env rustx\n//! Charter.\n"))
        self.assertFalse(CENSUS.starts_with_module_charter("/// Item docs.\nfn item() {}\n"))
        self.assertFalse(CENSUS.starts_with_module_charter("#![allow(dead_code)]\n//! Charter.\n"))


class ClassificationTests(unittest.TestCase):
    def test_classifies_test_surfaces(self) -> None:
        self.assertTrue(CENSUS.is_test_path("crates/demo/tests/integration.rs"))
        self.assertTrue(CENSUS.is_test_path("src/parser_tests.rs"))
        self.assertTrue(CENSUS.is_test_path("src/test.rs"))
        self.assertTrue(CENSUS.is_test_path("src/tests.rs"))
        self.assertTrue(CENSUS.is_test_path("benches/parser.rs"))
        self.assertFalse(CENSUS.is_test_path("src/parser.rs"))


if __name__ == "__main__":
    unittest.main()
