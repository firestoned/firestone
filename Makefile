CP := $(shell which cp)
RM := $(shell which RM)
MKDIR := $(shell which mkdir)

CLIENT_OUTDIR := $(shell mktemp -d)
SERVER_CLIENT_OUTDIR := $(shell mktemp -d)
OPENAPI_GEN := $(shell which openapi-generator)
FIRESTONE := $(shell which firestone)

ADDRESSBOOK_DIR := examples/addressbook
RESOURCES := ${ADDRESSBOOK_DIR}/addressbook.yaml,${ADDRESSBOOK_DIR}/person.yaml
OPENAPI_DOC := ${ADDRESSBOOK_DIR}/openapi.yaml

.PHONY: gen-openapi openapi-generator

help:
	@echo "gen-openapi: Generate OpenAPI file from resources."
	@echo "gen-server: Generate FastAPI server code."

gen-openapi: ${FIRESTONE}
	${FIRESTONE} generate \
		--title 'Example person and addressbook API' \
		--description 'Example person and addressbook API' \
		--resources ${RESOURCES} \
		--version 1.0 \
		openapi \
		--security '{"name": "bearer_auth", "scheme": "bearer", "type": "http", "bearerFormat": "JWT"}' \
		> ${OPENAPI_DOC}

gen-server: $(OPENAPI_GEN)
	${OPENAPI_GEN} generate \
		-i ${OPENAPI_DOC} \
		-g python-fastapi \
		--package-name addressbook \
		-o ${SERVER_CLIENT_OUTDIR} \
		--skip-validate-spec

	@echo "Copying model files from temp dir to project"
	${MKDIR} -pv ${ADDRESSBOOK_DIR}/addressbook/models
	${CP} -rv ${SERVER_CLIENT_OUTDIR}/src/addressbook/models/[a-z]* ${ADDRESSBOOK_DIR}/addressbook/models

	${RM} -f ${ADDRESSBOOK_DIR}/addressbook/models/extra_models*

	@echo "Copying api files from temp dir to ${ADDRESSBOOK_DIR}"
	${MKDIR} -pv ${ADDRESSBOOK_DIR}/addressbook/apis
	${CP} -rv ${SERVER_CLIENT_OUTDIR}/src/addressbook/apis/* ${ADDRESSBOOK_DIR}/addressbook/apis

gen-client: $(OPENAPI_GEN)
	${OPENAPI_GEN} generate \
		-i ${OPENAPI_DOC} \
		-g python-nextgen \
		-o ${CLIENT_OUTDIR} \
		--skip-validate-spec \
		-c ${ADDRESSBOOK_DIR}/openapi-gen-config.json

	@echo "Copying client files from ${CLIENT_OUTDIR} to project"
	${CP} -rv ${CLIENT_OUTDIR}/addressbook/* ${ADDRESSBOOK_DIR}/addressbook
