.PHONY: prepare gccprep srpm prebuild

# Define variables
BUILDDIR := $(shell pwd)
SPECFILE := $(spec)

prepare:
	dnf install --nodocs -y rpm-build rpmdevtools

gccprep: prepare
	dnf install --nodocs -y gcc gcc-c++ make cmake ninja-build meson

prebuild:
	@buildtype="unknown"; \
	if grep -q "Name:.*scenefx\|Name:.*scrollfx\|Name:.*scroll\|Name:.*wayland\|Name:.*wlroots" "$(SPECFILE)"; then \
		buildtype="gcc"; \
	fi; \
	case $$buildtype in \
		"gcc") $(MAKE) -f $(lastword $(MAKEFILE_LIST)) gccprep;; \
		*) echo "Unknown package type in $(SPECFILE)"; exit 1;; \
	esac

srpm: prepare prebuild
	cd $(dir $(SPECFILE)) && spectool -g $(notdir $(SPECFILE))
	rpmbuild -bs \
		--define "_sourcedir $(dir $(SPECFILE))" \
		--define "_specdir $(dir $(SPECFILE))" \
		--define "_builddir $(BUILDDIR)" \
		--define "_srcrpmdir $(outdir)" \
		--define "_rpmdir $(BUILDDIR)" \
		--define "_buildrootdir $(BUILDDIR)/.build" \
		$(SPECFILE)

