
BUILD    := build
LEXDIR   := src/lexicon
PYDIR    := src/parser
TESTDIR  := src/test

LEXFILES     := $(wildcard $(LEXDIR)/*.foma) $(wildcard $(LEXDIR)/*.lexc)
PYFILES      := $(wildcard $(PYDIR)/*.py)
PYBUILDFILES := $(addprefix $(BUILD)/,$(PYFILES:$(PYDIR)/%=%))


.PHONY: all setup lexicon python run test clean

all: setup lexicon python

setup:
	@mkdir -p $(BUILD)

lexicon: $(BUILD)/lexicon.fst

python: $(PYBUILDFILES)

run: $(PYBUILDFILES)
	cd $(BUILD); python

test: all $(PYTESTFILES)
	@#cd $(BUILD); python main.py
	cd $(BUILD); py.test

clean:
	rm -fr $(BUILD)


$(BUILD)/lexicon.fst: $(LEXDIR)/root.foma $(LEXFILES)
	cd $(LEXDIR); foma -f root.foma
	mv -f $(LEXDIR)/lexicon.fst $(BUILD)/lexicon.fst

$(BUILD)/%.py: $(PYDIR)/%.py
	cp -f $< $@

