#ifndef _NETWORK_H_
#define _NETWORK_H_

#include <stdio.h> /* printf, sprintf */
#include <stdlib.h> /* exit */
#include <unistd.h> /* read, write, close */
#include <string.h> /* memcpy, memset */
#include <sys/socket.h> /* socket, connect */
#include <netinet/in.h> /* struct sockaddr_in, struct sockaddr */
#include <netdb.h> /* struct hostent, gethostbyname */

typedef enum {
    P_STOPPED,  /* Game is stopped */
    P_POWER,    /* Game is in power mode (a power pellet has been eaten */
    P_REGULAR   /* Game is going */
} game_status;

typedef struct cell_pos {
    int cp_x;   /* x coordinate */
    int cp_y;   /* y coordinate */
} cell_pos;

typedef struct state_response {
    game_status sr_state;   /* shows if the game is stopped, going or in power mode */
    cell_pos sr_pacbot;     /* Position of the Pacbot */
    cell_pos sr_inky;       /* Position of Inky */
    cell_pos sr_blinky;     /* Position of Blinky */
    cell_pos sr_pinky;      /* Position of Pinky */
    cell_pos sr_clyde;      /* Position of Clyde */
    int sr_power_counter;   /* Shows how long the power mode will be active */
} state_response;

cell_pos getPacbot();
cell_pos getClyde();
cell_pos getBlinky();
cell_pos getInky();
cell_pos getPinky();
game_status getGameStatus();
int getPowerCounter();

void pollState();
void printState();

extern state_response *latest_state;

#endif /* _NETWORK_H_*/
