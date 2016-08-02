PKG_SOURCE_URL:=${DL_MIRROR}/android/repository/${PKG_SOURCE}

DL_DIR=/var/cache/google-android-${PKG_NAME}-installer
INSTALL_DIR=/usr/lib/android-sdk/platforms
DOC_DIR=/usr/share/doc/google-android-${PKG_NAME}

all: $(UNPACK_DIR)/source.properties

install: all
	$(eval UNPACK_DIR=$(DL_DIR)/$(shell unzip -Z -1 $(DL_DIR)/$(PKG_SOURCE) | head -1))
	install -d -m0755 $(DOC_DIR)
	gzip -9 --stdout $(UNPACK_DIR)data/NOTICE.txt > $(DOC_DIR)/copyright.gz
	@if [ -f $(UNPACK_DIR)source.properties ]; then \
		install -m0644 $(UNPACK_DIR)source.properties $(DOC_DIR)/ ; \
        fi
	find ${DOC_DIR} | sort >> /var/lib/dpkg/info/google-android-${PKG_NAME}-installer.list
	install -d -m0755 $(INSTALL_DIR)
	@if [ ! -d $(INSTALL_DIR)/$(TRG_DIR) ]; then \
		mv $(UNPACK_DIR) $(INSTALL_DIR)/${TRG_DIR}  ;\
		find ${INSTALL_DIR}/${TRG_DIR}  | sort >> /var/lib/dpkg/info/google-android-${PKG_NAME}-installer.list ;\
	else\
		echo "\033[0;31m$(INSTALL_DIR)/${TRG_DIR} already exists.\033[0m" ; \
		exit 1 ; \
	fi

$(UNPACK_DIR)/source.properties: $(DL_DIR)/$(PKG_SOURCE)
	cd $(DL_DIR) && unzip -ou $(PKG_SOURCE)

$(DL_DIR)/$(PKG_SOURCE):
	cd $(DL_DIR) && \
		su nobody -s /bin/sh -c "wget --continue $(PKG_SOURCE_URL)"
	sha1sum -c $(PKG_SOURCE).sha1

clean:
	-rm -rf -- $(UNPACK_DIR)

distclean: clean
	-rm -rf -- $(DL_DIR)

.PHONY: install clean
