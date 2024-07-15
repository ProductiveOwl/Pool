#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "phylib.h"

phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ) {
  phylib_object * stillBall = malloc(sizeof(phylib_object));
  if (stillBall == NULL) {
    return NULL;
  }

  stillBall->type = PHYLIB_STILL_BALL;
  stillBall->obj.still_ball.number = number;
  stillBall->obj.still_ball.pos = *pos;

  return stillBall;
}

phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc) {
  phylib_object * rollBall = malloc(sizeof(phylib_object));
  if (rollBall == NULL) {
    return NULL;
  }

  rollBall->type = PHYLIB_ROLLING_BALL;
  rollBall->obj.rolling_ball.number = number;
  rollBall->obj.rolling_ball.pos = *pos;
  rollBall->obj.rolling_ball.vel = *vel;
  rollBall->obj.rolling_ball.acc = *acc;

  return rollBall;
}

phylib_object *phylib_new_hole( phylib_coord *pos ) {
  phylib_object * newHole = malloc(sizeof(phylib_object));
  if (newHole == NULL) {
    return NULL;
  }

  newHole->type = PHYLIB_HOLE;
  newHole->obj.hole.pos = *pos;

  return newHole;
}

phylib_object *phylib_new_hcushion( double y ) {
  phylib_object * hcushion = malloc(sizeof(phylib_object));
  if (hcushion == NULL) {
    return NULL;
  }

  hcushion->type = PHYLIB_HCUSHION;
  hcushion->obj.hcushion.y = y;

  return hcushion;
}

phylib_object *phylib_new_vcushion( double x ) {
  phylib_object * vcushion = malloc(sizeof(phylib_object));
  if (vcushion == NULL) {
    return NULL;
  }

  vcushion->type = PHYLIB_VCUSHION;
  vcushion->obj.vcushion.x = x;

  return vcushion;
}

phylib_table *phylib_new_table( void ) {
  phylib_table * newTable = malloc(sizeof(phylib_table));
  phylib_coord hPos;

  if (newTable == NULL) {
    return NULL;
  }
  newTable->time = 0.0;

  //initialize every object here
  for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
    newTable->object[i] = NULL;
  }

  newTable->object[0] = phylib_new_hcushion(0.0);
  newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
  newTable->object[2] = phylib_new_vcushion(0.0);
  newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

  int index = 4;
  hPos.x = 0.0;

  //Create all of the holes with x position 0.0
  for (int i = 0; i < 3; i++) {
    hPos.y = (i/2.0)*PHYLIB_TABLE_LENGTH;
    newTable->object[index] = phylib_new_hole(&hPos);
    index++;
  }

  //Create all of the holes with x position of table_width
  hPos.x = PHYLIB_TABLE_WIDTH;
  for (int i = 0; i < 3; i++) {
    hPos.y = (i/2.0)*PHYLIB_TABLE_LENGTH;
    newTable->object[index] = phylib_new_hole(&hPos);
    index++;
  }

  return newTable;
}

void phylib_copy_object( phylib_object **dest, phylib_object **src ) {
  *dest = malloc(sizeof(phylib_object));
  if (*dest == NULL || *src == NULL) {
    free(*dest);
    *dest = NULL;
  }
  memcpy(*dest, *src, sizeof(phylib_object));
}

phylib_table *phylib_copy_table( phylib_table *table ) {
  phylib_table * newTable = malloc(sizeof(phylib_table));
  if (newTable == NULL) {
    return NULL;
  }

  for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
    //newTable->object[i] = malloc(sizeof(phylib_object)); //allocate space 
    if (table->object[i] != NULL) { //if there is an object, copy it
      phylib_copy_object(&(newTable->object[i]), &(table->object[i]));
    } else { //otherwise, free the space and set it to null
        //free(newTable->object[i]);
        newTable->object[i] = NULL;
    }
  }

  newTable->time = table->time;

  return newTable;
}

void phylib_add_object( phylib_table *table, phylib_object *object) {
  for (int index = 0; index < PHYLIB_MAX_OBJECTS; index++) {
    if (table->object[index] == NULL) {
      table->object[index] = object;
      break;
    }
  }
}

void phylib_free_table( phylib_table *table ) {
  for (int index = 0; index < PHYLIB_MAX_OBJECTS; index++) {
      free(table->object[index]);
      table->object[index] = NULL;
  }
  //free(table->object);
  free(table);
  table = NULL;
}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ) {
  phylib_coord newCord;
  newCord.x = c1.x - c2.x;
  newCord.y = c1.y - c2.y;
  return newCord;
}

