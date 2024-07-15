import phylib;
import os
import sqlite3

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;

# add more here
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER

HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH

SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON

DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME

MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg id="svgPoolTable" width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

#A3
FRAME_INTERVAL = 0.01

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        #None, None = vel, acc
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg (self):
        string = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" %(self.obj.still_ball.pos.x,self.obj.still_ball.pos.y,BALL_RADIUS,BALL_COLOURS[self.obj.still_ball.number],)
        return string

################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number, position (x,y), velocity (x,y) and acceleration (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;


    # add an svg method here
    def svg (self):
        string = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" %(self.obj.rolling_ball.pos.x,self.obj.rolling_ball.pos.y,BALL_RADIUS,BALL_COLOURS[self.obj.rolling_ball.number],)
        return string

################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole;


    # add an svg method here
    def svg (self):
        string = """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" %(self.obj.hole.pos.x,self.obj.hole.pos.y,HOLE_RADIUS,)
        return string
################################################################################
class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, yVal):
        """
        Constructor function. Requires a y value as an arguemnt
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, yVal );
      
        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion;

    # add an svg method here
    def svg (self):
        string = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" %(self.obj.hcushion.y,)
        return string
################################################################################
class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, xVal):
        """
        Constructor function. Requires a x value as an arguemnt
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       xVal, 0.0 );
      
        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion;


    # add an svg method here
    def svg (self):
        string = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" %(self.obj.vcushion.x,)
        return string
################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        string = HEADER
        for object in self:
            if object != None:
                string += object.svg()
        string += FOOTER
        return string
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                    Coordinate( ball.obj.still_ball.pos.x,
                                    ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;
    
class Database():
    def __init__(self, reset=False):
        if reset == True:
            if os.path.exists("phylib.db"):
                    os.remove("phylib.db")
        self.conn = sqlite3.connect( 'phylib.db' );
    
    def createDB(self):
        # create database file if it doesn't exist and connect to it
        conns = self.conn.cursor()
        conns.execute( """CREATE TABLE IF NOT EXISTS Ball ( 
             		BALLID   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             		BALLNO   INTEGER NOT NULL,
             		XPOS     FLOAT NOT NULL,
             		YPOS     FLOAT NOT NULL,
                    XVEL     FLOAT,
                    YVEL     FLOAT);""" );
        
        conns.execute( """CREATE TABLE IF NOT EXISTS TTable ( 
             		TABLEID   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             		TIME      FLOAT NOT NULL);""" );
        
        conns.execute( """CREATE TABLE IF NOT EXISTS BallTable ( 
             		BALLID   INTEGER NOT NULL,
             		TABLEID  INTEGER NOT NULL,
             		FOREIGN KEY (BALLID) REFERENCES Ball, 
                    FOREIGN KEY (TABLEID) REFERENCES TTable);""" );
        
        conns.execute( """CREATE TABLE IF NOT EXISTS Game ( 
             		GAMEID      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             		GAMENAME    VARCHAR(64) NOT NULL);""" );
        
        conns.execute( """CREATE TABLE IF NOT EXISTS Player ( 
             		PLAYERID      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             		GAMEID        INTEGER NOT NULL,
                    PLAYERNAME    VARCHAR(64) NOT NULL,
                    FOREIGN KEY (GAMEID) REFERENCES Game);""" );
    
        conns.execute( """CREATE TABLE IF NOT EXISTS Shot ( 
             		SHOTID    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             		PLAYERID  INTEGER NOT NULL,
                    GAMEID    INTEGER NOT NULL,
             		FOREIGN KEY (PLAYERID) REFERENCES Player, 
                    FOREIGN KEY (GAMEID) REFERENCES Game);""" );
    
        conns.execute( """CREATE TABLE IF NOT EXISTS TableShot ( 
             		TABLEID   INTEGER NOT NULL,
             		SHOTID    INTEGER NOT NULL,
             		FOREIGN KEY (SHOTID) REFERENCES Shot, 
                    FOREIGN KEY (TABLEID) REFERENCES TTable);""" );
        conns.close()
        self.conn.commit()


    def readTable(self, tableID):
        #print("Read")
        conns = self.conn.cursor()
        newTID = int(tableID) + 1

        table = Table()
        pos = Coordinate(0, 0)
        vel = Coordinate(0, 0)
        acc = Coordinate(0, 0)
        ballNum = 0

        ballIDs = (conns.execute("""SELECT BallTable.BALLID
                                    FROM BallTable
                                    WHERE BallTable.TABLEID==(?);""", (newTID,)).fetchall())
        #print(ballIDs)
        if len(ballIDs) == 0:
            return None

        aTime = (conns.execute("""SELECT TTABLE.TIME
                                    FROM TTABLE
                                    WHERE TTABLE.TABLEID==(?);""", (newTID,)).fetchall())
        
        table.time = aTime[0][0]
        #print(table.time)
        
        for ballID in ballIDs:
            theID = ballID[0]
            #print(theID)

            aBall = conns.execute("""SELECT *
                                    FROM Ball
                                    WHERE Ball.BALLID==(?);""", (theID,)).fetchall()
            
            #It is a StillBall
            if aBall[0][-1] == None:
                ballNum = aBall[0][1]
                pos.x = aBall[0][2]
                pos.y = aBall[0][3]
                sb = StillBall(ballNum, pos)
                table += sb

            #It is a RollingBall
            else:
                ballNum = aBall[0][1]
                pos.x = aBall[0][2]
                pos.y = aBall[0][3]
                vel.x = aBall[0][4]
                vel.y = aBall[0][5]
                aLenVel = phylib.phylib_length(vel)
                if aLenVel > VEL_EPSILON:
                    acc.y = ((-1.0*vel.y) / aLenVel) * DRAG
                    acc.x = ((-1.0*vel.x) / aLenVel) * DRAG
                rb = RollingBall(ballNum, pos, vel, acc)
                table += rb

        conns.close()
        self.conn.commit()
        return table

    
    def writeTable(self, table):
        #print("Write")
        conns = self.conn.cursor()
        ballIDs = []
    
        for item in table:
            if isinstance(item, RollingBall):
                conns.execute( """INSERT
                                INTO   Ball  ( BALLNO,  XPOS,  YPOS, XVEL, YVEL  )
                                VALUES    ( ?, ?, ?, ?, ? );""", (item.obj.rolling_ball.number, item.obj.rolling_ball.pos.x, item.obj.rolling_ball.pos.y, item.obj.rolling_ball.vel.x, item.obj.rolling_ball.vel.y) );
                ballIDs.append(conns.lastrowid)
            if isinstance(item, StillBall):
                conns.execute( """INSERT
                                    INTO   Ball  ( BALLNO, XPOS, YPOS  )
                                    VALUES    ( ?, ?, ?);""", (item.obj.rolling_ball.number, item.obj.rolling_ball.pos.x, item.obj.rolling_ball.pos.y))
                ballIDs.append(conns.lastrowid)
        
        conns.execute( """INSERT
                        INTO   TTable  ( TIME )
                        VALUES    ( ?);""", (table.time,))
        tableID = conns.lastrowid
        #print(tableID)
        for ball in ballIDs:
            conns.execute("""INSERT INTO BallTable (BALLID, TABLEID)
                            SELECT Ball.BALLID, TTable.TABLEID
                            FROM Ball, TTable
                            WHERE Ball.BALLID==(?) AND TTable.TABLEID==(?);""", (ball, tableID))

        conns.close()
        self.conn.commit()
        return tableID-1
    
    def close(self):
        self.conn.commit()
        self.conn.close()

    
class Game ():
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        self.gameID = gameID
        self.gameName = gameName
        self.player1Name = player1Name
        self.player2Name = player2Name
        self.db = Database()
        self.db.createDB()
        self.conn = self.db.conn.cursor()

        if gameID != None and gameName == None and player1Name == None and player2Name == None:
            self.gameID = gameID + 1
            self.getGame()
            self.conn.close()
            self.db.conn.commit()
            self.db.conn.close()
            return
        elif gameID != None and (gameName != None or player1Name != None or player2Name != None):
            self.conn.close()
            self.db.conn.close()
            raise TypeError("GameID and another parameter are not None")
        elif gameID == None and (gameName == None or player1Name == None or player2Name == None):
            self.conn.close()
            self.db.conn.close()
            raise TypeError("GameID and another parameter are None")

        self.conn.execute( """INSERT
                            INTO   Game  (GAMENAME)
                            VALUES    ( ?);""", (gameName,))
        
        self.gameID = self.conn.lastrowid
        #print(str(gameID) + " is Gameid")

        self.conn.execute( """INSERT
                            INTO   Player  ( GAMEID, PLAYERNAME)
                            VALUES    ( ?, ?);""", (self.gameID, player1Name))
        
        player1ID = self.conn.lastrowid
        #print(player1Name + " is p1 name and id " + str(player1ID))

        self.conn.execute( """INSERT
                            INTO   Player  ( GAMEID, PLAYERNAME)
                            VALUES    ( ?, ?);""", (self.gameID, player2Name,))

        player2ID = self.conn.lastrowid
        #print(player2Name + " is p1 name and id " + str(player2ID))

        self.conn.close()
        self.db.conn.commit()
        self.db.conn.close()

    def getGame(self):
        gameInfo = self.conn.execute("""SELECT Player.PLAYERID, Player.PLAYERNAME, Game.GAMENAME
                                FROM Player
                                INNER JOIN Game ON (Player.GAMEID==(?) AND Game.GAMEID==(?));""", (self.gameID,self.gameID)).fetchall()
        #print("The game info:")
        #print(gameInfo)

        if len(gameInfo) >= 2:
            self.gameName = gameInfo[0][2]
            if gameInfo[0][0] < gameInfo[1][0]:
                self.player1Name = gameInfo[0][1]
                self.player2Name = gameInfo[1][1]
            else:
                self.player2Name = gameInfo[0][1]
                self.player1Name = gameInfo[1][1]

    def cueBall(self, table, xvel, yvel):
        index = 0
        vel = Coordinate(xvel, yvel)
        newTable = Table()

        for item in table:
            if isinstance(item, RollingBall):
                if item.obj.rolling_ball.number == 0:
                    item.obj.rolling_ball.vel.x = xvel
                    item.obj.rolling_ball.vel.y = yvel

                    aLenVel = phylib.phylib_length(vel)
                    if aLenVel > VEL_EPSILON:
                        item.obj.rolling_ball.acc.y = ((-1.0*vel.y) / aLenVel) * DRAG
                        item.obj.rolling_ball.acc.x = ((-1.0*vel.x) / aLenVel) * DRAG
                newTable += item
            elif isinstance(item, StillBall):
                if item.obj.still_ball.number == 0:
                    #Store the postion temporarily
                    posx = item.obj.still_ball.pos.x
                    posy = item.obj.still_ball.pos.y

                    #Change to rolling ball
                    item.type = phylib.PHYLIB_ROLLING_BALL
                    item.obj.rolling_ball.number = 0

                    #Copy position
                    item.obj.rolling_ball.pos.x = posx
                    item.obj.rolling_ball.pos.y = posy

                    #Copy velocity
                    item.obj.rolling_ball.vel.x = xvel
                    item.obj.rolling_ball.vel.y = yvel

                    #Add acceleration
                    aLenVel = phylib.phylib_length(vel)
                    if aLenVel > VEL_EPSILON:
                        item.obj.rolling_ball.acc.y = ((-1.0*vel.y) / aLenVel) * DRAG
                        item.obj.rolling_ball.acc.x = ((-1.0*vel.x) / aLenVel) * DRAG
                newTable += item
            index += 1
        return newTable


    def shoot(self, gameName, playerName, table, xvel, yvel):
        #print("Shoot")
        conns = sqlite3.connect( 'phylib.db' );
        self.conn = conns.cursor()
        shotID = 0
        
        #Add the game to the shot table
        self.conn.execute( """INSERT INTO Shot (PLAYERID, GAMEID)
                            SELECT Player.PLAYERID, Game.GAMEID
                            FROM Player, Game
                            WHERE Player.PLAYERNAME==(?) AND Game.GAMENAME==(?)""", (playerName, gameName)).fetchall()
        shotID = self.conn.lastrowid

        self.conn.close()
        conns.commit()
        conns.close()
        
        #Change cueBall to rollingball
        newTable = self.cueBall(table, xvel, yvel)
        table = newTable

        #Keep track of time
        currentTime = table.time
        newTime = table.time

        #These are table variables used below
        oldTable = table
        newTable = newTable.segment()
        rollingT = Table()

        while newTable != None:
            newTime = newTable.time
            
            timeDifference = newTime - currentTime
            totalTime = int(timeDifference / FRAME_INTERVAL)

            #print("Total time: " + str(totalTime))

            for i in range(totalTime):
                #Create the frame
                rollingT = oldTable.roll(i*FRAME_INTERVAL)
                rollingT.time = currentTime + i*FRAME_INTERVAL

                #Write the frame
                data = Database(reset=False)
                tableID = data.writeTable(rollingT) + 1
                data.close()

                conns = sqlite3.connect( 'phylib.db' );
                self.conn = conns.cursor()
                self.conn.execute( """INSERT INTO TableShot (TABLEID, SHOTID)
                                        SELECT TTable.TABLEID, Shot.SHOTID
                                        FROM TTable, Shot
                                        WHERE TTable.TABLEID==(?) AND Shot.SHOTID==(?)""", (tableID, shotID)).fetchall()

                self.conn.close()
                conns.commit()
                conns.close()

            currentTime = newTime
            oldTable = newTable
            newTable = newTable.segment()
        
        #print("Final current time: " + str(currentTime))
        table = oldTable

        #Write the final frame - (Cue ball falls in the hole)
        data = Database(reset=False)
        tableID = data.writeTable(table) + 1
        data.close()

        conns = sqlite3.connect( 'phylib.db' );
        self.conn = conns.cursor()
        self.conn.execute( """INSERT INTO TableShot (TABLEID, SHOTID)
                                SELECT TTable.TABLEID, Shot.SHOTID
                                FROM TTable, Shot
                                WHERE TTable.TABLEID==(?) AND Shot.SHOTID==(?)""", (tableID, shotID)).fetchall()

        self.conn.close()
        conns.commit()
        conns.close()
        return shotID
