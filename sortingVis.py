import random
import pygame
import math
import asyncio
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BLUE = 0, 0, 255
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 25)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)
    
    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending, speed, time = 0):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLUE)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))
    
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))

    sorting = draw_info.FONT.render("I - InsertionSort | B - BubbleSort | S - Selection Sort | M - Merge Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

    speedometer = draw_info.FONT.render("+ - Speed Up | '-' - Speed Down | Current Speed: " + str(speed), 1, draw_info.BLACK)
    draw_info.window.blit(speedometer, (draw_info.width/2 - sorting.get_width()/2, 105))

    timer = draw_info.FONT.render("Time elapsed: " + str(time/1000.0) + " seconds", 1, draw_info.BLACK)
    draw_info.window.blit(timer, (draw_info.width/2 - sorting.get_width()/2, 135))

    draw_list(draw_info)
    pygame.display.update()
    
def draw_list(draw_info, color_positions={}, clear_bg = False):
    lst = draw_info.lst
        
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    
    return lst
    
def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True
    
    return lst

def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break
            
            lst[i] = lst[i - 1]
            i -= 1
            lst[i] = current
            draw_list(draw_info, {i: draw_info.GREEN, i - 1: draw_info.RED}, True)
            yield True
        
    return lst

def selection_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst)):
        current = i
        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[current] and ascending) or (lst[j] > lst[current] and not ascending):
                current = j
            draw_list(draw_info, {i: draw_info.GREEN, current: draw_info.BLUE, j: draw_info.RED}, True)
            yield True
        lst[i], lst[current] = lst[current], lst[i]

    return lst

def merge(draw_info, lst, left_start, left_end, right_start, right_end, ascending):
    i = left_start
    j = right_start
    temp = []
    pygame.event.pump()
    if ascending:
        while i <= left_end and j <= right_end:
            draw_list(draw_info, {i: draw_info.RED, j: draw_info.RED}, True)
            yield True
            draw_list(draw_info, {i: draw_info.BLUE, j: draw_info.BLUE}, True)
            yield True
            if lst[i] < lst[j]:
                temp.append(lst[i])
                i += 1
            else:
                temp.append(lst[j])
                j+= 1
        while i <= left_end:
            draw_list(draw_info, {i: draw_info.RED}, True)
            yield True
            draw_list(draw_info, {i: draw_info.BLUE}, True)
            yield True
            temp.append(lst[i])
            i += 1
        while j <= right_end:
            draw_list(draw_info, {i: draw_info.RED}, True)
            yield True
            draw_list(draw_info, {i: draw_info.BLUE}, True)
            yield True
            temp.append(lst[j])
            j += 1
    else:
        while i <= left_end and j <= right_end:
            draw_list(draw_info, {i: draw_info.RED, j: draw_info.RED}, True)
            yield True
            draw_list(draw_info, {i: draw_info.BLUE, j: draw_info.BLUE}, True)
            yield True
            if lst[i] > lst[j]:
                temp.append(lst[i])
                i += 1
            else:
                temp.append(lst[j])
                j+= 1
        while i <= left_end:
            draw_list(draw_info, {i: draw_info.RED}, True)
            yield True
            draw_list(draw_info, {i: draw_info.BLUE}, True)
            yield True
            temp.append(lst[i])
            i += 1
        while j <= right_end:
            draw_list(draw_info, {i: draw_info.RED}, True)
            yield True
            draw_list(draw_info, {i: draw_info.BLUE}, True)
            yield True
            temp.append(lst[j])
            j += 1
    j = 0
    for i in range(left_start, right_end + 1):
        pygame.event.pump()
        lst[i] = temp[j]
        j += 1
        draw_list(draw_info, {i: draw_info.GREEN}, True)
        yield True

def merge_sort(draw_info, lst, l, r, ascending = True):
    mid = (l + r) // 2
    if l < r:   
        yield from merge_sort(draw_info, lst, l, mid, ascending)    
        yield from merge_sort(draw_info, lst, mid + 1, r, ascending)
        yield from merge(draw_info, lst, l, mid, mid + 1, r, ascending)

    yield True
    return


        

def main():
    run = True
    clock = pygame.time.Clock()
    current_ticks = 0
    sort_ticks = 0

    n = 50
    min_val = 0
    max_val = 100
    speed = 60

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        if sorting:
            clock.tick(speed)
            sort_ticks = pygame.time.get_ticks() - current_ticks
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            clock.tick(60)
            draw(draw_info, sorting_algo_name, ascending, speed, sort_ticks)
            current_ticks = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type != pygame.KEYDOWN:
                continue
            
            if event.key == pygame.K_r:
                clock.tick(60)
                sorting = False
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
            elif sorting:
                continue
            elif event.key == pygame.K_SPACE:
                sorting = True
                if(sorting_algorithm == merge_sort):
                    sorting_algorithm_generator = sorting_algorithm(draw_info, draw_info.lst, 0, len(draw_info.lst) - 1, ascending)
                else:
                    sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a:
                ascending = True
            elif event.key == pygame.K_d:
                ascending = False
            elif event.key == pygame.K_i:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_s:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
            elif event.key == pygame.K_m:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"
            elif pygame.key.get_pressed()[pygame.K_LSHIFT or pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_EQUALS]:
                if speed >= 190:
                    speed = 200
                elif speed <= 9:
                    speed = 10
                else:
                    speed += 10
            elif event.key == pygame.K_MINUS:
                if speed <= 10:
                    speed = 1
                else:
                    speed -= 10

                        

    
    pygame.quit()

if __name__ == "__main__":
    #asyncio.run(main())
    main()



