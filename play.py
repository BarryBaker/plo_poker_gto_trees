import numpy as np
import pandas as pd

# print(np.any([[1, 0], [1, 0], [0, 1], [0, 0]], axis=0))

a = np.array(
    [
        [[1, 2], [1, 2], [1, 2]],
        [[1, 3], [1, 4], [1, 2]],
        [[1, 2], [1, 5], [1, 2]],
        [[1, 2], [1, 6], [2, 2]],
    ]
)
# print(np.any(a == 1, axis=(2)) & np.any(a == 2, axis=(2)))

print(
    pd.DataFrame(
        {
            "a": [
                False,
                False,
                False,
                False,
            ],
            "b": [
                False,
                False,
                False,
                False,
            ],
        }
    )
)
