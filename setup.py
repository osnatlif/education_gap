# to build the cython extensions use: python setup.py build_ext --inplace
from setuptools import setup, Extension
from Cython.Build import cythonize

from Cython.Compiler import Options
Options.buffer_max_dims = 18

extensions = [
        Extension("calculate_wage", ["calculate_wage.pyx"]),
        Extension("input.parameters170white", ["input/parameters1970white.pyx"]),
        Extension("constant_parameters", ["constant_parameters.pyx"]),
        Extension("draw_husband", ["draw_husband.pyx"]),
        Extension("draw_wife", ["draw_wife.pyx"]),
        Extension("gross_to_net", ["gross_to_net.pyx"]),
        Extension("value_to_index", ["value_to_index.pyx"]),
        Extension("calculate_utility_single_women", ["calculate_utility_single_women.pyx"]),
        Extension("calculate_utility_single_man", ["calculate_utility_single_man.pyx"]),
        Extension("calculate_utility_married", ["calculate_utility_married.pyx"]),
        Extension("update_wife_husband_objects", ["update_wife_husband_objects.pyx"]),
        Extension("calculate_emax", ["calculate_emax.pyx"]),
        Extension("single_men", ["single_men.pyx"]),
        Extension("single_women", ["single_women.pyx"]),
        Extension("math_perf", ["math_perf.pyx"]),
        Extension("randn", ["randn.c"]),
        Extension("married_couple_emax", ["married_couple_emax.pyx"])
]
setup(ext_modules=cythonize(extensions, language_level="3", gdb_debug=True))
