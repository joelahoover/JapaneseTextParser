
BUILD    := build
LEXDIR   := src/lexicon
PYDIR    := src/parser
TESTDIR  := src/test

LEXFILES     := $(wildcard $(LEXDIR)/*.foma) $(wildcard $(LEXDIR)/*.lexc)
PYFILES      := $(wildcard $(PYDIR)/*.py)
PYBUILDFILES := $(addprefix $(BUILD)/,$(PYFILES:$(PYDIR)/%=%))


.PHONY: all setup lexicon python test clean

all: setup lexicon python

setup:
	@mkdir -p $(BUILD)

lexicon: $(BUILD)/lexicon.fst

python: $(PYBUILDFILES)

test: all $(PYTESTFILES)

clean:
	rm -fr $(BUILD)


$(BUILD)/lexicon.fst: $(LEXDIR)/root.foma $(LEXFILES)
	cd $(LEXDIR); foma -f root.foma
	mv -f $(LEXDIR)/lexicon.fst $(BUILD)/lexicon.fst

$(BUILD)/%.py: $(PYDIR)/%.py
	cp -f $< $@

