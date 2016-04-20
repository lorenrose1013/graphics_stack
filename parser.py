from display import *
from matrix import *
from draw import *

ARG_COMMANDS = [ 'line', 'scale', 'translate', 'xrotate', 'yrotate', 'zrotate', 'circle', 'bezier', 'hermite', 'sphere', 'box', 'torus']

def parse_file( f, points, transform, screen, color ):
    temp = new_matrix()
    ident(temp)
    origin_stack = [temp]
    #print origin_stack
    commands = f.readlines()


    c = 0
    while c  <  len(commands):
        cmd = commands[c].strip()
        #temp = []
        if cmd in ARG_COMMANDS:
            c+= 1
            args = commands[c].strip().split(' ')
            i = 0
            while i < len( args ):
                args[i] = float( args[i] )
                i+= 1
            if cmd == 'line':
                points = []
                add_edge( points, args[0], args[1], args[2], args[3], args[4], args[5] )
                matrix_mult(origin_stack[-1], points)
                draw_lines(points, screen, color)
                
                
            elif cmd == 'circle':
                points = []
                add_circle( points, args[0], args[1], 0, args[2], .01 )
                matrix_mult(origin_stack[-1], points)
                draw_lines(points, screen, color)
                
            
            elif cmd == 'bezier':
                points = []
                add_curve( points, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], .01, 'bezier' )
                matrix_mult(origin_stack[-1], points)
                draw_lines(points, screen, color)
                
            
            elif cmd == 'hermite':
                points = []
                add_curve( points, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], .01, 'hermite' )
                matrix_mult(origin_stack[-1], points)
                draw_lines(points, screen, color)
                

            elif cmd == 'sphere':
                points = []
                add_sphere( points, args[0], args[1], 0, args[2], 5 )
                matrix_mult(origin_stack[-1], points)
                draw_polygons(points, screen, color)
                

            elif cmd == 'torus':
                points = []
                add_torus( points, args[0], args[1], 0, args[2], args[3], 5 )
                matrix_mult(origin_stack[-1], points)
                draw_polygons(points, screen, color)
                

            elif cmd == 'box':
            	points = []
                add_box( points, args[0], args[1], args[2], args[3], args[4], args[5] )
                matrix_mult(origin_stack[-1], points)
                draw_polygons(points, screen, color)
                


            elif cmd == 'scale':
                s = make_scale( args[0], args[1], args[2] )
                matrix_mult(origin_stack[-1], s)
                origin_stack[-1] = s

            elif cmd == 'translate':
                t = make_translate( args[0], args[1], args[2] )
                matrix_mult(origin_stack[-1], t)
                origin_stack[-1] = t

            else:
                angle = args[0] * ( math.pi / 180 )
                if cmd == 'xrotate':
                    r = make_rotX( angle )
                elif cmd == 'yrotate':
                    r = make_rotY( angle )
                elif cmd == 'zrotate':
                    r = make_rotZ( angle )
                matrix_mult(origin_stack[-1], r)
                origin_stack[-1] = r
        elif cmd == 'push':
            origin_stack.append(origin_stack[-1])
        elif cmd == 'pop':
            origin_stack.pop()
        elif cmd == 'ident':
            ident( transform )
            
        elif cmd == 'apply':
            matrix_mult( transform, points )

        elif cmd == 'clear':
            points = []

        elif cmd in ['display', 'save' ]:
            screen = new_screen()
            draw_polygons( points, screen, color )
            
            if cmd == 'display':
                display( screen )

            elif cmd == 'save':
                c+= 1
                save_extension( screen, commands[c].strip() )
        elif cmd == 'quit':
            return    
        elif cmd[0] != '#':
            print 'Invalid command: ' + cmd
        c+= 1