double phylib_length( phylib_coord c ) {
  double cSquared = (c.x * c.x) + (c.y * c.y);
  return sqrt(cSquared);
}

double phylib_dot_product( phylib_coord a, phylib_coord b ) {
  return (a.x * b.x) + (a.y * b.y);
}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ) {
  phylib_coord distance; 
  double cushionDist = 0.0;

  if (obj1->type != PHYLIB_ROLLING_BALL) {
    return -1.0;
  }

  if (obj2->type == PHYLIB_STILL_BALL) {
    distance = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);
    return phylib_length(distance) - PHYLIB_BALL_DIAMETER;

  } else if (obj2->type == PHYLIB_ROLLING_BALL) {
    distance = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
    return phylib_length(distance) - PHYLIB_BALL_DIAMETER;

  } else if (obj2->type == PHYLIB_HOLE) {
    distance = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);
    return phylib_length(distance) - PHYLIB_HOLE_RADIUS;

  } else if (obj2->type == PHYLIB_HCUSHION) {
    cushionDist = obj2->obj.hcushion.y - obj1->obj.rolling_ball.pos.y;
    if (cushionDist < 0) {
      cushionDist *= -1;
    }
    cushionDist -= PHYLIB_BALL_RADIUS;
    return cushionDist;

  } else if (obj2->type == PHYLIB_VCUSHION) {
    cushionDist = obj2->obj.vcushion.x - obj1->obj.rolling_ball.pos.x;
    if (cushionDist < 0) {
      cushionDist *= -1;
    }
    cushionDist -= PHYLIB_BALL_RADIUS;
    return cushionDist;
  }
  return -1.0;
}

