from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CommandHandler, CallbackQueryHandler
import random
import time
from final_token import tok

black = '⚫️'
white = '⚪️'

def show_board(board):
    M = [['  ' for b in range(8)]for a in range(8)]
    for i in range(8):
        for j in range(8):
            if (i, j) in board:
                M[i][j] = board[(i, j)]

    for i in range(8):
        print(M[i], "\n")

def enc(board):
    # board is a dictionary mapping (row, col) to grid
    # grid = [[board.get((row, col), '') for col in range(8)] for row in range(8)]
    number = 0
    base = 3
    for row in range(8):
        for col in range(8):
            number *= base
            # if grid[row][col] == black:
            if board.get((row, col)) == black:
                number += 2
            # elif grid[row][col] == white:
            elif board.get((row, col)) == white:
                number += 1
    return str(number)


def dec(number):
    board = {}
    base = 3
    for row in [7, 6, 5, 4, 3, 2, 1, 0]:
        for col in [7, 6, 5, 4, 3, 2, 1, 0]:
            if number % 3 == 2:
                board[(row, col)] = black
            elif number % 3 == 1:
                board[(row, col)] = white
            number //= base
    return board


def board_markup(board):
    # board will be encoded and embedded to callback_data
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(board.get((row, col), ' '), callback_data=f'{row}{col}{enc(board)}') for col in range(8)]
        for row in range(8)])


def playervalid(board):
    dir = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]  # 方向
    player_validplace = []

    for (i, j) in board:
        if board[(i, j)] == black:
            for k in range(8):  # 每個方向檢查
                #print("dir: ", dir[k])
                search_r = i + dir[k][0]
                search_c = j + dir[k][1]
                if (search_r, search_c) in board:
                    if board[(search_r, search_c)] == '⚪️':  # 先檢查第一個是不是白子
                        #print("may valid for black")
                        while search_r + dir[k][0] >= 0 and search_c + dir[k][1] >= 0 and search_r + dir[k][0] <= 7 and search_c + dir[k][1] <= 7:  # 再檢查這個方向的所有子
                            search_r = search_r + dir[k][0]
                            search_c = search_c + dir[k][1]
                            #print("search_r: ", search_r, "search_c:", search_c)
                            if (search_r, search_c) in board:  # 檢查方向上還有沒有子
                                #print("find: ", (search_r, search_c))
                                if board[(search_r, search_c)] == '⚫️':  # 找到黑色跳出迴圈，若是白色則繼續找
                                    break
                            else:  # 這方向上已經沒有子跳出迴圈
                                #print("valid for white")
                                player_validplace.append((search_r, search_c))
                                break
    return player_validplace


def whitevalid(board):
    dir = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]  # 方向
    white_validplace = []

    for (i, j) in board:
        if board[(i, j)] == white:
            for k in range(8):  # 每個方向檢查
                #print("dir: ", dir[k])
                search_r = i + dir[k][0]
                search_c = j + dir[k][1]
                if (search_r, search_c) in board:
                    if board[(search_r, search_c)] == '⚫️':  # 先檢查第一個是不是黑子
                        #print("may valid for white")
                        while search_r + dir[k][0] >= 0 and search_c + dir[k][1] >= 0 and search_r + dir[k][0] <= 7 and search_c + dir[k][1] <= 7:  # 再檢查這個方向的所有子
                            search_r = search_r + dir[k][0]
                            search_c = search_c + dir[k][1]
                            #print("search_r: ", search_r, "search_c:", search_c)
                            if (search_r, search_c) in board:  # 檢查方向上還有沒有子
                                #print("find: ", (search_r, search_c))
                                if board[(search_r, search_c)] == '⚪️':  # 找到白色跳出迴圈，若是黑色則繼續找
                                    break
                            else:  # 這方向上已經沒有子跳出迴圈
                                #print("valid for white")
                                white_validplace.append((search_r, search_c))
                                break
    return white_validplace


