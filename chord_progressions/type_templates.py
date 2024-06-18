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
