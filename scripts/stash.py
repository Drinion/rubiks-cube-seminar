SEQUENCE_INDEX = 0
CUBES = []
SECOND_COMPLETED = 0
SECOND_LAYER_CONFS = [[1, "br"],
                      [5, "bo"],
                      [18, "rg"],
                      [22, "og"]]
LAST_LAYER = False
NAMES = []
POS = []
SOLUTION = []
ALGO_CONFIGS = [[7, "bw"], [9, "rw"], [15, "ow"], [24, "gw"],
                [0, "bwr"], [6, "bwo"], [23, "wgo"], [17, "rgw"],
                [1, "br"], [5, "bo"], [18, "rg"], [22, "og"],
                [3, "by"], [666, "skip"], [777, "skip"], [888, "skip"],
                [999, "orient_corners"]]
ALL_CUBE_CONFIGS = [[0, "bwr"],[1, "br"],[2, "byr"],[3, "by"],[4, "boy"],
                    [5, "bo"],[6, "bwo"],[7, "bw"],[8, "b"],[9, "rw"],
                    [10, "r"],[11, "ry"],[12, "y"],[13, "yo"],[14, "o"],
                    [15, "ow"],[16, "w"],[17, "rgw"],[18, "rg"],[19, "ryg"],
                    [20, "yg"],[21, "yog"],[22, "og"],[23, "owg"], [24, "wg"],
                    [26, "g"]]
NO_ANIM = False
PARENT = ""
SKIP = False
RESET = False
N_SOLV_AND_N_ROT = 0
INVOCATIONS = 0
OPTIM_SEQUENCE = ""

SIDES = {
    "a": ["110","100","101","111","1-10","11-1","10-1","1-11","1-1-1"],
    "b": ["-110","-100","-101","-111",'-1-1-1',"-11-1","-1-11","-1-10","-10-1"],
    "c": ["110","010","011","-110","-11-1","01-1","111","11-1","-111"],
    "d": ["1-10","-1-11","1-11","0-10","0-11","0-1-1","-1-1-1","-1-10","1-1-1"],
    "e": ["101","001","111","1-11","-1-11","0-11","-101","-111","011"],
    "f": ["10-1","00-1","11-1","01-1","-11-1","-10-1","-1-1-1","1-1-1","0-1-1"],
    "g": ["110","100","101","111","1-10","11-1","10-1","1-11","1-1-1"],
    "h": ["-110","-100","-101","-111",'-1-1-1',"-11-1","-1-11","-1-10","-10-1"],
    "j": ["110","010","011","-110","-11-1","01-1","111","11-1","-111"],
    "k": ["1-10","-1-11","1-11","0-10","0-11","0-1-1","-1-1-1","-1-10","1-1-1"],
    "l": ["101","001","111","1-11","-1-11","0-11","-101","-111","011"],
    "o": ["10-1","00-1","11-1","01-1","-11-1","-10-1","-1-1-1","1-1-1","0-1-1"],
}

OUTER_SIDES = {
    0: ["1.510","1.500","1.501","1.511","1.5-10","1.51-1","1.50-1","1.5-11","1.5-1-1"],
    1: ["-1.510","-1.500","-1.501","-1.511",'-1.5-1-1',"-1.51-1","-1.5-11","-1.5-10","-1.50-1"],
    2: ["11.50","01.50","01.51","-11.50","-11.5-1","01.5-1","11.51","11.5-1","-11.51"],
    3: ["1-1.50","-1-1.51","1-1.51","0-1.50","0-1.51","0-1.5-1","-1-1.5-1","-1-1.50","1-1.5-1"],
    4: ["101.5","001.5","111.5","1-11.5","-1-11.5","0-11.5","-101.5","-111.5","011.5"],
    5: ["10-1.5","00-1.5","11-1.5","01-1.5","-11-1.5","-10-1.5","-1-1-1.5","1-1-1.5","0-1-1.5"],
}

SIDES_BY_COLOR = {
    "y": ["1.510","1.500","1.501","1.511","1.5-10","1.51-1","1.50-1","1.5-11","1.5-1-1"],
    "w": ["-1.510","-1.500","-1.501","-1.511",'-1.5-1-1',"-1.51-1","-1.5-11","-1.5-10","-1.50-1"],
    "b": ["11.50","01.50","01.51","-11.50","-11.5-1","01.5-1","11.51","11.5-1","-11.51"],
    "g": ["1-1.50","-1-1.51","1-1.51","0-1.50","0-1.51","0-1.5-1","-1-1.5-1","-1-1.50","1-1.5-1"],
    "o": ["101.5","001.5","111.5","1-11.5","-1-11.5","0-11.5","-101.5","-111.5","011.5"],
    "r": ["10-1.5","00-1.5","11-1.5","01-1.5","-11-1.5","-10-1.5","-1-1-1.5","1-1-1.5","0-1-1.5"],
}

