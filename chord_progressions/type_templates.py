from chord_progressions import logger
from chord_progressions.pitch import (
    get_note_from_midi_num,
    get_pitch_class_from_midi_num,
    get_pitch_class_from_note,
)
from chord_progressions.utils import is_circular_match

"""
From https://web.archive.org/web/20221116234056/https://vladimir_ladma.sweb.cz/english/music/structs/mus_rot.htm

Further readings:

Forte, Allen. The Structure of Atonal Music. New Haven: Yale, 1973

Solomon, Larry. "The List of Chords, Their Properties, and Uses", Interface, Journal of New Music Research, Vol. 11 (1982)

Strauss, Joseph N. Post-Tonal Theory, Prentice-Hall, 1990.

Ideally we'd like to reduce this to a smaller set, say by remapping.
I wonder if there is a perceptual study that can be done for this.

remap = {
 'minor-ninth chord': 'minor-seventh chord',
 'major-ninth chord': 'major-seventh chord',
 'diminished chord': 'tritone',
 'dominant-ninth,major-minor|prometheus pentamirror': 'tritone',
 'italian sixth|incomplete dominant-seventh chord 1': 'tritone',
 'dominanth-11th|natural / genuine / lydian hexachord': 'tritone',
 'pyramid': 'tritone',
}
"""

