import time, random, statistics
import matplotlib.pyplot as plt

#Константы
GOAL = 50000 # стремимся к весу крысы
NUM_RATS = 200 # начальное кол-во крыс
RETAIN_RATS = 20 # кол-во крыс проходящих отбор
INITIAL_MIN_WT = 200 # начальный минимальный вес крысы
INITIAL_MAX_WT = 600 # начальный максимальный вес крысы
INITIAL_MODE_WT = 300 # начальный средний вес крысы
MUTATE_ODDS = 0.3 # Вероятность появления мутации
MUTATE_MIN = 0.5 # Скаляр на весе крысы с наименее благоприятной мутацией
MUTATE_MAX = 1.2 # Скаляр на весе крысы с наиболее благоприятной мутацией
LITTER_SIZE = 8 # Число детенышей на 1 спаривание пары крыс
LITTERS_PER_YEAR = 10 # Количество спариваний на пару в год
GENERATION_LIMIT = 500 # Поколенческое отсечение для останова программы размножения

if NUM_RATS % 2 != 0:
    NUM_RATS += 1

# генерация начальной популяции крыс
def populate(num_rats, min_wt, max_wt, mode_wt): 
    return [int(random.triangular(min_wt, max_wt, mode_wt)) for i in range(num_rats)]

# определение процентной доли достижения результата по весу
def fitness(population, goal): 
    ave = statistics.mean(population)
    return ave/goal

'''Далее идёт функция для выбора крыс для скрещивания, отсеивание непрошедших порог
Принцип: сортируем массив по возрастанию, первая половина женский пол, вторая мужской, 
так как м всегда крупнее ж (основа).
Возвращаем to_retain каждого типа крыс с каждого конца подмасива - 
получили по to_retain самых сильных крыс обоев полов данного поколения
'''
def select(population, to_retain): 
    sorted_population = sorted(population)
    to_retain_by_sex = to_retain//2
    members_per_sex = len(sorted_population)//2
    females = sorted_population[:members_per_sex]
    males = sorted_population[members_per_sex:]
    selected_females = females[-to_retain_by_sex:]
    selected_males = males[-to_retain_by_sex:]
    
    return selected_males, selected_females

# Создаем детей весом больше материнского меньше мужского
def breed(males,females, litter_size):
    random.shuffle(males)
    random.shuffle(females)
    children = []
    
    for male, female in zip(males, females):
        for child in range(litter_size):
            child = random.randint(female,male)
            children.append(child)
            
    return children

# Алгоритм возможной мутации некоторых крыс сильно в худшую или в лучшую сторону
def mutate(children, mutate_odds, mutate_min, mutate_max):
    for index, rat in enumerate(children):
        if mutate_odds >= random.random(): # проверка на вероятность появления мутации
            children[index] = round(rat*random.uniform(mutate_min,mutate_max))
            
    return children

def add_line_to_file(filename, years, parameter):
    with open(filename, 'a') as file:
        line = f"{years} {parameter}\n"
        file.write(line)
        
def main():
    fit = []
    generations = 0
    parents = populate(NUM_RATS, INITIAL_MIN_WT, INITIAL_MAX_WT, INITIAL_MODE_WT)
    print("Первоначальные веса крыс = {}".format(parents))
    
    popl_fitness = fitness(parents,GOAL)
    print("Первоначальная приспособленность популяции = {}".format(popl_fitness))
    print("Остовляемое число = {}".format(NUM_RATS))
    
    ave_wt = []
    
    while popl_fitness < 1 and generations < GENERATION_LIMIT:
        selected_males, selected_females = select(parents, NUM_RATS)
        children = breed(selected_males,selected_females, LITTER_SIZE)
        children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)
        parents = selected_males + selected_females + children
        popl_fitness = fitness(parents, GOAL)
        fit.append(popl_fitness)
        #print("Приспособленность поколения {} = {:.4f}".format(generations,popl_fitness))
        ave_wt.append(int(statistics.mean(parents)))
        generations += 1
        
    print("Конечная приспособленность популяции = {}".format(popl_fitness))
        
    print("Средний вес на поколение = {}".format(ave_wt))
    print("\nЧисло поколений = {}".format(generations))
    print("Число лет = {}".format(int(generations/LITTERS_PER_YEAR)))
    
    gen = [x for x in range(generations)]
    
    #графики
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(6, 12))
    
    #1
    axes[0].plot(fit, gen, color='gray', linewidth=2)
    axes[0].set_xlabel('Приспособленность')
    axes[0].set_ylabel('Поколение')
    axes[0].set_title('График приспособленности поколений')
    
    #2
    axes[1].plot(ave_wt, gen, color='gray', linewidth=2)
    axes[1].set_xlabel('Средний вес')
    axes[1].set_ylabel('Поколение')
    axes[1].set_title('График среднего веса покалений')
    
    # Отображение графиков
    plt.tight_layout()
    plt.show()
    return generations

    
    
if __name__ == '__main__':
    #generations = []
    #generations.append(main())

    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
        
    print("\nВремя выполнения этой программы составило {:.2f} секунд.".format(duration))   
         
    #generations = statistics.mean(generations)  
    #add_line_to_file(r'F:\Code\Python\Проекты\Genetic Algorithm SuperRats\mutate_odds.txt', int(generations/LITTERS_PER_YEAR),MUTATE_ODDS)
