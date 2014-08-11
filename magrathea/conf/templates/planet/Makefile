# Magrathea Makefile

MAGRATHEA = {MAGRATHEA_EXECUTABLE}
BUILDDIR = {PLANET_BUILD_DIR}

# User-friendly check for magrathea
ifeq ($(shell which $(MAGRATHEA) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(MAGRATHEA)' command was not found. Make sure you have Magrathea installed, then set the MAGRATHEA environment variable to point to the full path of the '$(MAGRATHEA)' executable. Alternatively you can add the directory with the executable to your PATH.)
endif

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean       to clean up any previously built output"

clean:
    rm -rf $(BUILDDIR)/*