TYPE_TEMPLATES = {
    "": "",
    "unison": "100000000000",
    "semitone": "110000000000",
    "whole-tone": "101000000000",
    "bach / chromatic trimirror": "111000000000",
    "minor third": "100100000000",
    "phrygian trichord": "110100000000",
    "minor trichord": "101100000000",
    "major third": "100010000000",
    "major-minor trichord 1": "110010000000",
    "whole-tone trichord": "101010000000",
    "major-second tetracluster 2": "111010000000",
    "major-minor trichord 2": "100110000000",
    "alternating tetramirror": "110110000000",
    "major-second tetracluster 1": "101110000000",
    "chromatic pentamirror": "111110000000",
    "perfect fourth": "100001000000",
    "incomplete minor-seventh chord": "101001000000",
    "minor-third tetracluster 2": "111001000000",
    "incomplete dominant-seventh chord 2": "100101000000",
    "dorian tetrachord|phrygian tetrachord": "110101000000",
    "phrygian tetrachord|minor tetramirror": "101101000000",
    "major-second pentacluster 2": "111101000000",
    "chromatic mezotetrachord|arabian tetramirror": "110011000000",
    "lydian tetrachord|major tetrachord": "101011000000",
    "minor-second major pentachord": "111011000000",
    "minor-third tetracluster 1": "100111000000",
    "spanish pentacluster": "110111000000",
    "major-second pentacluster 1": "101111000000",
    "chromatic hexamirror": "111111000000",
    "tritone": "100000100000",
    "rite chord 2|tritone-fourth 1": "110000100000",
    "italian sixth|incomplete dominant-seventh chord 1": "101000100000",
    "major-third tetracluster 2": "111000100000",
    "diminished chord": "100100100000",
    "minor-second diminished tetrachord": "110100100000",
    "harmonic-minor tetrachord": "101100100000",
    "blues pentacluster": "111100100000",
    "incomplete half-dim-seventh chord": "100010100000",
    "all-interval tetrachord 1": "110010100000",
    "whole-tone tetramirror": "101010100000",
    "tritone-expanding pentachord": "111010100000",
    "major-third diminished tetrachord": "100110100000",
    "alternating pentachord 1": "110110100000",
    "tritone-symmetric pentamirror": "101110100000",
    "rite chord 1|tritone-fourth 2": "100001100000",
    "double fourth tetramirror": "110001100000",
    "all-interval tetrachord 2": "101001100000",
    "oriental pentacluster 1": "111001100000",
    "perfect-fourth diminished tetrachord": "100101100000",
    "locrian pentamirror": "110101100000",
    "alternating pentachord 2": "101101100000",
    "major-third tetracluster 1": "100011100000",
    "oriental pentacluster 2": "110011100000",
    "tritone-contracting pentachord": "101011100000",
    "minor-third pentacluster": "100111100000",
    "chromatic heptamirror": "111111100000",
    "quartal trichord": "101000010000",
    "perfect fourth tetramirror": "111000010000",
    "minor chord": "100100010000",
    "all-interval tetrachord 3": "110100010000",
    "major-second minor tetrachord": "101100010000",
    "major-third pentacluster 1": "111100010000",
    "major chord": "100010010000",
    "major-diminished tetrachord": "110010010000",
    "major-second major tetrachord": "101010010000",
    "major-seventh pentacluster 2": "111010010000",
    "major-minor tetramirror": "100110010000",
    "major-minor-dim pentachord 1": "110110010000",
    "center-cluster pentachord 1": "101110010000",
    "minor-second quartal tetrachord": "110001010000",
    "quartal tetramirror": "101001010000",
    "double-seconds triple-fourth pentachord 1": "111001010000",
    "perfect-fourth minor tetrachord": "100101010000",
    "phrygian pentachord": "110101010000",
    "dorian / minor pentachord": "101101010000",
    "perfect-fourth major tetrachord": "100011010000",
    "gypsy / semiditonic pentachord 1": "110011010000",
    "major / ionic pentachord": "101011010000",
    "center-cluster pentachord 2": "100111010000",
    "messiaen's truncated 5|lendvai's|double tritone tetramirror": "110000110000",
    "tritone quartal tetrachord": "101000110000",
    "double pentacluster1": "111000110000",
    "minor-diminished tetrachord": "100100110000",
    "javanese pentachord": "110100110000",
    "gypsy / semiditonic pentachord 2": "101100110000",
    "all-interval tetrachord 4": "100010110000",
    "balinese pentachord": "110010110000",
    "lydian pentachord": "101010110000",
    "major-minor-dim pentachord 2": "100110110000",
    "alternating hexamirror": "110110110000",
    "double pentacluster 2": "110001110000",
    "double-seconds triple-fourth pentachord 2": "101001110000",
    "double-cluster hexamirror": "111001110000",
    "major-seventh pentacluster 1": "100101110000",
    "major-third pentacluster 2": "100011110000",
    "chromatic octamirror": "111111110000",
    "augmented chord": "100010001000",
    "minor-augmented tetrachord": "110010001000",
    "augmented pentacluster 1": "111010001000",
    "augmented-major tetrachord": "100110001000",
    "minor-major ninth chord": "110110001000",
    "augmented pentacluster 2": "101110001000",
    "major-seventh chord": "110001001000",
    "half-diminished seventh chord": "101001001000",
    "diminished pentacluster 1": "111001001000",
    "minor-seventh chord": "100101001000",
    "major-ninth chord": "110101001000",
    "diminished-major ninth chord": "101101001000",
    "syrian pentatonic|major-augmented ninth chord": "110011001000",
    "diminished-augmented ninth chord": "101011001000",
    "center-cluster pentamirror": "100111001000",
    "french-sixth chord|messiaen's truncated 6": "101000101000",
    "bardos's|assymetric pentamirror": "111000101000",
    "dominant-seventh / german-sixth chord": "100100101000",
    "kumoi pentachord 2": "110100101000",
    "augmented-sixth pentachord 1": "101100101000",
    "enigmatic pentachord 1": "110010101000",
    "whole-tone pentamirror": "101010101000",
    "augmented-diminished ninth chord": "100110101000",
    "balinese pelog pentatonic|korean": "110001101000",
    "augmented-sixth pentachord 2|indian hindola|javan pentatonic": "101001101000",
    "minor-diminished ninth chord": "100101101000",
    "locrian hexachord|suddha saveriraga": "110101101000",
    "super-locrian hexamirror": "101101101000",
    "indian-japan pentatonic": "101100011000",
    "persian pentamirror": "110010011000",
    "enigmatic pentachord 2|altered pentatonic": "101010011000",
    "lebanese pentachord|augmented-minor chord": "100110011000",
    "megha or 'cloud' raga": "101110011000",
    "korean|kumoi pentachord 1": "101001011000",
    "minor-ninth chord": "100101011000",
    "phrygian hexamirror": "110101011000",
    "minor hexachord": "101101011000",
    "gypsy hexatonic": "110011011000",
    "melodic-minor hexachord": "101011011000",
    "messiaen's 5": "111000111000",
    "diminished pentacluster 2": "100100111000",
    "chromatic nonamirror": "111111111000",
    "diminished-seventh chord": "100100100100",
    "diminished minor-ninth chord": "110100100100",
    "flat-ninth pentachord|ranjaniraga": "101100100100",
    "neapolitan pentachord 1": "110010100100",
    "dominant-ninth,major-minor|prometheus pentamirror": "101010100100",
    "neapolitan pentachord 2": "101001100100",
    "schoenberg anagram hexachord": "111001100100",
    "pyramid": "101101100100",
    "debussy's heptatonic": "111101100100",
    "natural / genuine / 'black key' / blues pentatonic|slendro|bilahariraga": "101010010100",
    "indian dipaka|prometheus neapolitan": "110110010100",
    "indian|blues": "101110010100",
    "scriabin's mystic|prometheus hexachord": "110101010100",
    "dorian hexachord": "101101010100",
    "guidon / arezzo / natural / genuine / persian hexachord|quartal hexamirror": "101011010100",
    "messiaen's truncated 2|minor-bitonal hexachord": "110100110100",
    "dominant-11th|natural / genuine / lydian hexachord": "101010110100",
    "gypsy|moravian pistalkova (whistle)|alternating heptachord 1": "110110110100",
    "blues octatonic 1": "111110110100",
    "indian|chromatic inverse": "111001110100",
    "tritone major heptachord": "101011110100",
    "augmented|messiaen's truncated 3|lendvai's|genus tertium": "110011001100",
    "messiaen's truncated 2|petruskka chord|major-bitonal hexachord": "101100101100",
    "harmonic hexachord|augmented-11th|indian sviraga": "101010101100",
    "neapolitan": "111010101100",
    "harmonic minor|spanish gypsy": "110110101100",
    "persian|gypsy|hungarian|double harmonic|indian bhairava|turkish": "111001101100",
    "harmonic major": "110101101100",
    "diminished|alternating heptachord 2": "101101101100",
    "greek chromatic|indian": "101110011100",
    "modified blues": "101011011100",
    "messiaen's 4": "111100111100",
    "enigmatic heptatonic": "101010111100",
    "enigmatic octatonic|free-constructed": "111010111100",
    "blues octatonic 2": "101011111100",
    "chromatic decamirror": "111111111100",
    "whole-tone|messiaen's mode 1|raga gopriya|anhemitonic hexatonic": "101010101010",
    "neapolitan|leading whole-tone|combined|kafenda's": "111010101010",
    "jazz minor|bartok's|aug 13th heptamirror|acoustic|plane-altered": "110110101010",
    "greek|medieval|natural / genuine": "110101101010",
    "spanish octatonic": "110111101010",
    "greek complete|egyptian|blues|quartal octachord|diatonic octad": "111101011010",
    "spanish|major-minor|blues": "110111011010",
    "nonatonic blues": "111111011010",
    "messiaen's 6": "111010111010",
    "major-minor nonatonic|ramdasi malhar": "111101111010",
    "diminished|messiaen's 2|lendvai's": "110110110110",
    "diminished nonachord": "111011110110",
    "messiaen's 3|tsjerepnin": "111011101110",
    "major-minor mixed": "111111011110",
    "messiaen's 7": "111110111110",
    "chromatic undecamirror": "111111111110",
    "twelve-tone chromatic,dodecamirror": "111111111111",
    # Generated by scripts/build_type_templates.py; appended so that the ids above do not change
    "bach / chromatic tetramirror": "111100000000",
    "pitch-class set 0-1-5": "110001000000",
    "pitch-class set 0-4-5": "100011000000",
    "pitch-class set 0-1-2-3-4-6": "111110100000",
    "pitch-class set 0-1-2-3-5-6": "111101100000",
    "pitch-class set 0-1-2-4-5-6": "111011100000",
    "pitch-class set 0-1-3-4-5-6": "110111100000",
    "pitch-class set 0-2-3-4-5-6": "101111100000",
    "pitch-class set 0-1-2-3-4-7": "111110010000",
    "pitch-class set 0-1-2-3-5-7": "111101010000",
    "pitch-class set 0-1-2-4-5-7": "111011010000",
    "pitch-class set 0-1-3-4-5-7": "110111010000",
    "pitch-class set 0-2-3-4-5-7": "101111010000",
    "pitch-class set 0-1-2-3-4-5-7": "111111010000",
    "pitch-class set 0-1-2-3-6-7": "111100110000",
    "pitch-class set 0-1-2-4-6-7": "111010110000",
    "pitch-class set 0-2-3-4-6-7": "101110110000",
    "pitch-class set 0-1-2-3-4-6-7": "111110110000",
    "pitch-class set 0-1-3-5-6-7": "110101110000",
    "pitch-class set 0-2-3-5-6-7": "101101110000",
    "pitch-class set 0-1-2-3-5-6-7": "111101110000",
    "pitch-class set 0-1-4-5-6-7": "110011110000",
    "raga dipak": "101011110000",
    "pitch-class set 0-1-2-4-5-6-7": "111011110000",
    "pitch-class set 0-3-4-5-6-7": "100111110000",
    "pitch-class set 0-1-3-4-5-6-7": "110111110000",
    "pitch-class set 0-2-3-4-5-6-7": "101111110000",
    "pitch-class set 0-2-4-8": "101010001000",
    "pitch-class set 0-1-2-3-4-8": "111110001000",
    "pitch-class set 0-1-2-3-5-8": "111101001000",
    "pitch-class set 0-1-2-4-5-8": "111011001000",
    "raga saravati (sharavati)": "110111001000",
    "pitch-class set 0-2-3-4-5-8": "101111001000",
    "pitch-class set 0-1-2-3-4-5-8": "111111001000",
    "pitch-class set 0-1-2-3-6-8": "111100101000",
    "arabian major locrian|raga jaganmohanam": "111010101000",
    "raga kamalamanohari|raga sarasvati|raga sindhura kafi": "110110101000",
    "raga jyoti": "101110101000",
    "pitch-class set 0-1-2-3-4-6-8": "111110101000",
    "raga gaula": "111001101000",
    "pitch-class set 0-1-2-3-5-6-8": "111101101000",
    "raga malarani (hamsanada)": "110011101000",
    "pitch-class set 0-2-4-5-6-8": "101011101000",
    "pitch-class set 0-1-2-4-5-6-8": "111011101000",
    "pitch-class set 0-3-4-5-6-8": "100111101000",
    "pitch-class set 0-1-3-4-5-6-8": "110111101000",
    "pitch-class set 0-2-3-4-5-6-8": "101111101000",
    "pitch-class set 0-1-2-3-4-5-6-8": "111111101000",
    "pitch-class set 0-1-2-3-7-8": "111100011000",
    "raga vijayasri": "111010011000",
    "raga paraju|simhavahini|ramamanohari|raga rudra pancama|raga kaikavasi": "110110011000",
    "pitch-class set 0-1-2-3-4-7-8": "111110011000",
    "raga mandari|gamakakriya": "111001011000",
    "raga ragesri": "111101011000",
    "pitch-class set 0-1-2-4-5-7-8": "111011011000",
    "pitch-class set 0-3-4-5-7-8": "100111011000",
    "pitch-class set 0-1-3-4-5-7-8": "110111011000",
    "pitch-class set 0-2-3-4-5-7-8": "101111011000",
    "pitch-class set 0-1-2-3-4-5-7-8": "111111011000",
    "raga tilang|savitri|brindavani-tilang|raga chandrajyoti": "110100111000",
    "raga syamalam|raga vijayavasanta|raga padi": "101100111000",
    "mela salaga": "111100111000",
    "raga dhavalangam": "110010111000",
    "raga jivantika": "101010111000",
    "mela jalarnava": "111010111000",
    "pitch-class set 0-3-4-6-7-8": "100110111000",
    "mela navanitam|raga nabomani": "110110111000",
    "pitch-class set 0-2-3-4-6-7-8": "101110111000",
    "pitch-class set 0-1-2-3-4-6-7-8": "111110111000",
    "pitch-class set 0-2-5-6-7-8": "101001111000",
    "mela jhalavarali|raga varali": "111001111000",
    "pitch-class set 0-3-5-6-7-8": "100101111000",
    "raga madhuri|mela pavani|raga kumbhini": "110101111000",
    "pitch-class set 0-2-3-5-6-7-8": "101101111000",
    "pitch-class set 0-1-2-3-5-6-7-8": "111101111000",
    "mela raghupriya|raga ravikriya|ghandarva": "110011111000",
    "pitch-class set 0-2-4-5-6-7-8": "101011111000",
    "pitch-class set 0-1-2-4-5-6-7-8": "111011111000",
    "pitch-class set 0-3-4-5-6-7-8": "100111111000",
    "pitch-class set 0-1-3-4-5-6-7-8": "110111111000",
    "pitch-class set 0-2-3-4-5-6-7-8": "101111111000",
    "pitch-class set 0-1-2-3-6-9": "111100100100",
    "pitch-class set 0-1-2-4-6-9": "111010100100",
    "raga madhukauns (hexatonic)|raga ghantana": "110110100100",
    "pitch-class set 0-2-3-4-6-9": "101110100100",
    "pitch-class set 0-1-2-3-4-6-9": "111110100100",
    "double-phrygian hexatonic / chord|raga sarasanana": "110101100100",
    "raga jivantini|gaurikriya|raga bauli|raga suddha mukhari": "110011100100",
    "pitch-class set 0-2-4-5-6-9": "101011100100",
    "mela yagapriya|raga kalahamsa": "111011100100",
    "mela sucaritra|raga santanamanjari": "110111100100",
    "pitch-class set 0-2-3-4-5-6-9": "101111100100",
    "pitch-class set 0-1-2-3-4-5-6-9": "111111100100",
    "raga bhanumanjari|raga sarang|megh|raga gurjari todi": "111010010100",
    "mela tanarupi|raga tanukirti": "111110010100",
    "pitch-class set 0-1-2-5-7-9": "111001010100",
    "mela rupavati": "111101010100",
    "raga kalavati|ragamalini|raga latika": "110011010100",
    "mela ragavardhani|raga cudamani|mela varunapriya": "111011010100",
    "pitch-class set 0-1-3-4-5-7-9": "110111010100",
    "pitch-class set 0-2-3-4-5-7-9": "101111010100",
    "pitch-class set 0-1-2-3-4-5-7-9": "111111010100",
    "raga vijayanagari|raga bhinna pancama": "101100110100",
    "mela gavambodhi|raga girvani|mela hatakambari|raga jeyasuddhamalavi": "111100110100",
    "pitch-class set 0-1-4-6-7-9": "110010110100",
    "mela vagadhisvari|raga bhogachayanata|nandkauns|bluesy r&r|mela bhavapriya|raga bhavani|kalamurti|mela naganandini|raga nagabharanam|samanta|viravasantham": "111010110100",
    "pitch-class set 0-2-3-4-6-7-9": "101110110100",
    "mela suvarnangi|raga sauviram": "110101110100",
    "pitch-class set 0-2-3-5-6-7-9": "101101110100",
    "pitch-class set 0-1-2-3-5-6-7-9": "111101110100",
    "mela divyamani": "110011110100",
    "pitch-class set 0-1-2-4-5-6-7-9": "111011110100",
    "pitch-class set 0-1-3-4-5-6-7-9": "110111110100",
    "pitch-class set 0-2-3-4-5-6-7-9": "101111110100",
    "pitch-class set 0-1-2-3-4-5-6-7-9": "111111110100",
    "raga takka|raga hejjajji|raga simharava (sinharavam)": "101011001100",
    "mela gangeyabhusani|raga gangatarangini|mela nitimati|raga nisada": "111011001100",
    "mela dhatuvardhani|raga dhauta pancama|devarashtra|mela gayakapriya|raga kalakanti|gipsy hexatonic": "110111001100",
    "mela dhavalambari|foulds' mantra of will scale|verdi's enigmatic descending": "101111001100",
    "pitch-class set 0-1-2-3-4-5-8-9": "111111001100",
    "mela syamalangi|raga shyamalam|mela visvambhari|raga vamsavathi|mela ganamurti|raga ganasamavarali": "111100101100",
    "mela namanarayani|raga narmada|pratapa": "101110101100",
    "raga cintamani": "111110101100",
    "pitch-class set 0-1-2-3-5-6-8-9": "111101101100",
    "pitch-class set 0-2-4-5-6-8-9": "101011101100",
    "pitch-class set 0-1-2-4-5-6-8-9": "111011101100",
    "pitch-class set 0-1-3-4-5-6-8-9": "110111101100",
    "pitch-class set 0-2-3-4-5-6-8-9": "101111101100",
    "pitch-class set 0-1-2-3-4-5-6-8-9": "111111101100",
    "raga ramkali": "111110011100",
    "mela senavati|raga senagrani|malini|mela suryakanta|bhairubahar that|mela latangi|raga gitapriya": "110101011100",
    "mela jhankaradhvani|raga jhankara bhramavi|marva that|mela gamanasrama|raga partiravam|puriya|mela ratnangi|raga phenadyuti": "101101011100",
    "raga bhatiyar": "111101011100",
    "pitch-class set 0-1-2-4-5-7-8-9": "111011011100",
    "mela jyotisvarupini|raga jotismatti|raga saurastra": "110111011100",
    "pitch-class set 0-2-3-4-5-7-8-9": "101111011100",
    "pitch-class set 0-1-2-3-4-5-7-8-9": "111111011100",
    "maqam hijaz|maqam shadd'araban|algerian": "110110111100",
    "pitch-class set 0-2-3-4-6-7-8-9": "101110111100",
    "pitch-class set 0-1-2-3-4-6-7-8-9": "111110111100",
    "pitch-class set 0-1-3-5-6-7-8-9": "110101111100",
    "pitch-class set 0-2-3-5-6-7-8-9": "101101111100",
    "pitch-class set 0-1-2-3-5-6-7-8-9": "111101111100",
    "pitch-class set 0-1-2-4-5-6-7-8-9": "111011111100",
    "pitch-class set 0-1-3-4-5-6-7-8-9": "110111111100",
    "pitch-class set 0-2-3-4-5-6-7-8-9": "101111111100",
    "pitch-class set 0-1-2-3-4-6-8-10": "111110101010",
    "raga mian ki malhar": "111101101010",
    "pitch-class set 0-1-2-4-5-6-8-10": "111011101010",
    "pitch-class set 0-1-2-3-4-5-6-8-10": "111111101010",
    "zirafkend: arabic": "111011011010",
    "pitch-class set 0-1-3-4-6-7-8-10": "110110111010",
    "pitch-class set 0-1-2-3-4-6-7-8-10": "111110111010",
    "pitch-class set 0-1-2-4-5-6-7-8-10": "111011111010",
    "pitch-class set 0-1-3-4-5-6-7-8-10": "110111111010",
    "pitch-class set 0-1-2-3-4-5-6-7-8-10": "111111111010",
    "pitch-class set 0-1-2-3-4-6-7-9-10": "111110110110",
    "moorish phrygian": "111101110110",
    "raga sindhi-bhairavi": "111111110110",
    "pitch-class set 0-1-2-3-4-5-6-8-9-10": "111111101110",
}


