import time
import asyncio
import chess
import chess.engine

INPUT_FILE = "analysis/queue.txt"
OUTPUT_DIR = "analysis"

async def main() -> None:
    num_analysis = 1
    while True:
        board, limit, num_variations = prepare_next_analysis(INPUT_FILE)
        if board is None and limit is None:
            time.sleep(60)
        else:
            info, board = await analyse(board, limit, num_variations)
            print(f"analysis for position number {num_analysis} done")
            num_analysis += 1

            write_results(OUTPUT_DIR, board, info)

async def analyse(board, limit, num_variations):
    transport, engine = await chess.engine.popen_uci(["/lc0/bin/lc0", "--config=/lc0/settings/lc0.config"])
    #transport, engine = await chess.engine.popen_uci("/home/ubuntu/stockfish_14_linux_x64_popcnt/stockfish_14_x64_popcnt")

    multi_info = await engine.analyse(board, limit, multipv=num_variations)
    await engine.quit()
    return multi_info, board

def prepare_next_analysis(input_file):
    position, limit, multipv = None, None, None
    first_legal_position_found = False
    updated_queue = []

    with open(input_file, "r") as file:
        for line in file:
            if first_legal_position_found or line[0] == '#':
                updated_queue.append(line)
            elif len(line) < 10:
                # skipping whitespace
                pass
            else:
                position = extract_position(line)
                limit = extract_limit(line)
                multipv = extract_multipv(line)

                if position is not None and limit is not None:
                    # crucially, this line is not written back to file
                    first_legal_position_found = True
                elif position is None:
                    updated_queue.append("# Next line contains illegal position! It cannot be analysed.\n")
                    updated_queue.append(line)
                elif limit is None:
                    updated_queue.append("# Next line contains illegal termination criterion! It cannot be analysed.\n")
                    updated_queue.append(line)

    with open(input_file, "w") as file:
        for line in updated_queue:
            file.write(line)

    if not first_legal_position_found:
        return None, None, None
    
    return position, limit, multipv

def extract_limit(line):
    limit = None
    param = line.split(";")[1].strip()
    mode = param.split(" ")[0].strip()
    amount = param.split(" ")[1].strip()

    if mode == "depth":
        limit = chess.engine.Limit(depth=int(amount))
    elif mode == "time":
        limit = chess.engine.Limit(time=float(amount))
    elif mode == "nodes":
        limit = chess.engine.Limit(nodes=int(amount))
    
    return limit

def extract_multipv(line):
    multipv = 1
    params = line.split(";")

    if (len(params) == 3 and params[2].strip().split(" ")[0] == "multipv"):
        multipv = int(params[2].strip().split(" ")[1])
    
    return multipv

def extract_position(line):
    fen = line.split(";")[0].strip()
    board = chess.Board(fen)
    if board.is_valid():
        return board
    else:
        return None

def write_results(output_dir, board: chess.Board, results):
    if not isinstance(results, list):
        results = [results]

    with open(f"{output_dir}/{board_descriptor(board)}.txt", "w") as file:
        file.write(f"Analysis for position {board.board_fen()}.\n\n")
        file.write(board.unicode())
        file.write("\n\n")

        for counter, variation in enumerate(results):
            #print(f"depth={info['depth']} | seldepth={info['seldepth']} | time={info['time']} | nodes={info['nodes']} | score={info['score'].white()} | win expectation white={info['wdl'].white().expectation()} | multipv={info['multipv']} | {' '.join([move.uci() for move in info['pv']])}")
            file.write(f"depth={variation['depth']} | ")
            file.write(f"seldepth={variation['seldepth']} | ")
            file.write(f"time={variation['time']} | ")
            file.write(f"nodes={variation['nodes']} | ")
            file.write(f"score={variation['score'].white()} | ")
            file.write(f"win expectation white={variation['wdl'].white().expectation()} | ")
            file.write(f"multipv={counter+1} | ")
            file.write(f"{' '.join([move.uci() for move in variation['pv']])}")
            file.write("\n")

def board_descriptor(board: chess.Board) -> str:
    descriptor = board.board_fen()
    descriptor = descriptor.replace("/", "_")
    return descriptor

if __name__ == "__main__":
    asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
    asyncio.run(main())
