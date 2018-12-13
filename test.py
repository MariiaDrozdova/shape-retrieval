from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from randomSphereVectors import *
import scipy.misc
import sys
import numpy as np
import os

global centers0
global directions0
global iteration
global filename
global d

def read_off(file):
    if 'OFF' != file.readline().strip():
        raise('Not a valid OFF header')
    n_verts, n_faces, n_dontknow = tuple([int(s) for s in file.readline().strip().split(' ')])
    n_verts = n_verts
    n_faces = n_faces
    verts = []
    faces = []
    for i_vert in range(n_verts):
        verts.append([])
        for s in file.readline().strip().split(' '):
            if len(s) > 0:
                verts[i_vert].append(float(s))
    for i_face in range(n_faces):
        faces.append([])
        try:
            for s in file.readline().strip().split(' ')[1:]:
                if len(s) > 0:
                    faces[i_face].append(int(s))
        except:
            for s in file.readline().strip().split('\t')[1:]:
                if len(s) > 0:
                    faces[i_face].append(int(s))
    return verts, faces

def sum_vec(p1, p2):
	assert(len(p1)==len(p2))
	res = [0]*len(p1)
	for i in range(len(p1)):
		res[i] = p1[i] + p2[i]
	return res

def opp(p1):
	res = [0]*len(p1)
	for i in range(len(p1)):
		res[i] = -p1[i]
	return res

def div(p1, a):
	res = [0]*len(p1)
	for i in range(len(p1)):
		res[i] = p1[i]/a
	return res

def init():
    global centers0
    global directions0
    global iteration
    # clear color and set background color 
    center = centers0[iteration]
    up = directions0[iteration]
    lightpos = (500*center[0], 500*center[1], 500*center[2]) 

    glClearColor(1.0, 1.0, 1.0, 1.0)  

    # Model of light
    ambient = (1.0, 1.0, 1.0, 1.0) 
    diffuse = (1.0, 1.0, 1.0, 1.0)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_POSITION,lightpos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glEnable(GL_LIGHTING)     
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)



def plotfunc():
    global centers0
    global directions0
    global iteration
    global filename

    eye = centers0[iteration]
    eyesight = [0., 0., 0.] 
    direction = directions0[iteration]
    lightpos = (50*eye[0], 50*eye[1], 50*eye[2]) 
    #lightpos = (50*center[0], 50*center[1], 50*center[2])  
    

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) 
    glLoadIdentity()
    gluLookAt(eyesight[0],eyesight[1],eyesight[2],eye[0],eye[1],eye[2],direction[0],direction[1],direction[2])       
    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)     # where are the lights
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    #glClearDepth(0.8)
    glEnable(GL_NORMALIZE)
    glFrontFace(GL_CW)

    verts, faces = read_off(open(filename))
    verts = centraliseVertices(verts)
    verts_normals = verticesNormals(verts,faces)
    
    glPointSize(1.0)                    # 设置点大小
    glColor3f(1.0, 0.0, 0.0)            # 设置点颜色
    #glBegin(GL_POINTS)                  # 此次开始，设置此次画的几何图形
    #for v in verts:
     #   glVertex3f(v[0],v[1],v[2])
        #glVertex3f(v[0]*,[1],v[2])
    #glEnd() 

    for f in faces:
        glBegin(GL_TRIANGLE_FAN) 
        for i in range(3):
            vv = verts[f[i]]  
            l = sum(opp(vv),lightpos) 
            cos_theta = (verts_normals[f[i]][0] * l[0] + verts_normals[f[i]][1] * l[1] + verts_normals[f[i]][2] * l[2])/(dist(verts_normals[f[i]], [0.,0.,0.])*dist(l, [0.,0.,0.]))
            glNormal3fv(div(verts_normals[f[i]],1./cos_theta))
            glVertex3fv(vv) 
            glColor3f(255.0,255.0,0.0)
        glEnd() 
    glFlush()  

    x, y, width, height = glGetIntegerv(GL_VIEWPORT)
    print("Screenshot viewport:", x, y, width, height)
    data = glReadPixels(x, y, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image_array = np.fromstring(data, np.uint8)
    image = image_array.reshape(width, height, 3)
    #scipy.misc.imsave('../images/' + filename[7:-4] + '_outfile_' + str(iteration) + '.jpg', image)                        
 
def specialkeys(key,x,y):
    global iteration
    global d
    if key == GLUT_KEY_UP:      
        if iteration < d-1:
            iteration  = iteration +1
        

    glutPostRedisplay()         # Вызываем процедуру перерисовки


def centraliseVertices(verticies):
    # the center of the vertices are the origin of the coordinates
    res = [0,0,0]
    for vert in verticies:
        res = sum(vert, res)
    res = div(res, len(verticies))
    for n_vert in range(len(verticies)):
        verticies[n_vert] = sum(verticies[n_vert], opp(res))
    return verticies

def verticesNormals(verticies,surfaces):
    # return normalized vertice normal
    face_normals = []
    vertex_normalized = []
    n = len(verticies)
    face_of_vertices = []
    for i in range(n):
        face_of_vertices.append([])
    # compute face normal
    x = 0
    for surface in surfaces:
        if len(surface) == 0:
            continue
        u = [verticies[surface[1]][0]-verticies[surface[0]][0], verticies[surface[1]][1]-verticies[surface[0]][1], verticies[surface[1]][2]-verticies[surface[0]][2]]
        v = [verticies[surface[2]][0]-verticies[surface[0]][0], verticies[surface[2]][1]-verticies[surface[0]][1], verticies[surface[2]][2]-verticies[surface[0]][2]]
        normal= [u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
         # une tentative a comprendre si dehors ou interieurs
        face_normals.append(normal)
        for vertex in surface:
            face_of_vertices[vertex].append(x)  
        x = x+1
    # compute vertice normal 
    x = 0
    #normals for each vertice = average of all normals of the adjoint vertices
    for j in range(len(face_of_vertices)):
        vertex_normalized.append([0, 0, 0])
        for z in range(len(face_of_vertices[j])):
            normal = face_normals[face_of_vertices[j][z]]
            vertex_normalized[j][0] = vertex_normalized[j][0] + normal[0]
            vertex_normalized[j][1] = vertex_normalized[j][1] + normal[1]
            vertex_normalized[j][2] = vertex_normalized[j][2] + normal[2]
        norm = np.sqrt(vertex_normalized[j][0]**2 + vertex_normalized[j][1]**2 + vertex_normalized[j][2]**2)
        for z in range(3):
            vertex_normalized[j][z] = vertex_normalized[j][z]/norm
    return vertex_normalized

if __name__ == '__main__':
    global centers0
    global directions0
    global iteration
    global filename 
    global d
    filename = "../models/m913.off"
    d = 20
    centers0, directions0 = determineViewDirections(d)
    iteration = 0

    glutInit(sys.argv)  #初始化
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH) #设置显示模式
    glutInitWindowPosition(100, 100)    #窗口打开的位置，左上角坐标在屏幕坐标
    glutInitWindowSize(600, 600)        #窗口大小
    glutCreateWindow(b"Function Plotter")   #窗口名字，二进制
    init()
    glutDisplayFunc(plotfunc)           #设置当前窗口的显示回调
    glutSpecialFunc(specialkeys)
    glClearColor(1.0, 1.0, 1.0, 1.0)    # 设置背景颜色
   
    glutMainLoop()                      # 启动循环

