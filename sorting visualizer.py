# This Sorting Visualizer will perform linear sorting algorithms (Insertion Sort and Bubble Sort) using Pygame framework.

import pygame
import random
import math
pygame.init()

class DrawInformation:
    #These are in rgb with highest value of 255.
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    REGULAR_FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    SIDE_PAD = 100
    TOP_PAD = 150


    #Inititalizing.
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))  #setting up a screen where we'll draw everything out.
        pygame.display.set_caption("Sorting Visualization")  #Setting a caption for the screen.
        self.set_list(lst)  #Initializing the list that we need to sort to fit the window.

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst) 
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))  #Width of each block. We round of the value because we can't draw fractional amount.
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2   #It will decide from where the blocks starts and end.


def draw(draw_info, algo_name, ascending):  #We are first filling the screen with the color to get rid of any previous drawing(overiding the screen) then draw, 
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)   #update it, clear everything, redraw and continue.

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

    controls = draw_info.REGULAR_FONT.render("R - Reset | SPACE - Start Sorting | A- Ascending | D- Descending ", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 55))  #This will display the text at the center top of the screen.

    sorting = draw_info.REGULAR_FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 85))  

    draw_list(draw_info)
    pygame.display.update()  #It will update the display and render it.


def draw_list(draw_info, color_positions = {}, clear_bg = False):
    lst = draw_info.lst
    
    if clear_bg:  #Clearing out the background after each sorting step to make a moving effect.
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)


    for idx, val in enumerate(lst):
        x_axis = draw_info.start_x + idx * draw_info.block_width
        y_axis = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[idx % 3]  #Every 3 consecutive blocks will have 3 differents shades of grey and after that it repeats.

        if idx in color_positions:
            color = color_positions[idx]

        pygame.draw.rect(draw_info.window, color, (x_axis, y_axis, draw_info.block_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val): #This will generate a list with random values ranging between max and min value.
    lst = []

    for idx in range(n):
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
                yield True  #It will store the current state of the function when paused and will resume from the last yield. 
    
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
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst


def main():  #This will render the screen where we set up the event loop which will enable us to press button, click the "X" button etc.
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None   #This will actually generate/perform the sorting algorithm.

    while run:  #We need the loop in pygame to make the event running otherwise it will run once and then terminate.
        clock.tick(40)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():  #This will return a list of events that have occured since the last loop.
            if event.type == pygame.QUIT:  #This means clicking the red "X" at the top right corner of the window.
                run = False

            if event.type != pygame.KEYDOWN:
                continue
            
            if event.key == pygame.K_r:  #If we hit the "r" button the list will be reset.
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list((lst))
                sorting = False

            elif event.key == pygame.K_SPACE and sorting == False:  #When we hit "space" it will start sorting.
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:  #When we hit "a" it will start sorting in ascending order.
                ascending = True

            elif event.key == pygame.K_d and not sorting:  #When we hit "d" it will start sorting in descending order.
                ascending = False

            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            
            #elif event.key == pygame.K_m and not sorting:
              #  sorting_algorithm = merge_sort
             #   sorting_algo_name = "Merge Sort"

           # elif event.key == pygame.K_q and not sorting:
            #    sorting_algorithm = quick_sort
           #     sorting_algo_name = "Quick Sort"
            
    pygame.quit()


if __name__ == "__main__":  #This will make sure that we are actually running this module by clicking the run button or running it directly.
    main()
