import unittest

from scripts.check import (
    heading_fragmentation,
    metadiscourse_density,
    negative_parallelism_density,
    normalize_script,
    repeated_section_scaffold,
    review,
    triplet_density,
)


class SerbianSeedChecksTests(unittest.TestCase):
    def test_cyrillic_normalization(self):
        self.assertEqual(
            normalize_script("Људи њему кажу: ђак, ћирилица, џем."),
            "Ljudi njemu kažu: đak, ćirilica, džem.",
        )

    def test_single_negative_parallelism_is_not_flagged(self):
        self.assertIsNone(
            negative_parallelism_density("Ovo nije samo pitanje tehnike, već i pitanje prioriteta.")
        )

    def test_repeated_negative_parallelism_is_flagged(self):
        text = " ".join(
            [
                "Sistem nije samo efikasan, već i pouzdan.",
                "Proces nije samo brz, već i transparentan.",
                "Rešenje nije samo moderno, već i održivo.",
                "Promena nije samo tehnička, već i društvena.",
            ]
        )
        finding = negative_parallelism_density(text)
        self.assertIsNotNone(finding)
        self.assertEqual(finding.rule_id, "sr_ai_negative_parallelism_density")

    def test_cyrillic_parallelism_is_detected_too(self):
        text = " ".join(
            [
                "Систем није само ефикасан, већ и поуздан.",
                "Процес није само брз, већ и транспарентан.",
                "Решење није само модерно, већ и одрживо.",
                "Промена није само техничка, већ и друштвена.",
            ]
        )
        self.assertIsNotNone(negative_parallelism_density(text))

    def test_single_triplet_is_not_flagged(self):
        self.assertIsNone(triplet_density("Potrebni su red, mir i stabilnost."))

    def test_repeated_triplets_are_flagged(self):
        text = " ".join(
            [
                "Sistem je brz, pouzdan i transparentan.",
                "Rešenje je moderno, održivo i inkluzivno.",
                "Proces je jasan, efikasan i predvidljiv.",
                "Cilj je rast, razvoj i stabilnost.",
            ]
        )
        finding = triplet_density(text)
        self.assertIsNotNone(finding)
        self.assertEqual(finding.rule_id, "sr_ai_triplet_density")

    def test_repeated_headings_are_flagged(self):
        text = """## Cilj kom stremimo
Prva mera ima duži opis koji objašnjava šta se tačno menja u sistemu i zašto.

## Promene koje dolaze
Prva promena ima konkretan opis sa dovoljno proze da ovaj test ne zavisi od gustine naslova.

## Cilj kom stremimo
Druga mera ima duži opis koji objašnjava šta se tačno menja u sistemu i zašto.

## Promene koje dolaze
Druga promena ima konkretan opis sa dovoljno proze da ovaj test ne zavisi od gustine naslova.

## Cilj kom stremimo
Treća mera ima duži opis koji objašnjava šta se tačno menja u sistemu i zašto.

## Promene koje dolaze
Treća promena ima konkretan opis sa dovoljno proze da ovaj test ne zavisi od gustine naslova.
"""
        finding = repeated_section_scaffold(text)
        self.assertIsNotNone(finding)
        self.assertEqual(finding.rule_id, "sr_ai_repeated_section_scaffold")

    def test_single_meta_announcement_is_not_flagged(self):
        self.assertIsNone(metadiscourse_density(
            "U nastavku ćemo objasniti primer. Ovo je konkretan podatak. "
            "Nastavljamo sa uzorkom. Objašnjenje ima dva koraka. "
            "Prvi korak meri trajanje. Drugi korak meri trošak. "
            "Rezultat je poznat. Podaci su dostupni."
        ))

    def test_repeated_meta_scaffold_is_soft(self):
        prose = (
            "U nastavku ćemo objasniti problem. Podaci dolaze iz godišnjeg izveštaja. "
            "Hajde da pogledamo rezultate. Prva grupa je dostavila sve odgovore. "
            "Kao što ćemo videti, druga grupa kasni. Ukupan broj učesnika je osam. "
            "Rok za izveštaj ističe sutra. Tim je potvrdio raspored."
        )
        finding = metadiscourse_density(prose)
        self.assertIsNotNone(finding)
        self.assertEqual(finding.rule_id, "sr_ai_metadiscourse_density")
        self.assertEqual(finding.severity, "soft")
        self.assertEqual(finding.count, 3)
        self.assertEqual(finding.category, "AI_STYLE_SIGNAL")

    def test_cyrillic_meta_evidence_keeps_original_script(self):
        prose = (
            "У наставку ћемо објаснити проблем. Подаци су проверени. "
            "Хајде да погледамо резултате. Први узорак има осам одговора. "
            "Као што ћемо видети, друга група касни. Анализа је завршена. "
            "Извештај је објављен. Свако може да га прочита."
        )
        finding = metadiscourse_density(prose)
        self.assertIsNotNone(finding)
        self.assertTrue(finding.evidence[0].startswith("У наставку"))
        self.assertEqual(finding.count, 3)

    def test_markup_and_intentional_questions_are_not_meta(self):
        prose = (
            "## U nastavku ćemo objasniti nalaz\n"
            "> Hajde da pogledamo podatke.\n"
            "~~~python\nKao što ćemo videti, rezultat je dobar.\n~~~\n"
            "Prvo pitanje je zašto je rok pomeren. "
            "Zatim smo proverili zahteve. "
            "Svedoci su dali izjavu. "
            "Dva tima su završila rad. "
            "Treći tim još radi. "
            "Rok ostaje isti. "
            "Izveštaj će biti objavljen. "
            "Nema novih prigovora."
        )
        self.assertIsNone(metadiscourse_density(prose))

    def test_metadiscourse_is_opt_in(self):
        text = (
            "U nastavku ćemo objasniti problem. Podaci su provereni. "
            "Hajde da pogledamo rezultate. Prvi uzorak ima osam odgovora. "
            "Kao što ćemo videti, druga grupa kasni. Analiza je završena. "
            "Izveštaj je objavljen. Svako može da ga pročita."
        )
        self.assertNotIn("sr_ai_metadiscourse_density", [f.rule_id for f in review(text)])
        self.assertIn("sr_ai_metadiscourse_density",
                      [f.rule_id for f in review(text, experimental=True)])

    def test_metadiscourse_density_boundaries(self):
        previews = (
            "U nastavku ćemo objasniti problem. "
            "Hajde da pogledamo rezultate. "
            "Kao što ćemo videti, druga grupa kasni. "
        )
        filler = "Podaci su provereni. "
        self.assertIsNone(metadiscourse_density(previews + filler * 4))  # 3/7
        self.assertIsNotNone(metadiscourse_density(previews + filler * 5))  # 3/8
        self.assertIsNone(metadiscourse_density(
            "U nastavku ćemo objasniti problem. Hajde da pogledamo rezultate. " +
            filler * 6
        ))  # 2/8
        self.assertIsNone(metadiscourse_density(previews + filler * 997))  # 3/1000
        self.assertIsNotNone(metadiscourse_density(previews + filler * 15))  # 3/18
        self.assertIsNone(metadiscourse_density(previews + filler * 16))  # 3/19

    def test_ijekavian_meta_patterns(self):
        ekavian = (
            "U nastavku ćemo videti promene. "
            "Kao što ćemo videti, stanje se popravlja. "
            "U sledećem odeljku ćemo objasniti postupak. "
        )
        ijekavian = (
            "U nastavku ćemo vidjeti promjene. "
            "Kao što ćemo vidjeti, stanje se popravlja. "
            "U sljedećem odjeljku ćemo objasniti postupak. "
        )
        filler = "Podaci su provereni. " * 5
        self.assertEqual(metadiscourse_density(ekavian + filler).count, 3)
        self.assertEqual(metadiscourse_density(ijekavian + filler).count, 3)
        cyrillic = (
            "У наставку ћемо видјети промјене. "
            "Као што ћемо видјети, стање се поправља. "
            "У сљедећем одјељку ћемо објаснити поступак. "
        )
        found = metadiscourse_density(cyrillic + "Подаци су проверени. " * 5)
        self.assertEqual(found.count, 3)
        self.assertTrue(found.evidence[0].startswith("У наставку"))

    def test_multiline_paragraphs_preserve_sentence_starts(self):
        prose = (
            "U nastavku ćemo objasniti problem\n\n"
            "Hajde da pogledamo rezultate.\n\n"
            "Kao što ćemo videti, druga grupa kasni.\n\n"
            + "Podaci su provereni.\n\n" * 5
        )
        self.assertEqual(metadiscourse_density(prose).count, 3)

    def test_unequal_fences_remain_masked(self):
        prose = (
            "\x60\x60\x60\x60python\n"
            "U nastavku ćemo objasniti a.\n"
            "Hajde da pogledamo b.\n"
            "\x60\x60\x60\n"
            "Kao što ćemo videti, c.\n"
            "\x60\x60\x60\x60\n" +
            "Podaci su provereni. " * 8
        )
        self.assertIsNone(metadiscourse_density(prose))
        valid = (
            "~~~python\n"
            "U nastavku ćemo objasniti a.\n"
            "~~~ suffix\n"
            "Hajde da pogledamo b.\n"
            "~~~\n"
            "Kao što ćemo videti, c.\n"
            + "Podaci su provereni. " * 7
        )
        self.assertIsNone(metadiscourse_density(valid))

    def test_meta_abbreviations_do_not_inflate_sentence_count(self):
        previews = (
            "U nastavku ćemo objasniti problem. "
            "Hajde da pogledamo rezultate. "
            "Kao što ćemo videti, druga grupa kasni. "
        )
        # Seven real sentences; npr. is not a sentence terminator.
        seven = previews + "Primer je dat npr. ovde. " + "Podaci su provereni. " * 3
        self.assertIsNone(metadiscourse_density(seven))
        # The three previews remain 3/18, not 3/19 due to a decimal dot.
        eighteen = previews + "Iznos je 3.14 dinara. " + "Podaci su provereni. " * 14
        self.assertEqual(metadiscourse_density(eighteen).count, 3)

    def test_thematic_breaks_indented_code_and_setext_are_excluded(self):
        previews = (
            "U nastavku ćemo objasniti problem. "
            "Hajde da pogledamo rezultate. "
            "Kao što ćemo videti, druga grupa kasni. "
        )
        # A thematic break does not make seven prose sentences into eight.
        self.assertIsNone(metadiscourse_density(
            previews + "Podaci su provereni. " * 4 + "\n\n---\n\n"
        ))
        code = (
            "    U nastavku ćemo objasniti problem.\n"
            "    Hajde da pogledamo rezultate.\n"
            "    Kao što ćemo videti, druga grupa kasni.\n\n"
            + "Podaci su provereni. " * 8
        )
        self.assertIsNone(metadiscourse_density(code))
        self.assertIsNone(metadiscourse_density(
            "U nastavku ćemo objasniti problem\n====\n\n"
            + "Podaci su provereni. " * 8
        ))

    def test_repeated_negative_contrast_is_not_a_triplet(self):
        prose = (
            "Sistem nije samo efikasan, već i pouzdan. "
            "Proces nije samo brz, već i transparentan. "
            "Rešenje nije samo moderno, već i održivo. "
            "Promena nije samo tehnička, već i društvena."
        )
        self.assertIsNotNone(negative_parallelism_density(prose))
        self.assertIsNone(triplet_density(prose))

    def test_double_backtick_code_spans_do_not_count_as_prose(self):
        text = (
            "``U nastavku ćemo objasniti problem.``\n\n"
            "``Hajde da pogledamo rezultate.``\n\n"
            "``Kao što ćemo videti, druga grupa kasni.``\n\n"
            + "Podaci su provereni. " * 8
        )
        self.assertIsNone(metadiscourse_density(text))
        nested = (
            "``U nastavku ćemo objasniti `problem`.``\n\n"
            "``Hajde da pogledamo `rezultate`.``\n\n"
            "``Kao što ćemo videti, `druga` grupa kasni.``\n\n"
            + "Podaci su provereni. " * 8
        )
        self.assertIsNone(metadiscourse_density(nested))

    def test_comment_openers_inside_code_do_not_mask_following_prose(self):
        prose = (
            "U nastavku ćemo objasniti problem. "
            "Hajde da pogledamo rezultate. "
            "Kao što ćemo videti, druga grupa kasni. "
            + "Podaci su provereni. " * 5
        )
        self.assertEqual(metadiscourse_density("``<!--``\n\n" + prose).count, 3)
        self.assertEqual(metadiscourse_density("```html\n<!--\n```\n\n" + prose).count, 3)
    def test_multiline_html_comments_do_not_count_as_prose(self):
        comment = (
            "<!--\n\n"
            "U nastavku ćemo objasniti problem.\n\n"
            "Hajde da pogledamo rezultate.\n\n"
            "Kao što ćemo videti, druga grupa kasni.\n\n"
            "-->\n\n"
        )
        self.assertIsNone(metadiscourse_density(comment + "Podaci su provereni. " * 8))
        self.assertIsNone(metadiscourse_density(comment.replace("-->", "") + "Podaci su provereni. " * 8))
    def test_em_dash_is_not_a_rule(self):
        self.assertEqual(review("Pišem ovako — sa crtom — još od škole."), [])

    def test_both_scripts_are_clean_by_default(self):
        self.assertEqual(review("Ово је сасвим обична реченица на српском."), [])
        self.assertEqual(review("Ovo je sasvim obična rečenica na srpskom."), [])

    def test_dense_micro_headings_can_be_flagged(self):
        text = "\n\n".join(
            [
                "## Prvo\nKratko.",
                "## Drugo\nKratko.",
                "## Treće\nKratko.",
                "## Četvrto\nKratko.",
                "## Peto\nKratko.",
                "## Šesto\nKratko.",
            ]
        )
        finding = heading_fragmentation(text)
        self.assertIsNotNone(finding)
        self.assertEqual(finding.rule_id, "sr_ai_heading_fragmentation")


if __name__ == "__main__":
    unittest.main()