def get_template_from_pitch_classes(pcs):
    """e.g. [0, 4, 7] -> [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]"""
    template = [0] * 12

    for ix in pcs:
        template[ix] = 1

    return template


def get_template_from_midi_nums(midi_nums):
    """e.g. [48, 60] -> [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"""
    pitch_classes = [get_pitch_class_from_midi_num(n) for n in midi_nums]

    return get_template_from_pitch_classes(pitch_classes)


def get_template_from_template_str(template_str):
    """e.g. "101010101010" -> [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]"""
    return [int(i) for i in list(template_str)]


def get_type_from_template(template):
    for chord_type in list(TYPE_TEMPLATES):
        if is_circular_match(
            template,
            get_template_from_template_str(TYPE_TEMPLATES[chord_type]),
        ):
            return chord_type
    return None


def get_type_from_type_num(num):
    """Takes the id of a chord type and returns its name"""
    return list(TYPE_TEMPLATES)[num]


def get_types_from_type_num_str(type_num_str):
    """Takes a type_num_str and returns a list of type names"""
    types = []

    for num in type_num_str.split("_"):
        if num == "":
            types.append("")
        else:
            types.append(get_type_from_type_num(int(num)))

    return types


def get_type_num_from_type(chord_type):
    """Takes the name of a chord type and returns its id"""
    if not chord_type:
        return None

    return list(TYPE_TEMPLATES).index(chord_type)


def notes_match_chord_type(notes, chord_type):
    """Returns true if any rotation of `notes` fit `chord_type`"""
    return is_circular_match(
        get_template_from_notes(notes),
        get_template_from_template_str(TYPE_TEMPLATES[chord_type]),
    )


def get_type_from_notes(notes):
    """
    Returns the first exact template match. Returns "" if no match.
    e.g. ["C4", "C3"] -> "unison"

    TODO: find partial matches as well
    """
    for chord_type in list(TYPE_TEMPLATES):
        if notes_match_chord_type(notes, chord_type):
            return chord_type

    logger.debug(f"No type template matched chord: {notes}")
    return ""


def get_type_from_midi_nums(midi_nums):
    """
    Returns the first exact template match
    e.g. [48, 60] -> "unison"
    """
    notes = [get_note_from_midi_num(n) for n in midi_nums]
    return get_type_from_notes(notes)


def get_template_from_notes(notes):
    """e.g. ["C4", "E4", "G4"] -> [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]"""
    pitch_classes = [get_pitch_class_from_note(n) for n in notes]

    return get_template_from_pitch_classes(pitch_classes)
