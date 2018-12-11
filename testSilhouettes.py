import sys
import scipy.misc
import numpy as np
from randomSphereVectors import *
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
import matplotlib.pyplot as plt

global file_name
global centers
global directions 
global iteration
# global variables
global xrot         # angle of rotation about x
global yrot         # angle of rotation about y
global ambient      # ambient colour
global lightpos     # light position


# Процедура инициализации
def init():
    global xrot         # angle of rotation about x
    global yrot         # angle of rotation about y
    global ambient      # ambient colour


    global centers
    global directions
    global iteration
       
    xrot = 0.0                          # angle of rotation about x
    yrot = 0.0                          # angle of rotation about y
    ambient = (1.0, 1.0, 1.0, 1.0)        # RGB + brightness
    eye = [0., 0., 0.] 
    center = centers[iteration]
    up = directions[iteration]
    lightpos = (-50*up[0], -50*up[1], -50*up[2])          # position on xyz
    #gluLookAt(eye[0] , eye[1], eye[2], center[0], center[1], center[2], up[0], up[1], up[2])

    #lightpos = (-50*up[0]*(-center[0] + eye[0]), -50*up[1]*(-center[1]+ eye[0]), -50*up[2]*(-center[2]+ eye[0]))          # Положение источника освещения по осям xyz


    glClearColor(1.0, 1.0, 1.0, 1.0)                # Gray color of thr background
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)                # The borders for painting
    
   
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient) # Model of light
    glEnable(GL_LIGHTING)                           # Turn on all the lights
    glEnable(GL_LIGHT0)                             # Turn on the concret light
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    


