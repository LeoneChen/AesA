//
// Created by leone on 2020/4/27.
//

#ifndef AESMULTITHREAD_TOOLS_H
#define AESMULTITHREAD_TOOLS_H

#include <stdio.h>
#include <string>
#include <fstream>
#include <unistd.h>

void showWorkDir();

int CopyFile(std::string inPath, std::string outPath);

#endif //AESMULTITHREAD_TOOLS_H
