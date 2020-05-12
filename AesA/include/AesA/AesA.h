// Author: Liheng Chen
// Organization: ISCAS, China

#ifndef _AES_H
#define _AES_H

#include <cstring>
#include <cerrno>
#include <pthread.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <cstdio>
#include <cstdlib>
#include <unistd.h>
#include <string>
#include <fstream>
#include <numeric>
#include <ctime>
#include <set>

#ifndef uint8
#define uint8  unsigned char
#endif

#ifndef uint32
#define uint32 unsigned long int
#endif


typedef struct AesContext {
    uint32 erk[64];     /* encryption round keys */
    uint32 drk[64];     /* decryption round keys */
    int nr;             /* number of rounds */
} AesContext_t;

struct ThreadTaskInfo {
    double taskDuration;
    pid_t taskTID;
    unsigned char *inBuffer;
    unsigned char *outBuffer;
    size_t start;
    size_t size;
    AesContext_t *pAesContext;
    bool EncryptFlag;
};

#ifdef __cplusplus
extern "C" {
#endif

double encryptFile(unsigned char *key, const char *ciphertextFilepath, const char *plaintextFilepath);

double decryptFile(unsigned char *key, const char *plaintextFilepath, const char *ciphertextFilepath);

#ifdef __cplusplus
}
#endif

#endif /* aes.h */