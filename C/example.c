#include <stdio.h>
#include <stdlib.h>
#include "network.h"

state_response* latest_state;


int main(int argc, char **arg) {

    latest_state = malloc(sizeof(state_response));
    if(latest_state == NULL) {
        return -1;
    }

    // Wait until game starts
    while(getGameStatus() == P_STOPPED) {
        pollState();
    }

    // Game has started
    while(getGameStatus() != P_STOPPED) {
        pollState();

    }

    free(state_response);

}