//Part 3
void phylib_roll( phylib_object *new, phylib_object *old, double time ) {
  if (old->type == PHYLIB_ROLLING_BALL && new->type == PHYLIB_ROLLING_BALL) {
    //Position
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x*time + 0.5*old->obj.rolling_ball.acc.x*time*time;
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y*time + 0.5*old->obj.rolling_ball.acc.y*time*time;

    //Velocity
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;

    //If the signs for velocity switch, set velocity and acc to 0
    if ((new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0) { 
      new->obj.rolling_ball.vel.y = 0;
      new->obj.rolling_ball.acc.y = 0;
    }
    if ((new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0) {
      new->obj.rolling_ball.vel.x = 0;
      new->obj.rolling_ball.acc.x = 0;
    }
  }
}

void changeToStillBall (phylib_object * object) {
  phylib_coord pos = object->obj.rolling_ball.pos;
  unsigned char number = object->obj.rolling_ball.number;

  object->type = PHYLIB_STILL_BALL;
  object->obj.still_ball.pos = pos;
  object->obj.still_ball.number = number;
}

void changeToRollingBall (phylib_object ** object) {
  phylib_coord pos = (*object)->obj.still_ball.pos;
  unsigned char number = (*object)->obj.still_ball.number;

  (*object)->type = PHYLIB_ROLLING_BALL;
  (*object)->obj.rolling_ball.number = number;
  (*object)->obj.rolling_ball.pos = pos;
  (*object)->obj.rolling_ball.vel.x = 0.0;
  (*object)->obj.rolling_ball.vel.y = 0.0;
  (*object)->obj.rolling_ball.acc.x = 0.0;
  (*object)->obj.rolling_ball.acc.y = 0.0;
}

unsigned char phylib_stopped( phylib_object *object ) {
  double velocity = 0.0;

  velocity = phylib_length(object->obj.rolling_ball.vel);
  if (velocity < PHYLIB_VEL_EPSILON) {
    changeToStillBall(object);
    return 1;
  }
  return 0;
}

void rollingBallHelp(phylib_object **a, phylib_object **b) {
  phylib_coord r_ab;
  phylib_coord v_rel;
  phylib_coord n;
  double v_rel_n = 0.0;
  double aLenVel = 0.0;
  double bLenVel = 0.0;

  r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
  v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
  n.x = r_ab.x / phylib_length(r_ab);
  n.y = r_ab.y / phylib_length(r_ab);
  v_rel_n = phylib_dot_product(v_rel, n);

  //Velocity
  (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x - (v_rel_n * n.x);
  (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y - (v_rel_n * n.y);

  (*b)->obj.rolling_ball.vel.x += (v_rel_n * n.x);
  (*b)->obj.rolling_ball.vel.y += (v_rel_n * n.y);

  //Acceleration
  aLenVel = phylib_length((*a)->obj.rolling_ball.vel);
  if (aLenVel > PHYLIB_VEL_EPSILON) {
    (*a)->obj.rolling_ball.acc.y = ((-1.0*(*a)->obj.rolling_ball.vel.y) / aLenVel) * PHYLIB_DRAG;
    (*a)->obj.rolling_ball.acc.x = ((-1.0*(*a)->obj.rolling_ball.vel.x) / aLenVel) * PHYLIB_DRAG;
  }

  bLenVel = phylib_length((*b)->obj.rolling_ball.vel);
  if (bLenVel > PHYLIB_VEL_EPSILON) {
    (*b)->obj.rolling_ball.acc.y = ((-1.0*(*b)->obj.rolling_ball.vel.y) / bLenVel) * PHYLIB_DRAG;
    (*b)->obj.rolling_ball.acc.x = ((-1.0*(*b)->obj.rolling_ball.vel.x) / bLenVel) * PHYLIB_DRAG;
  }
}

void phylib_bounce( phylib_object **a, phylib_object **b ) {
  switch ((*b)->type) {
    case PHYLIB_HCUSHION:
      (*a)->obj.rolling_ball.vel.y *= -1;
      (*a)->obj.rolling_ball.acc.y *= -1;
      break;
    case PHYLIB_VCUSHION:
      (*a)->obj.rolling_ball.vel.x *= -1;
      (*a)->obj.rolling_ball.acc.x *= -1;
      break;
    case PHYLIB_HOLE:
      free((*a));
      *a = NULL;
      break;
    case PHYLIB_STILL_BALL:
      changeToRollingBall(b);
    case PHYLIB_ROLLING_BALL:
      rollingBallHelp(a, b);
      break;
  }
}

unsigned char phylib_rolling( phylib_table *t ) {
  int numB = 0;
  for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
    if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
      numB += 1;
    }
  }

  return (unsigned char)numB;
}

int checkDistance(phylib_table * table, int indexOfObject) {
  double dist = 5;
  for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
    if (table->object[i] == NULL || i == indexOfObject) { //If the object is null or the object itself, skip it
      continue;
    } else {
      dist = phylib_distance(table->object[indexOfObject], table->object[i]);
      if (dist < 0.0) { //If distance is negative, the object has touched the object
        phylib_bounce(&(table->object[indexOfObject]), &(table->object[i]));
        return 1;
      }
    }
  }
  return 0;
}

phylib_table *phylib_segment( phylib_table *table ) {
  phylib_table * newTable = phylib_copy_table(table);

  int numRolling = phylib_rolling(table); //find the number of rolling balls
  int rollingBalls[numRolling]; //create an array to store the index of rolling balls
  int index = 0; //keeps track of the index for the rollingBalls array

  double timePassed = PHYLIB_SIM_RATE;
  int dist = 0;

  if (numRolling == 0) {
    phylib_free_table(newTable); //Free the table we copied as there weren't any rolling balls
    return NULL;
  }

  //Calculate the number of rolling balls and add their index number to the array
  for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
    if (table->object[i] != NULL && table->object[i]->type == PHYLIB_ROLLING_BALL) {
      rollingBalls[index] = i;
      index++;
    }
  }
  
  while (timePassed < PHYLIB_MAX_TIME) {
    for (int i = 0; i < numRolling; i++) { //This loop rolls all the rolling balls by timePassed
      phylib_roll(newTable->object[rollingBalls[i]], table->object[rollingBalls[i]], timePassed);
    }
    for (int i = 0; i < numRolling; i++) { //This loop is to check if any of the balls stopped or bounced
      if (phylib_stopped(newTable->object[rollingBalls[i]])) { //Check if the rolling ball has stopped
        dist = 1;
        break;
      }
      dist = checkDistance(newTable, rollingBalls[i]); //checks if the ball has bounced against anything else
      if (dist == 1) {
        break;
      }
    }
    if (dist == 1) {
      break;
    }
    timePassed += PHYLIB_SIM_RATE;
  }

  newTable->time = table->time + timePassed;
  return newTable;
}

//A2
char *phylib_object_string( phylib_object *object ) {
  static char string[80];
  if (object==NULL) {
    snprintf( string, 80, "NULL;" );
    return string;
  }
  switch (object->type) {
    case PHYLIB_STILL_BALL:
      snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
      break;
    case PHYLIB_ROLLING_BALL:
      snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
        break;
    case PHYLIB_HOLE:
      snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
        break;
    case PHYLIB_HCUSHION:
      snprintf( string, 80,
        "HCUSHION (%6.1lf)",
        object->obj.hcushion.y );
         break;
    case PHYLIB_VCUSHION:
      snprintf( string, 80,
        "VCUSHION (%6.1lf)",
        object->obj.vcushion.x );
        break;
  }
  return string;
}