LABELS = {
    30: "-11-1",
    6: "01-1",
    66: "11-1",
    22: "110",
    154: "111",
    14: "011",
    70: "-111",
    10: "-110",
    2: "010",
    15: "-10-1",
    3: "00-1",
    33: "10-1",
    11: "100",
    77: "101",
    7: "001",
    35: "-101",
    5: "-100",
    195: "-1-1-1",
    39: "0-1-1",
    429: "1-1-1",
    143: "1-10",
    1001: "1-11",
    91: "0-11",
    455: "-1-11",
    65: "-1-10",
    13: "0-10"
}

ROTATIONS = {
    "br": "N",
    "bw": "yyy",
    "bo": "yy",
    "by": "y",
    "gr": "xx",
    "gw": "yyyxx",
    "go": "xx",
    "gy": "yxx",
    "ob": "xxx",
    "ow": "xxxyyy",
    "og": "xxxyy",
    "oy": "xxxy",
    "rg": "x",
    "rw": "xyyy",
    "rb": "xzz",
    "ry": "xy",
    "yr": "zzz",
    "yb": "zzzyyy",
    "yo": "zzzyy",
    "yg": "zzzy",
    "wr": "z",
    "wg": "zyyy",
    "wo": "zyy",
    "wb": "zy"
}

