.PHONY: all clean deps

all:
	python setup.py build_ext --inplace

deps:
	pip install -r requirements.txt

clean:
	python setup.py clean --all
	rm -rf *.c
	rm -rf *.so