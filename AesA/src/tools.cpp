//
// Created by leone on 2020/4/27.
//
#include "AesA/tools.h"

void showWorkDir() {
    int MAX_PATH = 100;
    char buffer[MAX_PATH];
    getcwd(buffer, MAX_PATH);
    printf("WorkDir: %s\n", buffer);
}

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