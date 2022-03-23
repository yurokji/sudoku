# 작성자: lowlevel coder
# DISCLAIMER: 코드의 정확성을 보장할 수 없으니 참고하고 사용하세요.

from random import randint, sample
# 리스트를 안전하게 값을 복사하기 위해 사용한다
from copy import deepcopy

# 아직 결정되지 않은 셀의 값
NOT_FILLED = 0
HORIZONTAL_DIRECTION = 0
VERTICAL_DIRECTION = 1
BLOCK = 0
ROW = 1
COL = 2

class Sudoku:
    def __init__(self):
        self.size = 9
        # 빈칸으로 남겨둘 개수만큼 게임의 난이도
        self.difficulty = 10
        self.grid = []
        # 스도쿠 풀이시 막혔을 때 되돌아갈길의 갯수
        self.num_backtracks = 0
        self.num_shuffle = randint(20,100)
        self.user_places = []
        self.fixed_places = [] 
        self.init_grid()
        
    #  스도쿠 그리드 초기화
    def init_grid(self):
        self.grid = []
        self.user_places = []
        self.fixed_places = [] 
        for i in range(self.size):
            row_data = []
            for j in range(self.size):
                row_data.append(NOT_FILLED)
            self.grid.append(row_data)
            
    # 셀의 값이 채워져있지 않은지 확인
    def isCellNotFilled(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == NOT_FILLED:
                    return i,j
        return -1, -1
    
    # 숫자 e가 현재 셀 i, j에 위치할 수 있는 지 체크한다
    def isValid(self, i, j, e):
        # 숫자 e가 같은 행의 모든 열에서 유일한지 체크한다
        rowOk = all([e != self.grid[i][x] for x in range(9)])
        if rowOk:
            # 숫자 e가 같은 열의 모든 행에서 유일한지 체크한다
            colOk = all([e != self.grid[y][j] for y in range(9)])
            if colOk:
                # 숫자 erk 각각의 작은 정사각형 블록내에서도 
                # 유일한지 체크한다
                blockTopX, blockTopY = 3 * (i // 3), 3 * (j //3)
                for x in range(blockTopX, blockTopX + 3):
                    for y in range(blockTopY, blockTopY + 3):
                        if self.grid[x][y] == e:
                            return False
                return True
        return False
                
            
    
    # 주어진 스도쿠 문제에 대한 해답
    def solve(self, i=0, j=0):
        i, j = self.isCellNotFilled()
        # 모든 셀이 다 채워져 값이 있는 경우
        # 다 풀었다고 참값을 반환
        if i == -1:
            return True
        # 아직 다 못푼 경우
        # 1-9까지의 숫자를 랜덤하게 배열하여 샘플한다
        random_list = sample(range(1,10), 9)
        for e in random_list:
            # 고른 1-9의 숫자중 하나가 현재 셀에 올 수 있는지
            # 체크한다
            if self.isValid(i, j, e):
                self.grid[i][j] = e
                # 재귀적으로 현재 시점부터 스도쿠를 푼다
                if self.solve(i,j):
                    return True
                # 만약 해를 못찾았다면
                # 그 지점에서 백트래킹하기 위해 카운트를 올린다
                self.num_backtracks += 1
            # 그리고 현재 위치를 롤백하여 채워지지 않음으로 표시한다
            self.grid[i][j] = NOT_FILLED
        return False
    
    
    # 정사각 (x,y)번째 서브 블록을 하나 가져온다
    def getSubBlock(self, x, y):
        # 각각의 블록에 따라 셀의 위치 i,j값의 범위를 계산한다
        begin_i = x * 3
        end_i = begin_i + 3
        begin_j = y * 3
        end_j = begin_j + 3  
        sub_block = []
        for i in range(begin_i, end_i):
            sub_row = []
            for j in range(begin_j, end_j):
                sub_row.append(self.grid[i][j])
            sub_block.append(sub_row)
        return sub_block
    
    
    # 주어진 정사각 (x,y)번째 서브 블록의 값을 채워준다
    def setSubBlock(self, new_list, x, y):
        # 각각의 블록에 따라 셀의 위치 i,j값의 범위를 계산한다
        begin_i = x * 3
        end_i = begin_i + 3
        begin_j = y * 3
        end_j = begin_j + 3 
        idx = 0
        for i in range(begin_i, end_i):
            for j in range(begin_j, end_j):
                # print(9 * 3 + j, new_list[idx])
                self.grid[i][j] = deepcopy(new_list[idx])
                idx += 1  
        
    
    # 풀이 전에 스도쿠의 일부 셀을 채워준다
    # 스도쿠의 9개의 작은 정사각 블록 중
    # 한 군데만 랜덤하게 채워주고 시작한다
    # 이 때 정사각 블록의 위치도 랜덤하게 정해준다
    def fillOneBlock(self):
        rlist = sample(range(1,10), 9)
        num_block_row = randint(0,2)
        num_block_col = randint(0,2)
        # print("rlist:", rlist)
        self.setSubBlock(rlist, num_block_row, num_block_col)
    
    #스도쿠의 현재 상태를 프린트한다
    def print(self):
        num_row = 0
        for row in self.grid:
            if num_row % 3 == 0 and num_row != 0:
                print(" ")
            print(row[0:3], " ", row[3:6], " ", row[6:9])
            num_row += 1
        print()
        print()
         
    
    #정사각 서브 블록 3개 구역(행방향, 또는 열방향) 두개의 위치를 서로 바꿈
    def swapSubBlock(self, block1, block2, swapdir=HORIZONTAL_DIRECTION):
        temp = [] 
        # 수평방향으로 블록3개의 구역을 서로 바꾼다
        if swapdir==HORIZONTAL_DIRECTION:
            for i in range(3):
                row_num1 = block1 * 3 + i
                row_num2 = block2 * 3 + i
                self.swapRow(row_num1, row_num2)
                
                
        # 수직방향으로 블록3개의 구역을 서로 바꾼다
        else:
            for j in range(3):
                col_num1 = block1 * 3 + j
                col_num2 = block2 * 3 + j
                self.swapCol(col_num1, col_num2)
                
                 

    
    
    # 행을 가져옴
    def getRow(self, i):
        return self.grid[i]
    
    # 열을 가져옴
    def getCol(self, j):
        col = []
        for row in self.grid:
            col.append(row[j])
        return col
        
    # 행에 값을 채움
    def setRow(self, new_row, pos):
        self.grid[pos] = deepcopy(new_row)
        
    # 열에 값을 채움
    def setCol(self, new_col, pos):
        for i in range(self.size):
            self.grid[i][pos] = new_col[i]
            
        
    
    # 두 행의 위치를 바꿈
    def swapRow(self, v1, v2):
        row1 = self.getRow(v1)
        row2 = self.getRow(v2)
        # print(row1, row2)
        self.grid[v1] = deepcopy(row2)
        self.grid[v2] = deepcopy(row1)
        # row1 = self.getRow(v1)
        # row2 = self.getRow(v2)
        # print(row1, row2)
        
    # 두 열의 위치를 바꿈
    def swapCol(self, h1, h2):
        col1 = self.getCol(h1)
        col2 = self.getCol(h2)
        # print(col1, col2)
        self.setCol(col2, h1)
        self.setCol(col1, h2)
        # col1 = self.getCol(h1)
        # col2 = self.getCol(h2)
        # print(col1, col2)
        
        
         
    
    # 풀이가 가능한 스도쿠 데이터가 준비되었음
    # 이제 이 스도쿠를 기초로 
    # 몇 가지 셔플 작업을 함
    # 첫째, 풀이가 가능한 스도쿠 데이터의 정사각 블록 행, 
    # 정사각 블록 열을 셔플해줌
    # 블록을 셔플하는 것은 풀이의 무결성을 해치지 않음
    def shuffle(self, num, type, direction=HORIZONTAL_DIRECTION):
        for i in range(num):
             # 셔플의 옵션이 블록이라면
            if type == BLOCK:
                # (행/열 방향이 선택된 후) 두 블록을 결정 
                V1, V2 = sample([0,1,2], 2)
                # 두 블록의 위치를 바꿈 (랜덤한 방향으로 결정)
                # print(i, "번 블록 셔플 후")
                self.swapSubBlock(V1, V2, swapdir=direction)
                # self.print()
            # 셔플의 옵션이 행이라면
            elif type == ROW:
                block_row_num = randint(0,2)
                V1, V2 = sample([0,1,2], 2)
                # 블록의 위치에 따라 행의 위치를 계산
                V1 = V1 + block_row_num * 3
                V2 = V2 + block_row_num * 3
                self.swapRow(V1, V2)
             # 셔플의 옵션이 열이라면
            elif type == COL:
                block_col_num = randint(0,2)
                V1, V2 = sample([0,1,2], 2)
                # 블록의 위치에 따라 행의 위치를 계산
                V1 = V1 + block_col_num * 3
                V2 = V2 + block_col_num * 3
                self.swapCol(V1, V2)               

        
    # 셔플이 완료된 풀이 데이터를 이용해서
    # 일부의 셀을 삭제하여 문제로 바꾼다 
    # del_size; 얼마나 지울 것인지에 따라 난이도가 올라간다 
    def delete(self, del_size=10): 
        if del_size >= self.size * self.size:
            del_size = self.size * self.size - 1
        # 유저가 클릭할 i, j 위치: user_places
        # 숫자 이미지가 고정되어 들어갈 i,j 위치: fixed_places 
        self.user_places = []
        self.fixed_places = []
        for i in range(self.size):
            for j in range(self.size):
                self.fixed_places.append((i,j))
                 
        del_count = 0
        while True:
            i, = sample(range(self.size), 1)
            j, = sample(range(self.size), 1)
            if self.grid[i][j] != NOT_FILLED:
                self.grid[i][j] = NOT_FILLED
                self.user_places.append((i,j))
                self.fixed_places.remove((i,j))
                del_count += 1
                if del_count == del_size:
                    break

                
    
    # 스도쿠가 모두 채워졌는지 검사한다
    def isAllFilled(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == NOT_FILLED:
                    return False
        return True
    
    
    # 2차원 리스트를 1차원으로 만든다
    def flatten2D(self, list2d):
        res = []
        for row in list2d:
            res.extend(row)
        return res
        
    
    
    # 스도쿠가 클리어되었는지 검사한다
    def isSolved(self):
        # 첫째로, 각 행을 살펴 숫자들이 유일한지 검사하여
        # 모든 행의 숫자가 각각 유일하다면 행조건 통과
        for i in range(self.size):
            row = self.getRow(i)
            #  각 행마다 똑같은 숫자가 2개 이상 있는지 검사
            dupli = [number for number in row if row.count(number) > 1]
            # set 연산자를 이용해서 겹치는 숫자 중 1개만 거름 [1, 2,2, 4,4,4] -> [1,2,4]
            dupli = list(set(dupli))
            # 만약 겹치는 숫자 1개라도 발견된다면, 클리어 안된 것
            if len(dupli) > 0:
                return False
        print("행 클리어 조건 통과!")
        
        # 둘째로, 각 열을 살펴 숫자들이 유일한지 검사하여
        # 모든 열의 숫자가 각각 유일하다면 열조건 통과
        for i in range(self.size):
            col = self.getCol(i)
            #  각 행마다 똑같은 숫자가 2개 이상 있는지 검사
            dupli = [number for number in col if col.count(number) > 1]
            # set 연산자를 이용해서 겹치는 숫자 중 1개만 거름 [1, 2,2, 4,4,4] -> [1,2,4]
            dupli = list(set(dupli))
            # 만약 겹치는 숫자 1개라도 발견된다면, 클리어 안된 것
            if len(dupli) > 0:
                return False
        print("열 클리어 조건 통과!")
        
        # 셋째로, 정사각 블록 9개를 검사하여
        # 각 블록 안의 숫자들이 유일한지 검사하여
        # 유일하다면 블록 조건 통과
        for y in range(3):
            for x in range(3):
                # 블록을 하나 가져온다
                sub_block = self.getSubBlock(x,y)
                # 블록을 2차원에서 1차원 리스트로 변환한다
                flat_list = self.flatten2D(sub_block)
                # 리스트 안에 똑같은 숫자가 2개 이상 있는지 검사
                dupli = [number for number in flat_list if flat_list.count(number) > 1]
                # set 연산자를 이용해서 겹치는 숫자 중 1개만 거름 [1, 2,2, 4,4,4] -> [1,2,4]
                dupli = list(set(dupli))
                # 만약 겹치는 숫자 1개라도 발견된다면, 클리어 안된 것
                if len(dupli) > 0:
                    return False
        print("블록 클리어 조건 통과!")
        return True
                
                
        
        
        
    
    # 스도쿠 문제 풀이 준비
    # 난이도는 1: 빈칸 하나만 있는 것
    # 난이도 최대: 모두 빈칸 81 
    def generate(self):
        # 스도쿠 초기화
        self.init_grid()
        print("스도쿠 그리드 지우기")
        self.print()
        # 스도쿠 한 블록만 채워서 준비
        print("스도쿠 블록 하나 랜덤하게 채우기")
        self.fillOneBlock()
        self.print()
        # 스도쿠 풀이
        print("스도쿠 솔루션 하나 만들기")
        self.solve()
        self.print()

        # 각각의 서브 정사각 블록 셔플
        self.shuffle(type=BLOCK, direction=HORIZONTAL_DIRECTION, num=1)
        self.print()

        # 각각의 서브 정사각 블록 내의 행 3개의 위치 셔플한다
        self.shuffle(type=ROW, num=100)
        print("행 셔플후")
        self.print()

        self.shuffle(type=COL, num=100)
        print("열 셔플후")
        self.print()
        
        # 셔플이 완료된 풀이 데이터를 이용해서
        # 일부의 셀을 삭제하여 문제로 바꾼다
        self.delete(del_size=self.difficulty)
        # print("일부 셀을 삭제 한 후")
        # self.print()


                    
        


    

 
        
        
