import pyautogui
from time import sleep

pyautogui.FAILSAFE = True

#Open Website + Adjust
pyautogui.hotkey('win', 'r')
pyautogui.typewrite('https://solvable-sheep-game.streakingman.com/')
pyautogui.press('enter')
sleep(1)
pyautogui.click(1750, 110)
sleep(1)
pyautogui.scroll(-40)
sleep(1)

#Initialize
pics = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png']
all_cnt = 0

#find the duplicate points
def same(i, j):
    xi, yi = i
    xj, yj = j
    if abs(xi-xj)**2+abs(yi-yj)**2<50**2:
        return True
    return False

#find all the corresponding points
def location(index):
    locs = []
    cur = pyautogui.locateCenterOnScreen(pics[index], region=(675, 125, 600, 700), confidence=0.92)
    if cur:
        locs.append(cur)
        for i in pyautogui.locateAllOnScreen(pics[index], region=(675, 125, 600, 700), confidence=0.92):
            center = pyautogui.center(i)
            diff = True
            for j in locs:
                if same(center, j):
                    diff = False
            if diff == True:
                locs.append(center)
        return locs
    return None

#Main 
while all_cnt<1000:
    nums = []
    maxn = 0
    for i in range(10):
        if location(i):
            nums.append(len(location(i)))
            if len(location(i))>maxn:
                maxn = len(location(i))
        else:
            nums.append(0)
           
    print(nums) #point on screen of current
    
    if maxn>=3:
        for i in range(10):
            sleep(0.1)
            if nums[i]>=3:
                cnt = 0
                while cnt!=3:
                    sleep(0.1)
                    center = pyautogui.locateCenterOnScreen(pics[i], region=(675, 125, 600, 700), confidence=0.92)
                    pyautogui.click(center)
                    cnt+=1
    else:
        sleep(0.1) 
        pyautogui.click(1015, 987)
        print("shuffle")
        
        
        