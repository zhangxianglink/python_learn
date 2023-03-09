# -*- coding: utf-8 -*-
def _def_params(p1, p2):
    print(f"you have {p1} apple")
    print(f"you have {p2} pen")


_def_params(20.30, "90")
_def_params(1 + 1, 2 + 2)
i = 1
_def_params(i + 2, i + 1)
_def_params(input("p1: "),input("p2: "))
