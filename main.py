import sys, pygame, socket
import os
import server

def sendPoint(s,point):
    """s = socket.socket()
    host = '192.168.1.3'
    port = 1234
    s.connect((host,port))"""
    s.send(point.encode('utf-8'))

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
exitMsg = "GO"
green = 0, 255, 0
white = 255, 255, 255
x_dim = 0
y_dim = 0
x_start = 100
y_start = 50
interval = 50
x_dim = ((width-(2*x_start))/interval)-2
y_dim = ((height-(2*y_start))/interval)-2
#ball = {'x' : x_start+((x_dim+2)/2)*interval, 'y' : y_start+((y_dim+2)/2)*interval}
line_surface = pygame.Surface(size, flags=pygame.SRCALPHA)
line_surface.fill((0,0,0,0))
points = []
x_count = 0
x = x_start
while x <= width-x_start:
    points.append([])
    y = y_start
    while y <= height-y_start:
        points[x_count].append((x,y))
        y += interval
    x += interval
    x_count+=1
ball = {'x' : 6, 'y' : 5}
lines = []
visited = []
for x in range(points.__len__()):
    for y in range(points[x].__len__()):
        if (x == 0 or y == 0) and y != 5:
            visited.append((x,y))
        if (x == points.__len__() or y == points[x].__len__()) and y!=5 :
            visited.append(x,y)
for y in range(points[0].__len__()):
    if y < 4 and y > 6 and y < points[x].__len__():
        lines.append([(0,y),(0,y+1)])
for y in range(points[-1].__len__()):
    if y < 4 and y > 6 and y < points[x].__len__():
        lines.append([(0,y),(0,y+1)])
for x in range(points.__len__()):
    lines.append([(x,points[x][0]),x+1,points[x][0]])
    lines.append([(x,points[x][-1]),x+1,points[x][-1]])
visited.append((ball['x'],ball['y']))
print visited[0][0]
#server.connectToServer('192.188.1.3')
s = socket.socket()
host = '192.168.1.3'
port = 1234
s.connect((host,port))
move = 0
side = 0 #lewa strona, domyslnie
msg = s.recv(2048)
if msg == 'ST1':
    move = 1
    side = 1 #prawa strona
