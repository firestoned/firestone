CP := $(shell which cp)
DIRNAME := $(shell which dirname)
MKDIR := $(shell which mkdir)
RM := $(shell which RM)

CLIENT_OUTDIR := $(shell mktemp -d)
SERVER_CLIENT_OUTDIR := $(shell mktemp -d)
OPENAPI_GEN := $(shell which openapi-generator)
FIRESTONE := $(shell which firestone)

ADDRESSBOOK_DIR := examples/addressbook
RESOURCES := ${ADDRESSBOOK_DIR}/addressbook.yaml,${ADDRESSBOOK_DIR}/person.yaml,${ADDRESSBOOK_DIR}/postal_codes.yaml
OPENAPI_DOC := ${ADDRESSBOOK_DIR}/openapi.yaml

PKG := addressbook
CLIENT_PKG := addressbook.client
MAIN_FILE := ${ADDRESSBOOK_DIR}/main.py
STREAMLIT_FILE := ${ADDRESSBOOK_DIR}/addressbook/webui/pages.py

.PHONY: gen-openapi gen-server gen-client gen-cli

help:
	@echo "gen-openapi: Generate OpenAPI file from resources."
	@echo "gen-server: Generate FastAPI server code."
	@echo "gen-client: Generate Python client code."
	@echo "gen-cli: Generate CRUD Python (Click-based) CLI."

gen-openapi: ${FIRESTONE}
	${FIRESTONE} generate \
		--title 'Example person and addressbook API' \
		--description 'Example person and addressbook API' \
		--resources ${RESOURCES} \
		--version 1.0 \
		openapi \
		--version 3.1.0 \
		> ${OPENAPI_DOC}

gen-server: $(OPENAPI_GEN) \
			${OPENAPI_DOC}
	${OPENAPI_GEN} generate \
		-i ${OPENAPI_DOC} \
		-g python-fastapi \
		--package-name addressbook \
		-o ${SERVER_CLIENT_OUTDIR} \
		--skip-validate-spec \
		-c ${ADDRESSBOOK_DIR}/openapi-gen-server-config.json

	@echo "Copying model files from temp dir to project"
	${MKDIR} -pv ${ADDRESSBOOK_DIR}/addressbook/models
	${CP} -rv ${SERVER_CLIENT_OUTDIR}/src/addressbook/models/[a-z]* ${ADDRESSBOOK_DIR}/addressbook/models

	#${RM} -f ${ADDRESSBOOK_DIR}/addressbook/models/extra_models*

	@echo "Copying api files from temp dir to ${ADDRESSBOOK_DIR}"
	${MKDIR} -pv ${ADDRESSBOOK_DIR}/addressbook/apis
	${CP} -rv ${SERVER_CLIENT_OUTDIR}/src/addressbook/security_api.py ${ADDRESSBOOK_DIR}/addressbook
	${CP} -rv ${SERVER_CLIENT_OUTDIR}/src/addressbook/apis/* ${ADDRESSBOOK_DIR}/addressbook/apis

gen-client: $(OPENAPI_GEN) \
			${ADDRESSBOOK_DIR}/addressbook/apis
	${OPENAPI_GEN} generate \
		-i ${OPENAPI_DOC} \
		-g python \
		-o ${CLIENT_OUTDIR} \
		--skip-validate-spec \
		-c ${ADDRESSBOOK_DIR}/openapi-gen-config.json

	@echo "Copying client files from ${CLIENT_OUTDIR} to project"
	${CP} -rv ${CLIENT_OUTDIR}/addressbook/* ${ADDRESSBOOK_DIR}/addressbook

gen-cli: $(FIRESTONE)
	@echo "Creating directory for ${MAIN_FILE}"
	${MKDIR} -pv $(shell ${DIRNAME} ${MAIN_FILE})

	${FIRESTONE} generate \
		--title 'Addressbook CLI' \
		--description 'This is the CLI for the example Addressbook' \
		--resources ${RESOURCES} \
		--version 1.0 \
		 cli \
		 --pkg ${PKG} \
		 --client-pkg ${CLIENT_PKG} > ${MAIN_FILE}

	${FIRESTONE} generate \
		--title 'Addressbook CLI' \
		--description 'This is the CLI for the example Addressbook' \
		--resources ${RESOURCES} \
		--version 1.0 \
		 cli \
		 --pkg ${PKG} \
		 --client-pkg ${CLIENT_PKG} \
		 --output-dir ${ADDRESSBOOK_DIR}/addressbook/cli \
		 --as-modules

gen-streamlit: $(FIRESTONE)
	@echo "Creating directory for ${STREAMLIT_FILE}"
	${MKDIR} -pv $(shell ${DIRNAME} ${STREAMLIT_FILE})

	${FIRESTONE} generate \
		--title 'Addressbook CLI' \
		--description 'This is the streamlit module for the example Addressbook' \
		--resources ${RESOURCES} \
		--version 1.0 \
		 streamlit \
		 --as-modules \
		 --col-mappings '{"addressbook": ["addrtype", "street", "state", "country"]}' \
		 --backend-url "http://localhost:8080" \
		 --output-dir $(shell ${DIRNAME} ${STREAMLIT_FILE})
