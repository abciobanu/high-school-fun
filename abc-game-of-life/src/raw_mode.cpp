#include "../include/raw_mode.h"

#include <iostream>

#include <sys/ioctl.h>
#include <termios.h>

void enable_raw_mode()
{
    termios term; // use termios to turn off line buffering
    tcgetattr(0, &term);
    term.c_lflag &= ~(ICANON | ECHO); // disable echo as well
    tcsetattr(0, TCSANOW, &term);
}

void disable_raw_mode()
{
    termios term;
    tcgetattr(0, &term);
    term.c_lflag |= ICANON | ECHO;
    tcsetattr(0, TCSANOW, &term);
}

bool kbhit()
{ // Modified Morgan McGuire's Linux (POSIX) implementation of _kbhit(). (Morgan McGuire, morgan@cs.brown.edu)
    int byteswaiting;
    ioctl(0, FIONREAD, &byteswaiting);
    return byteswaiting > 0;
}
