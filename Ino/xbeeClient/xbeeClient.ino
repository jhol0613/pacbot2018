#include <SoftwareSerial.h>

struct game_state {
    int pac_x;
    int pac_y;

    int red_x;
    int red_y;
    int red_state; //0 = normal, 1 = frightened

    int pink_x;
    int pink_y;
    int pink_state; //0 = normal, 1 = frightened

    int orange_x;
    int orange_y;
    int orange_state; //0 = normal, 1 = frightened

    int blue_x;
    int blue_y;
    int blue_state; //0 = normal, 1 = frightened

    int score;
    int lives;
    int mode; //0 = running, 1 = paused
};

SoftwareSerial xbee(0, 1); // RX, TX
struct game_state state;

void setup() {
    Serial.begin(9600);
    // Set the data rate for the SoftwareSerial port.
    xbee.begin(9600);
}

int read_int() {
    char temp;
    String buf = "";
    while (1) {
        temp = xbee.read();
        if (temp == '#') {
            return buf.toInt();
        } else {
            buf += temp;
        }
    }
}

int read_ghost_state() {
    char temp = xbee.read();
    int ret = 0;
    if (temp == 'F') {
        ret = 1;
    }
    temp = xbee.read();
    return ret;
}

int read_state() {
    char temp;
    while (1) {
        temp = xbee.read();
        if (temp == '$')  break;
    }
    temp = xbee.read();
    if (temp == 'P') {
        state.mode = 1;
    } else {
        state.mode = 0;
    }
    temp = xbee.read();
    if (temp != '#')  return 1;
    state.score = read_int();
    state.lives = read_int();
    
    state.pac_x = read_int();
    state.pac_y = read_int();

    state.red_x = read_int();
    state.red_y = read_int();
    state.red_state = read_ghost_state();

    state.pink_x = read_int();
    state.pink_y = read_int();
    state.pink_state = read_ghost_state();

    state.orange_x = read_int();
    state.orange_y = read_int();
    state.orange_state = read_ghost_state(); 

    state.blue_x = read_int();
    state.blue_y = read_int();
    state.blue_state = read_ghost_state();
    return 0;
}

void print_state() {
    Serial.print("Mode: ");
    Serial.println(state.mode);
    Serial.print("Score: ");
    Serial.println(state.score);
    Serial.print("Lives: ");
    Serial.println(state.lives);
    Serial.print("pacman: (");
    Serial.print(state.pac_x);
    Serial.print(", ");
    Serial.print(state.pac_y);
    Serial.println(")");

    Serial.print("red: (");
    Serial.print(state.red_x);
    Serial.print(", ");
    Serial.print(state.red_y);
    Serial.println(")");
    
    Serial.print("pink: (");
    Serial.print(state.pink_x);
    Serial.print(", ");
    Serial.print(state.pink_y);
    Serial.println(")");

    Serial.print("orange: (");
    Serial.print(state.orange_x);
    Serial.print(", ");
    Serial.print(state.orange_y);
    Serial.println(")");

    Serial.print("blue: (");
    Serial.print(state.blue_x);
    Serial.print(", ");
    Serial.print(state.blue_y);
    Serial.println(")");
}

void loop()  {
    read_state();

    print_state();
    delay(500);
}
