VENV_DIR?=.venv-metrics
VENV_ACTIVATE=$(VENV_DIR)/bin/activate
WITH_VENV=. $(VENV_ACTIVATE);

.PHONY: venv
venv: $(VENV_ACTIVATE)

$(VENV_ACTIVATE): requirements.txt
	test -f $@ || virtualenv --python=python3 $(VENV_DIR)
	$(WITH_VENV) pip install -r requirements.txt
	touch $@
