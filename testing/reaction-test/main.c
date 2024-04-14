#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <sys/time.h>

#define KRED   "\x1B[31m"
#define KGREEN "\x1B[32m"
#define KCYAN  "\x1B[36m"
#define KWHITE "\x1B[37m"

// flag for pip between this program and detection software
volatile sig_atomic_t flag = 0;

/*
 * Sets flag to 1 when called
 */
void handler(int sig) {
    // signal received
    flag = 1;
}

/*
 * Given a path, opens an image in eog or Preview on Linux or macOS, respectively
 * Parameter - img_pth: relative path to image to be displayed
 */
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

/*
 * Closes a window of eog or Preview on Linux or macOS, respectively
 */
void closeImage() {
    #ifdef __linux__
        system("pkill -x eog");
    #elif __APPLE__
        system("pkill -x Preview");
    #endif
}

/*
 * Gets pid of another process
 */
int get_pid(const char* name) {
    char command[256];
    sprintf(command, "pgrep %s", name);

    FILE* fp = popen(command, "r");
    if (fp == NULL) {
        printf("Failed to run command\n");
        return -1;
    }

    int pid;
    if (fscanf(fp, "%d", &pid) != 1) {
        printf("Process not found\n");
        pid = -1;
    } else {
        printf("Found process with PID: %d\n", pid);
    }

    pclose(fp);
    return pid;
}

/*
 * Given a path, this function presents an image and measures the time that it
 * takes a secondary function to set the global variable `flag`. It then closes
 * the image.
 *
 * Parameter - img_pth: relative path to image to be displayed
 * Returns   - Reaction time in milliseconds
 */
int react(char * img_pth) {
    struct timeval tv;

    // begin timing
    gettimeofday(&tv,NULL);
    long long time_start = (((long long)tv.tv_sec)*1000)+(tv.tv_usec/1000);

    // open image in a new window
    openImage(img_pth);

    // wait for interrupt
    int wait = 1;
    while (wait) {
        if (flag) {
            wait = 0;
            flag = 0;
        }
    }

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
    // check that there aren't more tests requested than images available
    int test_n = atoi(argv[1]);
    if (test_n > 5) {
        printf("%s", KRED);
        printf("\nToo many tests, there aren't enough images\n");
        printf("%s", KWHITE);
        printf("The images directory only contains 5 images as of now\n\n");
        exit(-1);
    }

    // set up signal handler
    signal(SIGUSR1, handler);


    printf("\nProgram PID is: ");
    printf("%s", KGREEN);
    printf("%d\n\n", getpid());
    printf("%s", KCYAN);
    // printf("Provide the PID to the detection script as an argument\n");
    printf("Run test detection script; check that PID is the same\n");
    printf("%s", KWHITE);

    // await user input to begin test
    printf("Press ENTER/RETURN to begin the test...\n");
    getchar();

    printf("Testing with %d runs\n", test_n);
    sleep(1);
    printf("Start reaction test...\n");

    int times[test_n];

    // get pid of python program running yolo
    const char* name = "Python";
    int pid = get_pid(name);
    int running = (pid != -1);

    // run n tests, calling react() for each one
    for (int i = 0; i < test_n; i++) {
        printf("\nimage %d\n", i);
        // generate path to image
        char img_pth[32];
        snprintf(img_pth, sizeof(img_pth), "./images/light_%d.jpg", i);
        printf("path: %s\n", img_pth);

        // send a signal to the python program allowing it to continue
        sleep(3);
        if(pid >=0){
            kill(pid,SIGUSR2);
        }
        printf("pid: %d\n", pid);
        times[i] = react(img_pth);
        printf("Test %d took %d milliseconds\n", i, times[i]);
    }

    printf("Test complete\n");

    // calculate average reaction time
    float avg_time = 0;
    for (int i = 0; i < test_n; i++) {
        avg_time += 1.0*times[i];
    }
    avg_time /= test_n;

    printf("Average reaction time: %.2f\n", avg_time);

    return 0;
}
