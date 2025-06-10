#define STEP_X 2
#define DIR_X  5
#define X_PER_STEP 1
#define PLUS_X 1
#define MINUS_X 0

#define STEP_Y 3
#define DIR_Y  6
#define Y_PER_STEP 1
#define PLUS_Y 0
#define MINUS_Y 1

#define T_INIT 1000 // ms
#define T_STEP 1000 // us
#define T_DIR 1000 // ms

#define LS_X 9
#define LS_Y 10

#define LASER 11

float STATE[2];

void setup() {
  Serial.begin(115200);
  pinMode(STEP_X, OUTPUT);
  pinMode(STEP_Y, OUTPUT);
  pinMode(DIR_X, OUTPUT);
  pinMode(DIR_Y, OUTPUT);
  pinMode(LS_X, INPUT_PULLUP);
  pinMode(LS_Y, INPUT_PULLUP);
  pinMode(LASER, OUTPUT);
  digitalWrite(STEP_X, 0);
  digitalWrite(STEP_Y, 0);
  digitalWrite(DIR_X, PLUS_X);
  digitalWrite(DIR_Y, PLUS_Y);
  attachInterrupt(digitalPinToInterrupt(LS_X), cb_ls_x, FALLING);
  attachInterrupt(digitalPinToInterrupt(LS_Y), cb_ls_y, FALLING);
  delay(T_INIT);
}

void loop() {
  digitalWrite(LASER, 1);
  delay(1000);

  // change_dir(DIR_X, PLUS_X);
  // for (int i=0; i<400; i++){
  //   step_pulse(STEP_X);
  //  }
  // change_dir(DIR_Y, PLUS_Y);
  // for (int i=0; i<400; i++){
  //   step_pulse(STEP_Y);
  // }
  // change_dir(DIR_X, MINUS_X);
  // for (int i=0; i<400; i++){
  //   step_pulse(STEP_X);
  //  }
  // change_dir(DIR_Y, MINUS_Y);
  // for (int i=0; i<400; i++){
  //   step_pulse(STEP_Y);
  // }

}



void step_pulse(int step_pin) {
  if ( step_pin == STEP_X )
    if ( digitalRead(DIR_X) == PLUS_X )
      STATE[0] += X_PER_STEP;
    else 
      STATE[0] -= X_PER_STEP;
  else if ( step_pin == STEP_Y )
    if ( digitalRead(DIR_Y) == PLUS_Y )
      STATE[1] += Y_PER_STEP;
    else
      STATE[1] -= Y_PER_STEP;
  digitalWrite(step_pin, 1);
  delayMicroseconds(T_STEP/2);
  digitalWrite(step_pin, 0);
  delayMicroseconds(T_STEP/2);
}

void change_dir(int dir_pin, bool dir_val) {
  if ( digitalRead(dir_pin) == dir_val)
    return; 
  if ( dir_pin == DIR_X & dir_val == PLUS_X)
    Serial.println("CHANGE DIR_X TO +");
  else if ( dir_pin == DIR_X & dir_val == MINUS_X)
    Serial.println("CHANGE DIR_X TO -");
  else if ( dir_pin == DIR_Y & dir_val == PLUS_Y)
    Serial.println("CHANGE DIR_Y TO +");
  else if ( dir_pin == DIR_Y & dir_val == MINUS_Y)
    Serial.println("CHANGE DIR_Y TO -");
  delay(T_DIR/2);
  digitalWrite(dir_pin, dir_val);
  delay(T_DIR/2);
}

void cb_ls_x(){
  Serial.println("LS X ACTIVADO");
}
void cb_ls_y(){
  Serial.println("LS Y ACTIVADO");
}