while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and move!=0:
            if event.key == pygame.K_KP4 or event.key == pygame.K_a :
                if ball['x'] > 0 and [(ball['x'],ball['y']),(ball['x']-1,ball['y'])] not in lines:
                    pygame.draw.line(line_surface, white, (points[ball['x']][ball['y']]), (points[ball['x']-1][ball['y']]), 2)
                    lines.append([(ball['x'],ball['y']),(ball['x']-1,ball['y'])])
                    ball['x'] -= 1
                    if (ball['x'], ball['y']) not in visited:
                        visited.append(ball['x'],ball['y'])
                    sendPoint(s,str(ball['x'])+';'+str(ball['y']))
                elif ball['y'] == 5 and [(ball['x'],ball['y']),(ball['x']-1,ball['y'])] not in lines:
                    if side == 1:
                        print "Wygrana!"
                        server.sendPoint(s,"W1")
                    else:
                        print "Przegrana."
                        server.sendPoint(s,"W0")
                    pygame.quit()
                    sys.exit()
            if event.key == pygame.K_KP6 or event.key == pygame.K_d:
                if ball['x'] < points.__len__()-1 and [(ball['x'],ball['y']),(ball['x']+1,ball['y'])] not in lines:
                    pygame.draw.line(line_surface, white, (points[ball['x']][ball['y']]), (points[ball['x']+1][ball['y']]), 2)
                    lines.append([(ball['x'],ball['y']),(ball['x']+1,ball['y'])])
                    ball['x'] += 1
                    server.sendPoint(s,str(ball['x'])+';'+str(ball['y']))
                elif ball['y'] == 5:
                    if side == 1:
                        print "Przegrana."
                        server.sendPoint(s,"W1")
                    else:
                        print "Wygrana!"
                        server.sendPoint(s,"W0")
                    pygame.quit()
                    sys.exit()
            if event.key == pygame.K_KP8 or event.key == pygame.K_w:
                if ball['y'] > 0 and [(ball['x'],ball['y']),(ball['x'],ball['y']-1)] not in lines:
                    pygame.draw.line(line_surface, white, (points[ball['x']][ball['y']]), (points[ball['x']][ball['y']-1]), 2)
                    lines.append([(ball['x'],ball['y']),(ball['x'],ball['y']-1)])
                    ball['y'] -= 1
                    server.sendPoint(s,str(ball['x'])+';'+str(ball['y']))

            if event.key == pygame.K_KP2 or event.key == pygame.K_x:
                if ball['y'] < points[0].__len__()-1 and [(ball['x'],ball['y']),(ball['x'],ball['y']+1)] not in lines:
                    pygame.draw.line(line_surface, white, (points[ball['x']][ball['y']]), (points[ball['x']][ball['y']+1]), 2)
                    lines.append([(ball['x'],ball['y']),(ball['x'],ball['y']+1)])
                    ball['y'] += 1
                    server.sendPoint(s,str(ball['x'])+';'+str(ball['y']))

            if event.key == pygame.K_KP7 or event.key == pygame.K_q:
                if ball['x'] > 0 and ball['y'] > 0 and [(ball['x'],ball['y']),(ball['x']-1,ball['y']-1)] not in lines:
                    pygame.draw.line(line_surface, white, (points[ball['x']][ball['y']]), (points[ball['x']-1][ball['y']-1]), 2)
                    lines.append([(ball['x'],ball['y']),(ball['x']-1,ball['y']-1)])
                    ball['y'] -= 1
                    ball['x'] -= 1
                    server.sendPoint(s,str(ball['x'])+';'+str(ball['y']))
                elif ball['y'] == 5 or ball['y'] == 6:
                    if side == 1:
                        print "Wygrana!"
                        server.sendPoint(s,"W1")
                    else:
                        print "Przegrana."
                        server.sendPoint(s,"W0")
                    pygame.quit()
                    sys.exit()
            if event.key == pygame.K_KP9 or event.key == pygame.K_e:
                if ball['x'] < points.__len__()-1 and ball['y'] > 0 and [(ball['x'],ball['y']),(ball['x']+1,ball['y']-1)] not in lines:
                    pygame.draw.line(line_surface, white, (points[ball['x']][ball['y']]), (points[ball['x']+1][ball['y']-1]), 2)
                    lines.append([(ball['x'],ball['y']),(ball['x']+1,ball['y']-1)])
                    ball['y'] -= 1
                    ball['x'] += 1
                    server.sendPoint(s,str(ball['x'])+';'+str(ball['y']))
                elif ball['y'] == 5 or ball['y'] == 6:
                    if side == 1:
                        print "Przegrana."
                        server.sendPoint(s,"W1")
                    else:
                        print "Wygrana!"
                        server.sendPoint(s,"W0")
                    pygame.quit()
                    sys.exit()
            if event.key == pygame.K_KP3 or event.key == pygame.K_c:
                if ball['x'] < points.__len__()-1 and ball['y'] < points[0].__len__()-1 and [(ball['x'],ball['y']),(ball['x']+1,ball['y']+1)] not in lines:
                    pygame.draw.line(line_surface, white, (points[ball['x']][ball['y']]), (points[ball['x']+1][ball['y']+1]), 2)
                    lines.append([(ball['x'],ball['y']),(ball['x']+1,ball['y']+1)])
                    ball['y'] += 1
                    ball['x'] += 1
                    server.sendPoint(s,str(ball['x'])+';'+str(ball['y']))
                elif ball['y'] == 5 or ball['y'] == 4:
                    if side == 1:
                        print "Wygrana!"
                        server.sendPoint(s,"W1")
                    else:
                        print "Przegrana."
                        server.sendPoint(s,"W0")
                    pygame.quit()
                    sys.exit()
            if event.key == pygame.K_KP1 or event.key == pygame.K_z:
                if ball['x'] > 0 and ball['y'] < points[0].__len__()-1 and [(ball['x'],ball['y']),(ball['x']-1,ball['y']+1)] not in lines:
                    pygame.draw.line(line_surface, white, (points[ball['x']][ball['y']]), (points[ball['x']-1][ball['y']+1]), 2)
                    lines.append([(ball['x'],ball['y']),(ball['x']-1,ball['y']+1)])
                    ball['y'] += 1
                    ball['x'] -= 1
                    server.sendPoint(s,str(ball['x'])+';'+str(ball['y']))
                elif ball['y'] == 5 or ball['y'] == 4:
                    if side == 1:
                        print "Przegrana."
                        server.sendPoint("W1")
                    else:
                        print "Wygrana!"
                        server.sendPoint("W0")
                    pygame.quit()
                    sys.exit()
            move = 0

    screen.fill(green)
    x = x_start

    while x <= width-x_start:
        y = y_start
        while y <= height-y_start:
            pygame.draw.circle(screen, white, (x,y), 2, 0)
            y += interval
        x += interval
    pygame.draw.line(screen, white, (x_start-interval,y_start+(((y_dim+2)/2)-1)*interval),(x_start-interval,y_start+(((y_dim+2)/2)+1)*interval), 5)
    pygame.draw.line(screen, white, (x_start-interval,y_start+(((y_dim+2)/2)-1)*interval), (x_start,y_start+(((y_dim+2)/2)-1)*interval), 5)
    pygame.draw.line(screen, white, (x_start-interval,y_start+(((y_dim+2)/2)+1)*interval), (x_start,y_start+(((y_dim+2)/2)+1)*interval), 5)
    pygame.draw.line(screen, white, (width-x_start+interval,y_start+(((y_dim+2)/2)-1)*interval),(width-x_start+interval,y_start+(((y_dim+2)/2)+1)*interval), 5)
    pygame.draw.line(screen, white, (width-x_start+interval,y_start+(((y_dim+2)/2)-1)*interval), (width-x_start,y_start+(((y_dim+2)/2)-1)*interval), 5)
    pygame.draw.line(screen, white, (width-x_start+interval,y_start+(((y_dim+2)/2)+1)*interval), (width-x_start,y_start+(((y_dim+2)/2)+1)*interval), 5)
    pygame.draw.line(screen, white, (x_start,y_start), (width-x_start,y_start), 5)
    #pygame.draw.line(screen, white, (x_start,y_start), (x_start,height-y_start), 5)
    pygame.draw.line(screen, white, (x_start,y_start), (x_start,y_start+(((y_dim+2)/2)-1)*interval), 5)
    pygame.draw.line(screen, white, (x_start,y_start+(((y_dim+2)/2)+1)*interval), (x_start,height-y_start), 5)
    pygame.draw.line(screen, white, (x_start,height-y_start), (width-x_start,height-y_start), 5)
    #pygame.draw.line(screen, white, (width-x_start,y_start), (width-x_start,height-y_start), 5)
    pygame.draw.line(screen, white, (width-x_start,y_start), (width-x_start,y_start+(((y_dim+2)/2)-1)*interval), 5)
    pygame.draw.line(screen, white, (width-x_start,y_start+(((y_dim+2)/2)+1)*interval), (width-x_start,height-y_start), 5)
    pygame.draw.circle(screen, white, (points[ball['x']][ball['y']]), 4, 0)
    screen.blit(line_surface, (-1,-1))
    pygame.display.flip()
    if move == 0:
        msg = s.recv(2048)
        if msg == "W1":
            print 'Wygrana!'
            s.send(exitMsg.encode("utf-8"))
            pygame.quit()
            sys.exit()
        elif msg == "W0":
            print 'Przegrana'
            s.send(exitMsg.encode("utf-8"))
            pygame.quit()
            sys.exit()
        pt = msg.split(';',2)
        x = int(pt[0])
        y = int(pt[1])
        pygame.draw.line(line_surface, white, (points[ball['x']][ball['y']]), (points[x][y]), 2)
        ball['x'] = x
        ball['y'] = y
        move = 1