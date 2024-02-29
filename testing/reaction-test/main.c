#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/time.h>

void openImage(char * img_pth) {
    #ifdef __linux__
        pid_t x = fork();
        if (x == 0) {
            char buf[256];
            snprintf(buf, sizeof(buf), "eog %s", img_pth);
            system(buf);

            exit(0);
        } else if (x < 0) {
            printf("failed to start child process\n");
        }
    #elif __APPLE__
        char buf[32];
        snprintf(buf, sizeof(buf), "open %s", img_pth);
        system(buf);
    #endif
}

void closeImage() {
    #ifdef __linux__
        system("pkill -x eog");
    #elif __APPLE__
        system("pkill -x Preview");
    #endif
}

int react(int image_n) {
    struct timeval tv;

    // begin timing
    gettimeofday(&tv,NULL);
    long long time_start = (((long long)tv.tv_sec)*1000)+(tv.tv_usec/1000);
    // display image
    printf("\nimage %d\n", image_n);
    // generate path to image
    char img_pth[32];
    snprintf(img_pth, sizeof(img_pth), "./images/light_%d.jpg", image_n);
    printf("path: %s\n", img_pth);

    // open image in a new window
    openImage(img_pth);

    // wait for interrupt
    getchar();

    // close image window
    closeImage();

    // end timing
    gettimeofday(&tv,NULL);
    long long time_end = (((long long)tv.tv_sec)*1000)+(tv.tv_usec/1000);

    int time_diff = time_end - time_start;

    return time_diff;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Please include a single argument containing the number of ");
        printf("tests to run\nE.g. ./reaction-test 4\n");
        exit(-1);
    }

    int test_n = atoi(argv[1]);
    printf("Testing with %d runs\n", test_n);
    sleep(1);
    printf("Start reaction test...\n");

    int times[test_n];

    for (int i = 0; i < test_n; i++) {
        sleep(1);
        times[i] = react(i);
        printf("Test %d took %d milliseconds\n", i, times[i]);
    }

    printf("Test complete\n");

    float avg_time = 0;
    for (int i = 0; i < test_n; i++) {
        avg_time += 1.0*times[i];
    }
    avg_time /= test_n;

    printf("Average reaction time: %.2f\n", avg_time);

    return 0;
}
