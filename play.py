import numpy as np
import pandas as pd
import pickle
import glob
import os
from icecream import ic as qw
import json
from scipy.stats import pointbiserialr


a = {
    ("HRR", False): {
        ("2P", True): {
            ("LP", False): {("TP", False): {("SDBL", False): {}}, ("SDBL", False): {}},
            ("2PT", False): {("SDBL", False): {}},
            ("SDBL", False): {("TP", False): {}},
            ("TP", False): {},
        },
        ("WR", False): {("WR1", False): {("DSDBL", False): {}}, ("DSDBL", False): {}},
        ("BOP", False): {
            ("DSDBL", False): {
                ("TP", False): {("SD", False): {("OESD", False): {}, ("GS1", False): {}}, ("TRIPS", False): {}},
                ("OESD", False): {("MP", False): {}},
                ("GS1", False): {("MP", False): {}},
                ("MP", False): {("GS", False): {}, ("TRIPS", False): {}},
                ("GS", False): {},
            },
            ("GS", False): {
                ("TP", False): {("GS1", False): {}},
                ("GS1", False): {("MP", False): {}},
                ("LP", False): {},
            },
            ("TRIPS", False): {("TRIPS1", False): {}},
            ("TP", False): {("SDBL", False): {}},
            ("MP", False): {("SDBL", False): {}},
            ("SDBL", False): {},
        },
        ("LRR", False): {("SDBL", False): {("GS", False): {}}},
        ("GS1", False): {("DSDBL", False): {}},
        ("GS", False): {("DSDBL", False): {}},
        ("OESD", False): {("DSDBL", False): {}},
        ("DSDBL", False): {},
        ("SDBL", False): {},
    },
    ("2P", True): {
        ("LP", False): {
            ("MP", False): {
                ("SD", False): {("OESD", False): {}, ("GS1", False): {}},
                ("TP", False): {("2PT", False): {("SDBL", False): {}}, ("SDBL", False): {}},
                ("RR", False): {("SDBL", False): {}},
                ("SDBL", False): {},
            },
            ("GS1", False): {},
            ("RR", False): {("SDBL", False): {}},
            ("SDBL", False): {("GS", False): {}, ("OESD", False): {}},
        },
        ("2PT", False): {
            ("SD", False): {("OESD", False): {}, ("GS1", False): {}},
            ("SDBL", False): {("RR", False): {}},
            ("RR", False): {},
        },
        ("SD", False): {
            ("TP", False): {("GS1", False): {}, ("OESD", False): {}},
            ("OESD", False): {},
            ("GS1", False): {},
        },
        ("TP", False): {("DSDBL", False): {}, ("SDBL", False): {}, ("RR", False): {}},
        ("SDBL", False): {("RR", False): {}},
        ("RR", False): {},
    },
    ("TRIPS", True): {
        ("MP", False): {
            ("2PT", False): {
                ("TRIPS1", False): {("LP", False): {}, ("SDBL", False): {}},
                ("SDBL", False): {},
                ("LP", False): {},
            },
            ("TRIPS1", False): {("LP", False): {}, ("SDBL", False): {}},
            ("TP", False): {("LP", False): {}, ("SDBL", False): {}},
            ("RR", False): {},
            ("GS", False): {("GS1", False): {}},
            ("LP", False): {("SDBL", False): {}},
            ("SDBL", False): {("OESD", False): {}},
        },
        ("TRIPS1", False): {
            ("LP", False): {("SDBL", False): {}},
            ("SD", False): {("GS", False): {("GS1", False): {}}},
            ("RR", False): {("SDBL", False): {}},
            ("SDBL", False): {},
        },
        ("SDBL", False): {("TP", False): {}, ("SD", False): {("GS1", False): {}, ("OESD", False): {}}},
        ("TP", False): {},
    },
    ("WR", True): {
        ("WR1", False): {("BOP", False): {("LP", False): {}, ("TP", False): {}}, ("RR", False): {}},
        ("BOP", False): {("MP", False): {}, ("TP", False): {}},
        ("DSDBL", False): {},
        ("RR", False): {},
    },
    ("SD", False): {
        ("BOP", False): {
            ("MP", False): {
                ("OESD", True): {("RR", False): {}},
                ("GS1", False): {("RR", False): {}},
                ("RR", False): {("DSDBL", False): {}},
            },
            ("OESD", False): {("TP", False): {("RR", False): {}}, ("RR", False): {}},
            ("RR", True): {
                ("TP", False): {("DSDBL", False): {("GS1", False): {}}},
                ("DSDBL", False): {("GS1", False): {}},
            },
            ("TP", False): {("GS1", False): {}},
            ("GS1", False): {},
        },
        ("RR", False): {
            ("OESD", False): {("DSDBL", False): {}},
            ("GS1", False): {("DSDBL", False): {}},
            ("DSDBL", False): {},
        },
        ("OESD1", False): {},
        ("GS1", False): {("OP", False): {}},
        ("GS", False): {},
    },
    ("LP", False): {("SDBL", False): {("RR", False): {("DSDBL", False): {}}}, ("RR", False): {}, ("OP", False): {}},
    ("RR", False): {
        ("TP", False): {("DSDBL", False): {}, ("SDBL", False): {}},
        ("SDBL", False): {("DSDBL", False): {("MP", False): {}}, ("MP", False): {}},
        ("MP", False): {},
    },
    ("TP", False): {("SDBL", False): {}, ("OP", False): {}},
    ("SDBL", False): {("MP", False): {}, ("OP", False): {}},
    ("OP", False): {("MP", False): {}},
    ("MP", False): {},
}