# Define a few command handlers. These usually take the two arguments update and
# context.
async def func(update, context):
    data = update.callback_query.data
    # user clicked the button on row int(data[0]) and col int(data[1])
    row = int(data[0])
    col = int(data[1])
    #await context.bot.answer_callback_query(update.callback_query.id, f'你按的 row {row} col {col}')
    # TODO: check if the button is clickable. if not, report it is not clickable and return
    # the board is encoded and stored as data[2:]
    board = dec(int(data[2:]))
    print("current board: \n", show_board(board)) # current board
    #player_validplace = []
    #white_validplace = []
    dir = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]  # 方向

    while(True):
        # 檢查黑子是否能下
        time.sleep(3)
        player_validplace = playervalid(board)
        white_validplace = whitevalid(board)
        print("player_validplace:", player_validplace)  # 玩家可下的地方
        print("white_validplace:", white_validplace) # 電腦可下的地方

        if(player_validplace == [] and white_validplace == []): # gameover
            break
        elif(player_validplace == []):
            # White's turn
            white_choice = random.choice(white_validplace)  # 電腦下的白子位置
            board[white_choice] = white
            print(white_choice)

            change_white = []  # 黑子該被換成白子的位置
            for i in range(8):  # 每個方向檢查
                #print("dir: ", dir[i])

                Wcurr = []  # 紀錄黑子位子
                Wcurr_valid = False  # 黑子該不該被換成白子

                search_r = white_choice[0] + dir[i][0]
                search_c = white_choice[1] + dir[i][1]
                if (search_r, search_c) in board:
                    if board[(search_r, search_c)] == '⚫️':  # 先檢查第一個是不是黑子
                        Wcurr.append((search_r, search_c))
                        #print("may valid")
                        while search_r + dir[i][0] >= 0 and search_c + dir[i][1] >= 0 and search_r + dir[i][0] <= 7 and search_c + dir[i][1] <= 7:  # 再檢查這個方向的所有子
                            search_r = search_r + dir[i][0]
                            search_c = search_c + dir[i][1]
                            #print("search_r: ", search_r, "search_c:", search_c)
                            if (search_r, search_c) in board:  # 檢查方向上還有沒有子
                                #print("find: ", (search_r, search_c))
                                if board[(search_r, search_c)] == '⚪️':  # 找到白色則跳出迴圈
                                    #print("valid")
                                    Wcurr_valid = True
                                    break
                                else:  # 找到黑色繼續找
                                    Wcurr.append((search_r, search_c))
                            else:  # 這方向上已經沒有子且還沒找到白子則跳出迴圈
                                #print("not valid")
                                break
                        #print("Wcurr: ", Wcurr)
                        if Wcurr_valid == True:
                            change_white += Wcurr  # 紀錄該被換成黑子的白子
            print("change_white: ", change_white)

            for (i, j) in change_white:
                board[(i, j)] = white

            await context.bot.edit_message_text('目前盤面，白子已下',
                                                reply_markup=board_markup(board),
                                                chat_id=update.callback_query.message.chat_id,
                                                message_id=update.callback_query.message.message_id)
            await context.bot.edit_message_text('目前盤面，輪到你下了',
                                                reply_markup=board_markup(board),
                                                chat_id=update.callback_query.message.chat_id,
                                                message_id=update.callback_query.message.message_id)

        elif(white_validplace == []):
            if (row, col) in board:  # 已下子的地方無法再下
                await context.bot.answer_callback_query(update.callback_query.id,
                                                        f'你按的 r: {row} c: {col} 已下子，無法下子')
            else:
                # Player's turn
                valid = False
                while (valid == False):  # 給玩家下直到下到可以下的位置
                    change_black = []  # 白子該被換成黑子的位置

                    for i in range(8):  # 每個方向檢查
                        #print("dir: ", dir[i])

                        curr = []  # 紀錄白子位子
                        curr_valid = False  # 白子該不該被換成黑子

                        search_r = row + dir[i][0]
                        search_c = col + dir[i][1]
                        if (search_r, search_c) in board:
                            if board[(search_r, search_c)] == '⚪️':  # 先檢查第一個是不是白子
                                curr.append((search_r, search_c))
                                #print("may valid")
                                while search_r + dir[i][0] >= 0 and search_c + dir[i][1] >= 0 and search_r + dir[i][
                                    0] <= 7 and search_c + dir[i][1] <= 7:  # 再檢查這個方向的所有子
                                    search_r = search_r + dir[i][0]
                                    search_c = search_c + dir[i][1]
                                    #print("search_r: ", search_r, "search_c:", search_c)
                                    if (search_r, search_c) in board:  # 檢查方向上還有沒有子
                                        #print("find: ", (search_r, search_c))
                                        if board[(search_r, search_c)] == '⚫️':  # 找到黑色則跳出迴圈
                                            #print("valid")
                                            valid = True
                                            curr_valid = True
                                            break
                                        else:  # 找到白色繼續找
                                            curr.append((search_r, search_c))
                                    else:  # 這方向上已經沒有子且還沒找到黑子則跳出迴圈
                                        #print("not valid")
                                        break
                                #print("curr: ", curr)
                                if curr_valid == True:
                                    change_black += curr  # 紀錄該被換成黑子的白子

                    if valid == True:  # Player's turn valid
                        print("change_black: ", change_black)
                        for (i, j) in change_black:
                            board[(i, j)] = black
                        board[(row, col)] = black
                        await context.bot.answer_callback_query(update.callback_query.id,
                                                                f'你按的 r: {row} c: {col} 已下子')
                        print("after player's turn:", show_board(board))  # current board after player's turn
                    else:  # Player's turn not valid
                        await context.bot.answer_callback_query(update.callback_query.id,
                                                                f'你按的 row {row} col {col} 無法下子')
            await context.bot.edit_message_text('目前盤面，輪到你下了',
                                                reply_markup=board_markup(board),
                                                chat_id=update.callback_query.message.chat_id,
                                                message_id=update.callback_query.message.message_id)

        else:
            if (row, col) in board:  # 已下子的地方無法再下
                await context.bot.answer_callback_query(update.callback_query.id, f'你按的 r: {row} c: {col} 已下子，無法下子')
            else:
                # Player's turn
                valid = False
                while(valid == False): # 給玩家下直到下到可以下的位置
                    change_black = []  # 白子該被換成黑子的位置

                    for i in range(8):  # 每個方向檢查
                        #print("dir: ", dir[i])

                        curr = []  # 紀錄白子位子
                        curr_valid = False  # 白子該不該被換成黑子

                        search_r = row + dir[i][0]
                        search_c = col + dir[i][1]
                        if (search_r, search_c) in board:
                            if board[(search_r, search_c)] == '⚪️':  # 先檢查第一個是不是白子
                                curr.append((search_r, search_c))
                                #print("may valid")
                                while search_r + dir[i][0] >= 0 and search_c + dir[i][1] >= 0 and search_r + dir[i][0] <= 7 and search_c + dir[i][1] <= 7:  # 再檢查這個方向的所有子
                                    search_r = search_r + dir[i][0]
                                    search_c = search_c + dir[i][1]
                                    #print("search_r: ", search_r, "search_c:", search_c)
                                    if (search_r, search_c) in board:  # 檢查方向上還有沒有子
                                        #print("find: ", (search_r, search_c))
                                        if board[(search_r, search_c)] == '⚫️':  # 找到黑色則跳出迴圈
                                            #print("valid")
                                            valid = True
                                            curr_valid = True
                                            break
                                        else:  # 找到白色繼續找
                                            curr.append((search_r, search_c))
                                    else:  # 這方向上已經沒有子且還沒找到黑子則跳出迴圈
                                        #print("not valid")
                                        break
                               #print("curr: ", curr)
                                if curr_valid == True:
                                    change_black += curr  # 紀錄該被換成黑子的白子

                    if valid == True: # Player's turn valid
                        print("change_black: ", change_black)
                        for (i, j) in change_black:
                            board[(i, j)] = black
                        board[(row, col)] = black
                        await context.bot.answer_callback_query(update.callback_query.id, f'你按的 r: {row} c: {col} 已下子，請等待白子下')
                        print("after player's turn:", show_board(board))  # current board after player's turn
                        await context.bot.edit_message_text('目前盤面，請等待白子下',
                                                            reply_markup=board_markup(board),
                                                            chat_id=update.callback_query.message.chat_id,
                                                            message_id=update.callback_query.message.message_id)
                    else: # Player's turn not valid
                        await context.bot.answer_callback_query(update.callback_query.id, f'你按的 row {row} col {col} 無法下子')

                # White's turn
                white_validplace = whitevalid(board)
                if white_validplace != []:
                    white_choice = random.choice(white_validplace)  # 電腦下的白子位置
                    board[white_choice] = white
                    print(white_choice)

                    change_white = []  # 黑子該被換成白子的位置
                    for i in range(8):  # 每個方向檢查
                        #print("dir: ", dir[i])

                        Wcurr = []  # 紀錄黑子位子
                        Wcurr_valid = False  # 黑子該不該被換成白子

                        search_r = white_choice[0] + dir[i][0]
                        search_c = white_choice[1] + dir[i][1]
                        if (search_r, search_c) in board:
                            if board[(search_r, search_c)] == '⚫️':  # 先檢查第一個是不是黑子
                                Wcurr.append((search_r, search_c))
                                #print("may valid")
                                while search_r + dir[i][0] >= 0 and search_c + dir[i][1] >= 0 and search_r + dir[i][
                                    0] <= 7 and search_c + dir[i][1] <= 7:  # 再檢查這個方向的所有子
                                    search_r = search_r + dir[i][0]
                                    search_c = search_c + dir[i][1]
                                    #print("search_r: ", search_r, "search_c:", search_c)
                                    if (search_r, search_c) in board:  # 檢查方向上還有沒有子
                                        #print("find: ", (search_r, search_c))
                                        if board[(search_r, search_c)] == '⚪️':  # 找到白色則跳出迴圈
                                            #print("valid")
                                            Wcurr_valid = True
                                            break
                                        else:  # 找到黑色繼續找
                                            Wcurr.append((search_r, search_c))
                                    else:  # 這方向上已經沒有子且還沒找到白子則跳出迴圈
                                        #print("not valid")
                                        break
                                #print("Wcurr: ", Wcurr)
                                if Wcurr_valid == True:
                                    change_white += Wcurr  # 紀錄該被換成黑子的白子
                    #print("change_white: ", change_white)

                    for (i, j) in change_white:
                        board[(i, j)] = white

                    await context.bot.edit_message_text('目前盤面，白子已下',
                                                        reply_markup=board_markup(board),
                                                        chat_id=update.callback_query.message.chat_id,
                                                        message_id=update.callback_query.message.message_id)

                await context.bot.edit_message_text('目前盤面，輪到你下了',
                                                    reply_markup=board_markup(board),
                                                    chat_id=update.callback_query.message.chat_id,
                                                    message_id=update.callback_query.message.message_id)


    print("gameover")
    black_sum = 0
    white_sum = 0
    for (i, j) in board:
        if board[(i, j)] == black:
            black_sum += 1
        if board[(i, j)] == white:
            white_sum += 1
    print("black_sum: ", black_sum)
    print("white_sum: ", white_sum)

    if(black_sum>white_sum):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="遊戲結束，你贏了")

    elif(black_sum<white_sum):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="遊戲結束，你輸了")

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="遊戲結束，平手")


async def start(update, context):
    board = {(3,3): '⚫️', (3,4): '⚪️', (4,3): '⚪️', (4,4): '⚫️'}
    # reply_markup = board_markup(board)
    await update.message.reply_text('目前盤面，請開始遊戲', reply_markup=board_markup(board))


def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(tok).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("game_start", start))

    application.add_handler(CallbackQueryHandler(func))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()