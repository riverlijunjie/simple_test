
#include <iostream>
#include <sys/mman.h>
#include <sys/stat.h>
#include <memory>
#include <fcntl.h>
#include <unistd.h>
#include <chrono>
#include <vector>
#include <cstring>

int mmap_test(std::string path) {
    int prot = PROT_READ;
    int mode = O_RDONLY;
    int handle = open(path.c_str(), mode);

    if(handle == -1) {
        std::cout << "Cannot open file: " << path.c_str() << std::endl;
        return -1;
    }

    struct stat sb = {};
    auto ret = fstat(handle, &sb);
    if(ret == -1 || sb.st_size <=0) {
        std::cout << "Cannot get file size: " << path.c_str() << std::endl;
        return -1;
    }

    void *buffer = mmap(nullptr, sb.st_size, prot, MAP_PRIVATE, handle, 0);
    if(!buffer){
        std::cout << "Mmap failed: " << path.c_str() << std::endl;
        return -1;
    }

    char* dst = new char[sb.st_size];

    std::cout << "mmap src = " << buffer << ", dst = " << (void *)dst << std::endl;
    auto _start = std::chrono::high_resolution_clock::now();
    
    std::memcpy(dst, buffer, sb.st_size);

    auto _end = std::chrono::high_resolution_clock::now();
    auto _duration = std::chrono::duration_cast<std::chrono::nanoseconds>(_end - _start).count() * 0.000001;
    std::cout << "mmap: copy " <<  sb.st_size/1024/1024 << "MB cost " << _duration << " ms";
    std::cout << ", band width = " << 1000 * sb.st_size/1024/1024 / _duration << "MB/s" << std::endl;

    delete dst;
    munmap(buffer, sb.st_size);
    close(handle);
    return 0;
}

int memcpy_test(size_t size)
{
    char* src = new char[size];
    char* dst = new char[size];

    std::cout << "src = " << (void *)src << ", dst = " << (void *)dst << std::endl;
    auto _start = std::chrono::high_resolution_clock::now();

    std::memcpy(dst, src, size);

    auto _end = std::chrono::high_resolution_clock::now();
    auto _duration = std::chrono::duration_cast<std::chrono::nanoseconds>(_end - _start).count() * 0.000001;
    std::cout << "buffer: copy " << size / 1024 / 1024 << "MB cost " << _duration << " ms";
    std::cout << ", band width = " << 1000 * size / 1024 / 1024 / _duration << "MB/s" << std::endl;

    delete dst;
    delete src;
    return 1;
}

int main(int argc, char** argv) {

    mmap_test(argv[1]);
    size_t size = 512*1024*1024;
    memcpy_test(size);

    return 1;
}

