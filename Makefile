
BUILD    := build
LEXDIR   := src/lexicon
PYDIR    := src/parser
TESTDIR  := src/test

LEXFILES     := $(wildcard $(LEXDIR)/*.foma) $(wildcard $(LEXDIR)/*.lexc)
PYFILES      := $(wildcard $(PYDIR)/*.py)
PYBUILDFILES := $(addprefix $(BUILD)/,$(PYFILES:$(PYDIR)/%=%))
FSTFILES     := $(BUILD)/lexicon.fst $(BUILD)/segmenter.fst $(BUILD)/allwords.fst


.PHONY: all setup lexicon python run test clean

all: setup lexicon python

setup:
	@mkdir -p $(BUILD)

lexicon: $(FSTFILES)

python: $(PYBUILDFILES)

run: $(PYBUILDFILES)
	cd $(BUILD); python3 -i -c 'from parser import *'

test: all $(PYTESTFILES)
	@#cd $(BUILD); python main.py
	cd $(BUILD); py.test

clean:
	rm -fr $(BUILD)

$(FSTFILES): $(LEXDIR)/root.foma.intermediate

.INTERMEDIATE: $(LEXDIR)/root.foma.intermediate

$(LEXDIR)/root.foma.intermediate: $(LEXDIR)/root.foma $(LEXFILES)
	cd $(LEXDIR); foma -f root.foma
	mv -f $(LEXDIR)/*.fst $(BUILD)/

$(BUILD)/%.py: $(PYDIR)/%.py
	cp -f $< $@

