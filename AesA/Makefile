INCLUDE_PATHS := -Iinclude -I../arachne-all/Arachne/include -I../arachne-all/CoreArbiter/include -I../arachne-all/PerfUtils/include
LIBRARY_PATHS := -L../arachne-all/Arachne/lib -L../arachne-all/CoreArbiter/lib -L../arachne-all/PerfUtils/lib/
LIBRARY_NAMES := -lArachne -lCoreArbiter -lPerfUtils -lpcrecpp -pthread
CXX_FILES := src/AesA.cpp src/tools.cpp

LINK_FLAGS := $(LIBRARY_PATHS) $(LIBRARY_NAMES)
CXX_FLAGS := $(INCLUDE_PATHS) -std=c++11

ifeq ($(AES_MT_MODE), ArachneEnable)
	CXX_FLAGS += -DArachneEnable
else ifeq ($(AES_MT_MODE), PthreadSiblingCore)
	    CXX_FLAGS += -DPthreadSiblingCore
else
endif

.PHONY: all
all: AesATest

AesATest:
	@g++ $(CXX_FILES) $(LINK_FLAGS) $(CXX_FLAGS) -o ./bin/$@
# 	@echo $(CXX_FLAGS)
