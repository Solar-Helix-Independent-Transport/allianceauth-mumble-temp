# Makefile for Alliance Auth Mumble Temp Links

# Variables
appname = allianceauth-mumbletemps
appname_verbose = Alliance Auth Mumble-Temps
package = mumbletemps

# Default goal
.DEFAULT_GOAL := help

# Help
help:
	@echo "$(appname_verbose) Makefile"
	@echo ""
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@echo "  translationfiles    Create or update translation files"
	@echo "  clean               Clean build environment"
	@echo "  build               Build PyPi Packages"
	@echo "  publish             Publish build files to PyPi"

# Translation files
translationfiles:
	@django-admin makemessages \
		-l cs \
		-l de \
		-l es \
		-l fr_FR \
		-l it_IT \
		-l ja \
		-l ko_KR \
		-l nl \
		-l pl_PL \
		-l ru \
		-l sk \
		-l uk \
		-l zh_Hans \
		--keep-pot \
		--ignore 'build/*'

# build package
build:
	pip install hatch
	hatch build

# publish package
publish:
	pip install twine
	twine upload dist/*

clean:
	rm -rf dist/
