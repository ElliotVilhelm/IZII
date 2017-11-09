import sys
import Engine
import re
import logging


engine = Engine.IZII()
init_board = "xxxxxxxxxx" \
             "xxxxxxxxxx" \
             "xrnbqkbnrx" \
             "xppppppppx" \
             "xoooooooox" \
             "xoooooooox" \
             "xoooooooox" \
             "xoooooooox" \
             "xPPPPPPPPx" \
             "xRNBQKBNRx" \
             "xxxxxxxxxx" \
             "xxxxxxxxxx"

init_board = list(init_board)
init_state = [init_board, 0, -1, 0, 1, [0, 0, 0, 0], init_board.index('K'), init_board.index('k')]

WHITE = 0
BLACK = 1
def reply(command):
    logging.debug('<<'+command)
    sys.stdout.write(command + '\n')
    sys.stdout.flush()

def run_xboard():
    state = init_state
    force_mode = False
    history = []
    if sys.stdout.isatty():
        reply("-> Welcome to IZZI!, type 'new' to start a new game")

    # Begin Input loop
    while True:
        try:
            line = input()
        except IOError:
            print('-> got IOError')
            continue
        # Prep and log input
        cmd = line.strip()  # remove whitespace
        logging.debug(">> " + cmd)
        if cmd == 'xboard':
            reply("tellics say     IZZI")
            reply("tellics say     (c) Elliot Vilhelm Pourmand, All rights reserved.")
        elif cmd == 'new':
            state = init_state
            history = []
            force_mode = False
        elif cmd == 'protover 2':
            reply('feature myname="Elliots\'s IZZI"')
            reply('feature ping=1')
            reply('feature san=0')
            reply('feature sigint=0')
            reply('feature sigterm=0')
            reply('feature setboard=1')
            reply('feature debug=1')
            reply('feature time=0')
            reply('feature done=1')
        elif cmd == 'force':
            force_mode = True
        elif cmd == 'go':  # start playing
            force_mode = False
            move = engine.best_move(state, 2)
            fromsq = engine.sq120_sq64(move[0])
            tosq = engine.sq120_sq64(move[1])
            fromsq = engine.sq64_to_RF(fromsq)
            tosq = engine.sq64_to_RF(tosq)
            move_txt = fromsq[0] + fromsq[1] + tosq[0] + tosq[1]
            state = engine.run_move_at_state(state, move)
            reply("# moving in go")
            reply("move " + move_txt.lower())
        elif cmd.startswith('ping'):
            n = cmd.split(' ')[-1]
            reply('pong ' + n)
        elif cmd == 'white':
            my_team = WHITE
            reply('#Changed to  white')
        elif cmd == 'black':
            my_team = BLACK
            reply('#Changed to black')
        elif cmd == 'quit':
            return
        else:
            if re.match('^[a-h][1-8][a-h][1-8].?$', cmd):
                # Update my board
                fromsq = cmd[0:2]
                tosq = cmd[2:4]
                fromsq120 = engine.sq64_to_sq120(engine.RF_sq64(fromsq[0], fromsq[1]))
                tosq120 = engine.sq64_to_sq120(engine.RF_sq64(tosq[0], tosq[1]))
                history.append(state)
                state = engine.run_move_at_state(state, [fromsq120, tosq120])
                logging.debug("state after re.match")
                logging.debug(engine.get_board(state[0]))
                if not force_mode:
                    move = engine.best_move(state, 2)
                    fromsq = engine.sq120_sq64(move[0])
                    tosq = engine.sq120_sq64(move[1])
                    fromsq = engine.sq64_to_RF(fromsq)
                    tosq = engine.sq64_to_RF(tosq)
                    move_txt = fromsq[0] + fromsq[1] + tosq[0] + tosq[1]
                    state = engine.run_move_at_state(state, move)
                    logging.debug(engine.get_board(state[0]))
                    reply("# state after moving in not force")
                    reply("move " + move_txt.lower())
            else:
                reply("#non registered command : '" + cmd + "'")

if __name__ == '__main__':
    import sys
    logging.basicConfig(filename='test.log',level=logging.DEBUG)
    run_xboard()
