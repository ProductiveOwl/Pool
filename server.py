import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl;

import os # This is to delete the svg files
import Physics # Need this to calculate acceleration
import math
import re

class MyRequestHandler (BaseHTTPRequestHandler):
    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/index.html' ]:
            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
        
        elif parsed.path in [ '/previousTable.svg' ] or parsed.path in [ '/recentTable.svg' ]:
            # this one is different because its an image file
            # retreive the svg file (binary, not text file)
            fp = open( '.'+self.path, 'rb' );
            content = fp.read();

            self.send_response( 200 ); # OK
                # notice the change in Content-type
            self.send_header( "Content-type", "image/svg+xml" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            self.wfile.write( content );    # binary file
            fp.close();

        elif '/table-' in parsed.path and '.svg' in parsed.path:
            # this one is different because its an image file
            # retreive the svg file (binary, not text file)
            #fp = open( '.'+self.path, 'rb' );
            #content = fp.read();

            #newTableStr = ""
            tableString = parsed.path
            pattern = r'/table-(\d+)\.svg'
            match = re.search(pattern, tableString)
            if match:
                tableID = int(match.group(1))

                db = Physics.Database();
                cur = db.conn.cursor();
                #print("Reading tableid: " + str(tableID))
                table = db.readTable(tableID)

                with open( "table-" + str(tableID) + ".svg", "w+" ) as fp:
                    fp.write( table.svg() );
                
                cur.close();
                db.conn.commit();
                db.conn.close();
                
            fp = open( "table-" + str(tableID) + ".svg", 'rb' );
            content = fp.read();
            os.remove("table-" + str(tableID) + ".svg")


            self.send_response( 200 ); # OK
                # notice the change in Content-type
            self.send_header( "Content-type", "image/svg+xml" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            self.wfile.write( content );    # binary file
            fp.close();

        elif parsed.path in [ '/styles.css' ]:
            # retreive the CSS file
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
        elif parsed.path in ['/jquery.js']:
            # retreive the CSS file
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


    def do_POST(self):
        # hanle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );
        
        if parsed.path in [ '/shoot.html' ]:
            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                   );

            db = Physics.Database();
            cur = db.conn.cursor();

            cur.execute( """\
            SELECT TABLEID FROM TableShot;""");
            tableIDs = cur.fetchall();

            #print("Previous tableID " + str(len(tableIDs)))
            table = db.readTable(len(tableIDs))
            foundCue = False
            for item in table:
                if isinstance(item, Physics.RollingBall):
                    if item.obj.rolling_ball.number == 0:
                        foundCue = True
                elif isinstance(item, Physics.StillBall):
                    if item.obj.still_ball.number == 0:
                        foundCue = True
            if not foundCue:
                #Restore the cue ball to the orginal position and update the recent table + database
                pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0, Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
                sb  = Physics.StillBall( 0, pos );
                table += sb;
            
            with open('previousTable.svg','w+') as fp:
                fp.write( table.svg() );
            previousTable = table.svg()

            #Deleting the svg tables
            tableIndex = len(tableIDs)
            while (True):
                if os.path.exists("table-%d.svg" %(tableIndex)):
                    os.remove("table-%d.svg" %(tableIndex))
                    tableIndex -= 1
                else:
                    break

            game = Physics.Game( gameID=0 )
            #if not isinstance(form['xInput'].value, (int, float)):
            #    game.shoot("Game 01", game.player1Name, table, 0, 0)
             #   print("Invalid x")
            #else:
            #    print("Proper X")
            game.shoot("Game 01", form['current'].value, table, float(form['xInput'].value), float(form['yInput'].value))
            
            cur.execute( """\
            SELECT TABLEID FROM TableShot;""");
            maxTableID = cur.fetchall();

            #print("Recent tableID " + str(len(maxTableID)))
            table = db.readTable(len(maxTableID))
            with open('recentTable.svg','w+') as fp:
                fp.write( table.svg() );
            recentTable = table.svg()

            #print(form['xInput'].value)
            #print(form['yInput'].value)

            #maxTableID = 4
            shootString = ""
            with open('shoot.html','r') as file:
                shootString = file.read()

            if "maxTableID" in shootString:
                shootString = shootString.replace("maxTableID", str(len(maxTableID)))
            else:
                pattern = r'\(num > (\d+)\) \{'
                shootString = re.sub(pattern, f'(num > {len(maxTableID)}) {{', shootString)
            
            if "var num = 1;" in shootString:
                shootString = shootString.replace("var num = 1;", "var num = " + str(len(tableIDs)) + ";")
            else:
                pattern = r'var num = (\d+);'
                shootString = re.sub(pattern, f'var num = {len(tableIDs)};', shootString)


            #Change player's turn here
            nextPlayer = game.player2Name
            #print("recentTable = " + recentTable)
            #print("Num circles: " + str(recentTable.count("circle")))
            if (recentTable.count("circle") == previousTable.count("circle")): #No points were scored
                if form['current'].value == game.player2Name:
                    nextPlayer = game.player1Name
            else:
                pattern = r'fill="([^"]+)"'
                recentBallColours = re.findall(pattern, recentTable)
                previousBallColours = re.findall(pattern, previousTable)
                ballsScored = list(set(previousBallColours) - set(recentBallColours))
                #print(ballsScored)
                #8 ball was sunk, the other person wins or the current player wins if its the only other ball left for them
                if "BLACK" in ballsScored:
                    if game.player1Name == form['current'].value:
                        for num in range(0, len(recentBallColours)):
                            index = Physics.BALL_COLOURS.index(recentBallColours[num])
                            if (index <= 7):
                                shootString = shootString.replace("Winner: ?", "The winner is " + game.player2Name)
                                break
                        shootString = shootString.replace("Winner: ?", "The winner is " + game.player1Name)
                    else:
                        for num in range(0, len(recentBallColours)):
                            index = Physics.BALL_COLOURS.index(recentBallColours[num])
                            if (index > 7):
                                shootString = shootString.replace("Winner: ?", "The winner is " + game.player1Name)
                                break
                        shootString = shootString.replace("Winner: ?", "The winner is " + game.player2Name)

                elif "WHITE" in ballsScored:
                #Restore the cue ball to the orginal position and update the recent table + database
                    pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0, Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
                    sb  = Physics.StillBall( 0, pos );
                    table += sb;
                    #print("In white")
                    with open('recentTable.svg','w+') as fp:
                        fp.write( table.svg() );

                if not (len(ballsScored) == 1 and "WHITE" in ballsScored) and (float(form['ballType'].value) == 0):
                    pattern = r'size="1" value="(\d+)"'
                    shootString = re.sub(pattern, rf'size"1" value="{1}"', shootString)
                    index = Physics.BALL_COLOURS.index(ballsScored[0])
                    if index > 7 and form['current'].value == game.player1Name:
                        pattern = r'(id="player1Name">)(.*?)(</th>)'
                        shootString = re.sub(pattern, rf'\g<1>{game.player2Name + " (low)"}\g<3>', shootString)
                        pattern = r'(id="player2Name">)(.*?)(</th>)'
                        shootString = re.sub(pattern, rf'\g<1>{game.player1Name + " (high)"}\g<3>', shootString)
                        game.player1Name = game.player2Name
                        game.player2Name = form['current'].value
                        nextPlayer = game.player1Name
                    else:
                        pattern = r'(id="player1Name">)(.*?)(</th>)'
                        shootString = re.sub(pattern, rf'\g<1>{game.player1Name + " (low)"}\g<3>', shootString)
                        pattern = r'(id="player2Name">)(.*?)(</th>)'
                        shootString = re.sub(pattern, rf'\g<1>{game.player2Name+ " (high)"}\g<3>', shootString)

                for num in range(0, len(ballsScored)):
                    index = Physics.BALL_COLOURS.index(ballsScored[num])
                    if (index > 0 and index <= 7 and form['current'].value == game.player1Name):
                        nextPlayer = game.player1Name
                        break

            #Update the turn
            pattern = r'(id="currentTurn">).*?(</h2>)'
            shootString = re.sub(pattern, rf'\1{nextPlayer}\2', shootString)

            #Close the database
            cur.close();
            db.conn.commit();
            db.conn.close();

            #Write shoot.html and sent it back
            aFile = open("shoot.html", "w+")
            aFile.write(shootString)
            aFile.close()


            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(shootString));
            self.end_headers();

            self.wfile.write( bytes( shootString, "utf-8" ) );
        
        elif parsed.path in [ '/players.html' ]:
            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                   );

            #Deleting the svg tables
            tableIndex = 0
            while (True):
                if os.path.exists("table-%d.svg" %(tableIndex)):
                    os.remove("table-%d.svg" %(tableIndex))
                    tableIndex += 1
                else:
                    break

            indexString = ""
            with open('index.html','r') as file:
                indexString = file.read().replace('Player 1', form['p1'].value)
            indexString = indexString.replace('Player 2', form['p2'].value)
            indexString = indexString.replace('___', form['p1'].value)

            aFile = open("players.html", "w+")
            aFile.write(indexString)
            aFile.close()

            aFile = open("shoot.html", "w+")
            shootString = """<script id="shootScript">
                                var num = 1;
                                function makeShot() {
                                    $("#poolTable").load("table-" + num + ".svg");
                                    num++;
                                    if (num > maxTableID) {
                                        $("#poolTable").load("recentTable.svg");
                                        clearInterval(intervalID);
                                    }
                                }
                                window.onload = makeShot; // Call the function once the page is loaded
                                intervalID = setInterval(makeShot, 100);
                            </script>"""
            aFile.write(indexString+shootString)
            aFile.close()

            db = Physics.Database( reset=True );
            db.createDB();

            table = Physics.Table()

            pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0, Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
            sb  = Physics.StillBall( 0, pos );
            table += sb;
            pos = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0, Physics.TABLE_WIDTH / 2.0,);
            sb = Physics.StillBall( 1, pos );
            table += sb
            pos = Physics.Coordinate(Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0, Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0));
            sb = Physics.StillBall( 2, pos );
            table += sb
            pos = Physics.Coordinate(Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0, Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0));
            sb = Physics.StillBall( 3, pos );
            table += sb;
            pos = Physics.Coordinate(612.0, 571.0);
            sb = Physics.StillBall( 4, pos );
            table += sb;
            pos = Physics.Coordinate(675.0, 571.0);
            sb = Physics.StillBall( 5, pos );
            table += sb;
            pos = Physics.Coordinate(735.0, 571.0);
            sb = Physics.StillBall( 6, pos );
            table += sb;
            pos = Physics.Coordinate(575.0, 520.0);
            sb = Physics.StillBall( 7, pos );
            table += sb;
            pos = Physics.Coordinate(644.0, 520.0);
            sb = Physics.StillBall( 8, pos );
            table += sb;
            pos = Physics.Coordinate(707.0, 518.0);
            sb = Physics.StillBall( 9, pos );
            table += sb;
            pos = Physics.Coordinate(770.0, 520.0);
            sb = Physics.StillBall( 10, pos );
            table += sb;
            pos = Physics.Coordinate(540.0, 470.0);
            sb = Physics.StillBall( 11, pos );
            table += sb;
            pos = Physics.Coordinate(610.0, 470.0);
            sb = Physics.StillBall( 12, pos );
            table += sb;
            pos = Physics.Coordinate(678.0, 465.0);
            sb = Physics.StillBall( 13, pos );
            table += sb;
            pos = Physics.Coordinate(750.0, 465.0);
            sb = Physics.StillBall( 14, pos );
            table += sb;
            pos = Physics.Coordinate(815.0, 468.0);
            sb = Physics.StillBall( 15, pos );
            table += sb;

            db.writeTable(table)
            db.close();
            game = Physics.Game( gameName="Game 01", player1Name=form['p1'].value, player2Name=form['p2'].value );
            
            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(indexString));
            self.end_headers();

            self.wfile.write( bytes( indexString, "utf-8" ) );
        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyRequestHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