CROSS_SEQUENCES = {
    0: {
        "regular": {
            0: "7",
            2: "afgo",
            4: "fgo",
            6: "lfgeo",
            17: "oaaffgo",
            19: "aafgo",
            21: "faao",
            23: "efaalo"
        },
        "flip": {
            0: "faogfao"
        }
    },
    1: {
        "regular": {
            1: "7",
            3: "afgogjac",
            11: "aafgogjac",
            13: "fgogjac",
            20: "gfgogjac"
        },
        "flip": {
            1: "afgogjacgfgogjac"

        }
    },
    5: {
        "regular": {
            1: "7",
            5: "7",
            22: "7",
            18: "7",
            3: "aacgjglae",
            11: "gcgjglae",
            13: "acgjglae",
            20: "cgjglae",
        },
        "flip": {
            5: "acgjglaegcgjglae"
        }
    },
    6: {
        "regular": {
            0: "7",
            2: "lae",
            4: "glae",
            6: "7",
            17: "daklae",
            19: "laae",
            21: "alaae",
            23: "kaadlae"
        },
        "flip": {
            6: "lgealgea",
        }
    },
    7: {
        "regular": {
            1: "c",
            3: "cc",
            5: "j",
            7: "7",
            9: "fc",
            11: "oc",
            13: "ej",
            15: "b",
            18: "ffc",
            20: "aacc",
            22: "eej",
            24: "bb"
        },
        "flip": {
            7: "ceb",
        }
    },
    9: {
        "regular": {
            1: "o",
            3: "gff",
            5: "laaff",
            7: "7",
            9: "7",
            11: "ff",
            13: "aaff",
            15: "eeaaff",
            18: "f",
            20: "aff",
            22: "ddf",
            24: "df"
        },
        "flip": {
            9: "fhcb",
        }
    },
    15: {
        "regular": {
            1: "ccecc",
            3: "aee",
            5: "e",
            7: "7",
            9: "7",
            11: "aaee",
            13: "ee",
            15: "7",
            18: "ddl",
            20: "dl",
            22: "l",
            24: "kl"
        },
        "flip": {
            15: "ehdb",
        }
    },
    17: {
        "regular": {
            0: "7",
            2: "aoaaf",
            4: "oaaf",
            6: "7",
            19: "ogf",
            21: "oaf",
            23: "eoalf"
        },
        "flip": {
            17: "ogfaogf"
        }
    },
    18: {
        "regular": {
            3: "dgkgoaf",
            11: "adgkgoaf",
            13: "gdgkgoaf",
            20: "aadgkgoaf",
        },
        "flip": {
            18: "adgkgoafgdgkgoaf"
        }
    },
    22: {
        "regular": {
            11: "eglgkad",
            13: "aaeglgkad",
            20: "aeglgkad",
            3: "geglgkad",
        },
        "flip": {
            22: "aeglgkadgeglgkad"
        }
    },
    24: {
        "regular": {
            1: "faoaadd",
            3: "aadd",
            5: "eedee",
            7: "7",
            9: "7",
            11: "gdd",
            13: "add",
            15: "7",
            18: "k",
            20: "dd",
            22: "d",
            24: "7"
        },
        "flip": {
            24: "dhfb",
        }
    },
    23: {
        "regular": {
            0: "7",
            2: "eaal",
            4: "geaal",
            6: "7",
            17: "oaafgeaal",
            19: "egl",
            21: "aegl",
            23: "7"
        },
        "flip": {
            23: "ealgeal"
        }
    },
    666: {
        "ur": {
            0: "fadgko"
        },
        "lr": {
            0: "cafgoj"
        },
        "ll": {
            0: "eacgjl"
        },
        "ul": {
            0: "daeglk"
        },
        "dot": {
            0: "cfaogj"
        },
        "lv": {
            # 0: "430kgl"
            # 0: "o120jgh"
            0: "adealgk"
        },
        "lh": {
            # 0: "340lgk"
            0: "dealgk"
        }
    },
    777: {
        "GBRO": { # Rotate blue to Red position then swap Blue and Red
            0: "aa"
        },
        "GRBO": { # Fine, just rotate twice
            0: "aa"
        },
        "RGOB": { # Swap Upper Left
            0: "dakadaaka"
        },
        "GROB": { # Rotate once, swap Upper Right
            0: "afaoafaaoa"
        },
        "OGRB": { # Rotate once
            0: "a"
        },
        "GORB": { # Rotate once, swap Lower Right
            0: "acajacaaja"
        },
        "ROGB": { # Swap Upper Left
            0: "dakadaaka"
        },
        "ORGB": { # Swap Lower Right
            # 0: "50o05aao0"
            0: "cajacaaja"
        },
        "ORBG": { # Swap Upper Left
            0: "dakadaaka"
            # 0: "20j02aaj0"
        },
        "ROBG": { # Rotate thrice and swap Upper Right
            0: "gfaoafaaoa"
        },
        "BORG": { # Swap Lower Left
            0: "ealaeaala"
        },
        "OBRG": { # Rotate twice, swap Upper Left
            0: "aadakadaaka"
        },
        "RBOG": { # Fine, just rotate thrice
            0: "g"
        },
        "BROG": { # Rotate thrice, swap Upper Left
            0: "gdakadaaka"
        },
        "BGOR": { # Swap Lower Right
            0: "cajacaaja"
        },
        "GBOR": { # Rotate thrice, swap Lower Left
            0: "gealaeaala"
        },
        "OBGR": { # Swap Upper Right
            0: "faoafaaoa"
        },
        "BOGR": { # Fine
            0: "7"
        },
        "GOBR": { # Rotate once, swap Lower Right
            0: "acajacaaja"
        },
        "OGBR": { # Rotate once, swap Upper Left
            0: "adakadaaka"
        },
        "RGBO": { # Swap Upper Right
            0: "faoafaaoa"
        },
        "BRGO": { # Rotate thrice, swap Upper Left
            0: "gdakadaaka"
        },
        "RBGO": { # Rotate thrice, swap Lower Right
            0: "gcajacaaja"
        },
        "BGRO": { # Rotate once, swap Upper Right
            0: "afaoafaaoa"
        }
    },
    888: {
        0: {
            0: "afglaoge"
        },
        1: {
            0: "acgkajgd"
        },
        2: {
            0: "adgjakgc"
        },
        3: {
            0: "aegoalgf"
        },
        4: {
            0: "afglaoge"
        }
    },
    999: {
        0: {
            0: "ohfbohfb"
        },
        1: {
            0: "gohfbohfb"
        },
        2: {
            0: "aohfbohfb"
        },
        3: {
            0: "aaohfbohfb",
        },
        "last_layer": {
            0: "aa",
            1: "g",
            2: "a",
            3: "7"
        }
    }
}

EDGE_INDICES = [
    1,3,5,7,9,11,13,15,18,20,22,24
]

EDGE_VALIDATION_POSITIONS = [
    "-11.50","11.50","01-1.5","0-1-1.5","10-1.5","-10-1.5",
    "1-1.50","-1-1.50","101.5","-101.5","011.5","0-11.5"
]

CORNER_INDICES = [
    0,2,4,6,17,19,21,23
]

YELLOW_CORNER_POSITIONS = [
    "11-1","111","1-1-1","1-11"
]

CORNER_ORIENTATIONS_COUNTERCLOCKWISEUP = {
    "top": [2,6],
    "bottom": [19,23]
}

CORNER_ORIENTATIONS_CLOCKWISEUP = {
    "top": [0,4],
    "bottom": [17,21]
}

