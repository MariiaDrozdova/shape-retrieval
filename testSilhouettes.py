import sys
import scipy.misc
import numpy as np
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
import matplotlib.pyplot as plt


def read_off(file):
    if 'OFF' != file.readline().strip():
        raise('Not a valid OFF header')
    n_verts, n_faces, n_dontknow = tuple([int(s) for s in file.readline().strip().split(' ')])
    verts = [[float(s) for s in file.readline().strip().split(' ')] for i_vert in range(n_verts)]
    faces = [[int(s) for s in file.readline().strip().split(' ')][1:] for i_face in range(n_faces)]
    return verts, faces

def init():

    xrot = 0.0                          # Величина вращения по оси x = 0
    yrot = 0.0                          # Величина вращения по оси y = 0
    ambient = (1.0, 1.0, 1.0, 1)        # Первые три числа - цвет в формате RGB, а последнее - яркость
    greencolor = (0.2, 0.8, 0.0, 0.8)   # Зеленый цвет для иголок
    treecolor = (0.9, 0.6, 0.3, 0.8)    # Коричневый цвет для ствола
    lightpos = (1.0, 1.0, 1.0)          # Положение источника освещения по осям xyz

    glClearColor(1.0, 1.0, 1.0, 1.0)                # Серый цвет для первоначальной закраски
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)                # Определяем границы рисования по горизонтали и вертикали
    #glRotatef(-90, 1.0, 0.0, 0.0)                   # Сместимся по оси Х на 90 градусов
    gluLookAt(0.0 , 0.0, 0.0 , 50.0 ,  5.0,  50.0 ,  5.0,  5.0 ,5.0 )

   
    #glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient) # Определяем текущую модель освещения
    #glEnable(GL_LIGHTING)                           # Включаем освещение
    #glEnable(GL_LIGHT0)                             # Включаем один источник света
    #glLightfv(GL_LIGHT0, GL_POSITION, lightpos)     # Определяем положение источника света

def read3D(verticies,surfaces):
    
    glBegin(GL_TRIANGLES)
    x = 0
    for surface in surfaces:
        x = x + 1
        for vertex in surface:
            	#glColor3ub( 0, 200, 0)
            	#TODO: something with colors, now it is too far from reality
            	glColor3ub( 0, x%155+100, 0)
            	glVertex3fv(verticies[vertex])
            	
            	
    glEnd()
    x, y, width, height = glGetIntegerv(GL_VIEWPORT)
    print("Screenshot viewport:", x, y, width, height)
    glPixelStorei(GL_PACK_ALIGNMENT, 1)

    data = glReadPixels(x, y, width, height, GL_RGB, GL_UNSIGNED_BYTE)

    image_array = np.fromstring(data, np.uint8)
    image = image_array.reshape(width, height, 3)
    scipy.misc.imsave('outfile.jpg', image)


# Процедура перерисовки
def draw():
    global xrot
    global yrot
    global lightpos
    global greencolor
    global treecolor

    glClear(GL_COLOR_BUFFER_BIT)                                # Очищаем экран и заливаем серым цветом
    glPushMatrix()                                              # Сохраняем текущее положение "камеры"
    verts, faces = read_off(open("models/m73.off"))
    read3D(verts,faces)
    

    glPopMatrix()                                               # Возвращаем сохраненное положение "камеры"
    glutSwapBuffers()                                           # Выводим все нарисованное в памяти на экран


def runAll():
	# Здесь начинается выполнение программы
	# Использовать двойную буферизацию и цвета в формате RGB (Красный, Зеленый, Синий)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	# Указываем начальный размер окна (ширина, высота)
	glutInitWindowSize(600, 600)
	# Указываем начальное положение окна относительно левого верхнего угла экрана
	glutInitWindowPosition(150, 150)
	# Инициализация OpenGl
	glutInit(sys.argv)
	glutCreateWindow(b"Happy project!")
	# Определяем процедуру, отвечающую за перерисовку
	glutDisplayFunc(draw)
	# Вызываем нашу функцию инициализации
	init()
	# Запускаем основной цикл
	glutMainLoop()
runAll()
