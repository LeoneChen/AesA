//
// Created by leone on 2020/4/23.
//
#include <stdio.h>
#include <iostream>
#include <string>
#include <sys/stat.h>
#include <fstream>
#include <filesystem>
#include <unistd.h>
#include "Arachne/Arachne.h"
#include "AesA/AesA.h"
#include "Arachne/Logger.h"

#define BUFFER_LENGTH (1024 * 1024 * 8)
#define ArachneEnable

int CopyFile(std::string inPath, std::string outPath) {

    std::ifstream in(inPath, std::ios::binary);
    std::ofstream out(outPath, std::ios::binary);
    if (!in || !out) {
        printf("open file error");
        return -1;
    }
    out << in.rdbuf();
    in.close();
    out.close();
    return 0;
}

void showWorkDir() {
    int MAX_PATH = 100;
    char buffer[MAX_PATH];
    getcwd(buffer, MAX_PATH);
    printf("WorkDir: %s\n", buffer);
}


void encrypt(unsigned char *key, std::string plainPath, std::string cipherPath) {
    struct stat plainStat{};
    stat(plainPath.c_str(), &plainStat);
    printf("Encrypting file...\n"
           "Plaintext length: %ld\n", plainStat.st_size);

    auto plainTempPath = plainPath + "_temp";
    auto cipherTempPath = cipherPath + "_temp";

    CopyFile(plainPath, plainTempPath);

    if (plainStat.st_size % 16 != 0) {
        std::ofstream plainTempFile(plainTempPath, std::ios::app | std::ios::binary);
        plainTempFile << std::string(16 - (plainStat.st_size % 16), '\0');
        plainTempFile.close();
    }

    auto startTime = static_cast<double>(clock()) / CLOCKS_PER_SEC;
    encryptFile(key, plainTempPath.c_str(), cipherTempPath.c_str(), BUFFER_LENGTH);
    auto endTime = static_cast<double>(clock()) / CLOCKS_PER_SEC;
    auto duration = endTime - startTime;

    rename(cipherTempPath.c_str(), cipherPath.c_str());
    remove(plainTempPath.c_str());

    struct stat cipherStat{};
    stat(cipherPath.c_str(), &cipherStat);
    printf("Ciphertext length: %ld\n", cipherStat.st_size);
    printf("Time: %f, Speed: %f MB/s\n", (double) duration, (double) cipherStat.st_size / (1024 * 1024) / duration);
}

void decrypt(unsigned char *key, std::string cipherPath, std::string plainPath) {
    struct stat cipherStat{};
    stat(cipherPath.c_str(), &cipherStat);
    printf("Decrypting file...\n"
           "Ciphertext length: %ld\n", cipherStat.st_size);

    auto plainTempPath = plainPath + "_temp";

    auto startTime = static_cast<double>(clock()) / CLOCKS_PER_SEC;
    auto plainLen = decryptFile(
            key, cipherPath.c_str(), plainTempPath.c_str(), BUFFER_LENGTH);
    auto endTime = static_cast<double>(clock()) / CLOCKS_PER_SEC;
    auto duration = endTime - startTime;

//    FILE *plainTempFile = fopen(plainTempPath.c_str(), "rb");
//    fseek(plainTempFile, -16, SEEK_END);
//    char buffer[20];
//    fread(buffer, 16, 1, plainTempFile);
//    fclose(plainTempFile);
//
//    struct stat plainTempStat{};
//    stat(plainTempPath.c_str(), &plainTempStat);
//    truncate(plainTempPath.c_str(), plainTempStat.st_size - (16 - strlen(buffer)));

    rename(plainTempPath.c_str(), plainPath.c_str());

    struct stat plainStat{};
    stat(plainPath.c_str(), &plainStat);
    printf("Plaintext length: %ld\n", plainStat.st_size);
    printf("Time: %f, Speed: %f MB/s\n", (double) duration, (double) plainStat.st_size / (1024 * 1024) / duration);
}

void _encryptA(unsigned char *key, char **paths) {
    encryptFile(key, paths[0], paths[1], BUFFER_LENGTH);
    Arachne::shutDown();
}


extern "C" {
void encryptA(unsigned char *key, char *plainPath, char *cipherPath) {
//    showWorkDir();
//    chdir("/home/leone/文档/AESMultithread/AesA");
    char *paths[2] = {plainPath, cipherPath};
    Arachne::init(nullptr, nullptr);
    Arachne::createThread(&_encryptA, key, paths);
    Arachne::waitForTermination();
}
}

void _decryptA(unsigned char *key, char **paths) {
    decryptFile(key, paths[0], paths[1], BUFFER_LENGTH);
    Arachne::shutDown();
}


extern "C" {
void decryptA(unsigned char *key, char *cipherPath, char *plainPath) {
//    showWorkDir();
//    chdir("/home/leone/文档/AESMultithread/AesA");
    char *paths[2] = {cipherPath, plainPath};
    Arachne::init(nullptr, nullptr);
    Arachne::createThread(&_decryptA, key, paths);
    Arachne::waitForTermination();
}
}

void AppMain(int argc, const char **argv) {
    unsigned char key[] = "1111111111111111";
    encrypt(key, "data/vedio.mp4", "data/cipherFile");
//    decrypt(key, "data/cipherFile", "data/plainFile.mp4");
#ifdef ArachneEnable
    Arachne::shutDown();
#endif
}


int main(int argc, const char **argv) {
#ifdef ArachneEnable
    Arachne::Logger::setLogLevel(Arachne::WARNING);
    Arachne::init(&argc, argv);
    Arachne::createThread(&AppMain, argc, argv);
#else
    AppMain(argc, argv);
#endif

#ifdef ArachneEnable
    Arachne::waitForTermination();
#endif

}