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