def draw():  
    global xrot         # Величина вращения по оси x
    global yrot         # Величина вращения по оси y
    global ambient      # Рассеянное освещение
    global greencolor   # Цвет елочных иголок
    global treecolor    # Цвет елочного ствола
    global lightpos     # Position of lights
    global filename
    global centers
    global directions
    global iteration
    global names


    for filename in names:    
        print(filename)
        verticies, surfaces = read_off(open(filename))#73
        eye = [0, 0, 0]
        for iteration in range(len(centers)):
            #glClear(GL_DEPTH_BUFFER_BIT)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            #
            center = centers[iteration]
            up = directions[iteration]
            
            glLoadIdentity()
            eye = [0., 0, 0.] 
            #center = [-.1, -0.1, -0.1]
            #up = [0.2, 0.2, 0.2]
            lightpos = (50*center[0], 50*center[1], 50*center[2])  
            gluPerspective(0, 0.2, 0. , 100 )
            gluLookAt(eye[0] , eye[1], eye[2], 20*center[0], 20*center[1], 20*center[2], up[0], up[1], up[2])
            #glPushMatrix()   
            glRotatef(xrot, 1.0, 0.0, 0.0)                              # turning around xrot
            glRotatef(yrot, 0.0, 1.0, 0.0)                              # turning around yrot
            #gluPerspective(0.0, 0.0, 0.01, 10)#gluOrtho2D(-5, 5, -5, 5, 0.1, 10)
            #glMatrixMode(GL_MODELVIEW)
            #glLoadIdentity()

            glLightfv(GL_LIGHT0, GL_POSITION, lightpos)     # where are the lights
            #glEnable(GL_POLYGON_OFFSET_FILL);
            #glPolygonOffset(1.0, 1.0);
            #glEnable(GL_CULL_FACE)
            #gluPerspective(0, 0.2, 0.1 , 10 )
            #glEnable(GL_CULL_FACE)
            #glCullFace(GL_FRONT)
            ##glClearDepth(0.0)
            ##GL_DEPTH_BIAS=0
            ##GL_DEPTH_BITS=24
            ##GL_DEPTH_CLEAR_VALUE=2147482496
            ##GL_DEPTH_FUNC=GL_LESS
            ##GL_DEPTH_RANGE={0, 1}
            ##GL_DEPTH_SCALE=1
            ##GL_DEPTH_TEST=True
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LESS)
            #glDepthFunc(GL_ALWAYS)
            #glDepthMask(GL_FALSE)
            glEnable(GL_NORMALIZE)
            #glDepthFunc(GL_NEVER)
            #glDisable(GL_CULL_FACE) 
            #glFrontFace(GL_CW)
            #glDepthMask(GL_TRUE)
            #glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH24_STENCIL8, 600, 600, 0, GL_DEPTH_STENCIL, 	       GL_UNSIGNED_INT_24_8, None)
            #glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_TEXTURE_2D, 2, 0);


            res = [0,0,0]
            for vert in verticies:
                res = sum(vert, res)
            res = div(res, len(verticies))
            for n_vert in range(len(verticies)):
                verticies[n_vert] = sum(verticies[n_vert], opp(res))
            #glBegin(GL_TRIANGLES)
            #glShadeModel(GL_FLAT)
            x = 0
            normals = []
            n = len(verticies)
            #line 5: 1, 5, 8(order like in surfaces)
            vertices_to_surfaces = []
            for i in range(n):
                vertices_to_surfaces.append([])
            for surface in surfaces:
                if len(surface) == 0:
                    #print(surface)
                    continue
                    print('2')
                x = x + 1
                u = [verticies[surface[1]][0]-verticies[surface[0]][0], verticies[surface[1]][1]-verticies[surface[0]][1], verticies[surface[1]][2]-verticies[surface[0]][2]]
                v = [verticies[surface[2]][0]-verticies[surface[0]][0], verticies[surface[2]][1]-verticies[surface[0]][1], verticies[surface[2]][2]-verticies[surface[0]][2]]
                normal= [u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1]-u[1]*v[0]]

                # une tentative a comprendre si dehors ou interieurs
                s = 0
                for i in range(3):
                    s = s+normal[i]*verticies[surface[0]][i]
                if True:
                    normals.append(normal)
                else:
                    normals.append([-normal[0], -normal[1], -normal[2]])
                    #print('inverse')
                for vertex in surface:
                    vertices_to_surfaces[vertex].append(x-1)  	
            x = 0
            vertex_normalized = []
            #normals for each vertice = average of all normals of the adjoint vertices
            for j in range(len(vertices_to_surfaces)):
                vertex_normalized.append([0, 0, 0])
                for z in range(len(vertices_to_surfaces[j])):
                    normal = normals[vertices_to_surfaces[j][z]]
                    vertex_normalized[j][0] = vertex_normalized[j][0] + normal[0]
                    vertex_normalized[j][1] = vertex_normalized[j][1] + normal[1]
                    vertex_normalized[j][2] = vertex_normalized[j][2] + normal[2]
                norm = np.sqrt(vertex_normalized[j][0]**2 + vertex_normalized[j][1]**2 + vertex_normalized[j][2]**2)
                for z in range(3):
                    vertex_normalized[j][z] = vertex_normalized[j][z]/norm

            x = 0
            for surface in surfaces:
                #print(surface)
                #glEnable(GL_DEPTH_TEST)
                #glDepthFunc(GL_LESS)
                glBegin(GL_TRIANGLE_FAN);
                x = x + 1
                for vertex in surface:
                    #TODO: something with colors, now it is too far from reality
                    l = sum(opp(verticies[vertex]), lightpos) #lighpos - vector to vertex = vector from vertex to lights
                    cos_theta = (vertex_normalized[vertex][0]*l[0] + vertex_normalized[vertex][1]*l[1] + vertex_normalized[vertex][2]*l[2])/(dist(vertex_normalized[vertex], [0.,0.,0.])*dist(l, [0.,0.,0.]))
                    #glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE, (1., 0., 1., 1) )
                    #glMaterialfv(GL_FRONT_AND_BACK,GL_SPECULAR, (1., 0., 1., 1) )
                    #print(x)
                    #glColor3f(x*1.0/1000,x*1.0/1000,0.0);           	
                    
                    #GL_FLAT
                    #print(vertex_normalized[vertex])
                    #print(cos_theta)
                    glNormal3fv(div(vertex_normalized[vertex],1./cos_theta))
                    glVertex3fv(verticies[vertex]) 
                    glColor3f(255.0,255.0,0.0)
                    
                glEnd() 
                
                
                    #glShadeModel(GL_SMOOTH)       	
            #glEnd()
            
            #glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);

    

            #glPopMatrix()                          
            #for i in range(len(centers)):
            #gluLookAt(eye[0] , eye[1], eye[2], center[0], center[1], center[2], up[0], up[1], up[2])
            #glEnable(GL_DEPTH_TEST);
            #glDepthFunc(GL_LESS);
            glutSwapBuffers()   
            
            #glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)       
            x, y, width, height = glGetIntegerv(GL_VIEWPORT)
            print("Screenshot viewport:", x, y, width, height)
            #glPixelStorei(GL_PACK_ALIGNMENT, 1)

            data = glReadPixels(x, y, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    
            image_array = np.fromstring(data, np.uint8)
            image = image_array.reshape(width, height, 3)
            scipy.misc.imsave('images/' + filename[7:-4] + '_outfile_' + str(iteration) + '.jpg', image)
    glutDestroyWindow(1)
    if True:
        pass
        #-------------------------------

        #glPushMatrix()                                              # Сохраняем текущее положение "камеры"
        #glRotatef(xrot, 1.0, 0.0, 0.0)                              # Вращаем по оси X на величину xrot
        #glRotatef(yrot, 0.0, 1.0, 0.0)                              # Вращаем по оси Y на величину yrot
        """
        # Рисуем ствол елки
        # Устанавливаем материал: рисовать с 2 сторон, рассеянное освещение, коричневый цвет
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, treecolor)
        glTranslatef(0.0, 0.0, -0.7)                                # Сдвинемся по оси Z на -0.7
        # Рисуем цилиндр с радиусом 0.1, высотой 0.2
        # Последние два числа определяют количество полигонов
        glutSolidCylinder(0.1, 0.2, 20, 20)
        # Рисуем ветки елки
        # Устанавливаем материал: рисовать с 2 сторон, рассеянное освещение, зеленый цвет
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, greencolor)
        glTranslatef(0.0, 0.0, 0.2)                                 # Сдвинемся по оси Z на 0.2
        # Рисуем нижние ветки (конус) с радиусом 0.5, высотой 0.5
        # Последние два числа определяют количество полигонов
        glutSolidCone(0.5, 0.5, 20, 20)
        glTranslatef(0.0, 0.0, 0.3)                                 # Сдвинемся по оси Z на -0.3
        glutSolidCone(0.4, 0.4, 20, 20)                             # Конус с радиусом 0.4, высотой 0.4
        glTranslatef(0.0, 0.0, 0.3)                                 # Сдвинемся по оси Z на -0.3
        glutSolidCone(0.3, 0.3, 20, 20)                             # Конус с радиусом 0.3, высотой 0.3
    
        glPopMatrix()                                               # Возвращаем сохраненное положение "камеры"
        glutSwapBuffers()                                           # Выводим все нарисованное в памяти на экран
        """

# Процедура обработки специальных клавиш
def specialkeys(key, x, y):
    global xrot
    global yrot
    # Обработчики для клавиш со стрелками
    if key == GLUT_KEY_UP:      # Клавиша вверх
        xrot -= 2.0             # Уменьшаем угол вращения по оси X
    if key == GLUT_KEY_DOWN:    # Клавиша вниз
        xrot += 2.0             # Увеличиваем угол вращения по оси X
    if key == GLUT_KEY_LEFT:    # Клавиша влево
        yrot -= 2.0             # Уменьшаем угол вращения по оси Y
    if key == GLUT_KEY_RIGHT:   # Клавиша вправо
        yrot += 2.0             # Увеличиваем угол вращения по оси Y

    glutPostRedisplay()         # Вызываем процедуру перерисовки

def runAll(model_name, centers=0, directions=0):
	print(model_name)
	global filename
	filename = model_name
	# Execution starts
	# double buffer and RGB
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

	glutInitWindowSize(600, 600)
	# initial position on the screen
	glutInitWindowPosition(150, 150)
	
	# Initialization OpenGl
	glutInit(sys.argv)
	
	glutCreateWindow(b"Happy project!")

	# Function for drawing
	glutDisplayFunc(draw)
	
	glutSpecialFunc(specialkeys)

	init()
	# Main cycle
	glutMainLoop()

def execute(fname, centers0, directions0, iteration0, names0):
	global filename
	global centers
	global directions
	global iteration
	global names
	filename = fname
	centers = centers0
	directions = directions0
	iteration = iteration0
	names = names0
	runAll(fname)

#centers0, directions0 = determineViewDirections(d = 10)
#iteration0 = 4
#fname = "models/m73.off"
#execute(fname, centers0, directions0, iteration0)
