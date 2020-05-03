import pygame,sys,time,math,threading,os,random
from pygame.locals import *
import sqlite3

pygame.init()
WIDTH,HEIGHT=800,500
surface=pygame.display.set_mode((WIDTH,HEIGHT),0,32)
fps=100
ft=pygame.time.Clock()
pygame.display.set_caption('Ping Pong')

app_font=pygame.font.SysFont('segoe print',15,bold=False,italic=False)


class pos:
	def __init__(self,x=0,y=0):
		self.x=x
		self.y=y
	def random(self):
		self.x=random.randint(20,760)
		self.y=random.randint(20,440)

class ball:
	def __init__(self):
		self.pos=pos(50,50)
		self.size=20
		self.velocity=pos(2,2)
	def move(self):#.
		self.pos.x+=self.velocity.x
		self.pos.y+=self.velocity.y
	def check_boundary(self,paddle):
		got_in="no"
		if self.pos.x<=0 or WIDTH<=self.pos.x+self.size:
			self.velocity.x*=-1
		if self.pos.y<=0 or HEIGHT<=self.pos.y+self.size:
			self.velocity.y*=-1
			if HEIGHT<=self.pos.y+self.size:
				got_in="drop"#False
				# sys.stdout.write("---\n")
		ball_points=[
			pos(self.pos.x,self.pos.y),
			pos(self.pos.x,self.pos.y+self.size),
			pos(self.pos.x+self.size,self.pos.y),
			pos(self.pos.x+self.size,self.pos.y+self.size)
			]
		paddle_points=[paddle.pos.x,paddle.pos.x+paddle.width,paddle.pos.y,paddle.pos.y+20]
		for ball_point in ball_points:
			if paddle.pos.x<=ball_point.x<=paddle.pos.x+paddle.width and paddle.pos.y<=ball_point.y<=paddle.pos.y+20:
				if self.pos.y+self.size<=paddle.pos.y:
					self.velocity.y*=-1
				else:
					self.velocity.x*=-1
				got_in="hit"
				# sys.stdout.write("ooops\n")
				break
		return got_in

class paddle:
	def __init__(self):
		self.pos=pos(20,480)
		self.width=160
		self.height=10
		self.velocity=pos(80,0)
		self.speed=0
	def move(self,direction="null"):
		pass
		if direction=="right":
			self.velocity.x=abs(self.velocity.x)
			self.speed=self.velocity.x
		elif direction=="left":
			self.velocity.x=(-1)*abs(self.velocity.x)
			self.speed=self.velocity.x
		if self.speed<0:
			self.speed+=5
			self.pos.x-=5
		elif self.speed>0:
			self.speed-=5
			self.pos.x+=5
	def check_boundary(self):
		if self.pos.x<=0:
			self.pos.x=0
		elif WIDTH<=self.pos.x+self.width:
			self.pos.x=WIDTH-self.width
	def check_collision(self,ball):
		pass

class home:
	def __init__(self,surface):
		self.white=(255,255,255)
		self.black=(0,0,0)
		self.ball=ball()
		self.paddle=paddle()
		self.surface=surface
		self.direction="null"
		self.loops_size=5
		self.loops=[False]*self.loops_size
		self.loops_index=0
		self.custom_dataset="ball_x,ball_y,paddle_x,paddle_y,ball_velocity_x,ball_velocity_y,paddle_velocity_x,paddle_velocity_y,winning_strategy\n"
		self.current_fit=""
	def draw_paddle(self):
		pygame.draw.rect(self.surface,self.black,(self.paddle.pos.x,self.paddle.pos.y,self.paddle.width,self.paddle.height))
	def draw_ball(self):
		pygame.draw.rect(self.surface,self.black,(self.ball.pos.x,self.ball.pos.y,self.ball.size,self.ball.size))
		# pygame.draw.circle(self.surface,self.black,(self.ball.pos.x,self.ball.pos.y),self.ball.size)
	def manage_loops(self):
		self.loops_index+=1
		if self.loops_index>=self.loops_size:
			self.loops_index=0
		Trues=0
		for state in self.loops:
			if state=="hit":
				Trues+=1
		if Trues==self.loops_size:
			self.ball.pos.y=self.paddle.pos.y-self.ball.size-2
	def current_state(self):
		pass
		# print (0,0,WIDTH,HEIGHT,self.ball.size,self.paddle.width,self.paddle.height,self.ball.pos.x,self.ball.pos.y,self.paddle.pos.x,self.paddle.pos.y,self.ball.velocity.x,self.ball.velocity.y,self.paddle.velocity.x,self.paddle.velocity.y)
		# print (self.ball.pos.x,self.ball.pos.y,self.paddle.pos.x,self.paddle.pos.y,self.ball.velocity.x,self.ball.velocity.y,self.paddle.velocity.x,self.paddle.velocity.y)
		self.current_fit+=str(self.ball.pos.x)+","+str(self.ball.pos.y)+","+str(self.paddle.pos.x)+","+str(self.paddle.pos.y)+","+str(self.ball.velocity.x)+","+str(self.ball.velocity.y)+","+str(self.paddle.velocity.x)+","+str(self.paddle.velocity.y)+"\n"
	def add_to_database(self):
		pass
		outputs=["drop","hit"]
		type_=str(outputs.index(self.loops[self.loops_index]))
		text=self.current_fit.replace("\n",","+type_+"\n")
		self.custom_dataset+=text
		self.current_fit=""
		# sys.stdout.write(self.custom_dataset)
	def write_on_file(self):
		fobj=open("ping_pong_dataset.csv","w")
		fobj.write(self.custom_dataset)
		fobj.close()
	def main(self):
		play=True#
		while play:
			surface.fill(self.white)
			for event in pygame.event.get():
				if event.type==QUIT:
					pygame.quit()
					sys.exit()
				if event.type==KEYDOWN:
					if event.key==K_RETURN or event.key==K_SPACE:
						play=False
					if event.key==K_RIGHT:
						self.paddle.move("right")
					if event.key==K_LEFT:
						self.paddle.move("left")
				if event.type==KEYUP:
					if event.key==K_RETURN or event.key==K_SPACE:
						play=False
					if event.key==K_RIGHT:
						self.paddle.move("right")
					if event.key==K_LEFT:
						self.paddle.move("left")
			#-----
			self.draw_paddle()
			self.paddle.check_boundary()
			self.paddle.check_collision(self.ball)
			self.paddle.move()
			self.draw_ball()
			self.loops[self.loops_index]=self.ball.check_boundary(self.paddle)
			self.current_state()
			if self.loops[self.loops_index]!="no":
				self.add_to_database()
				sys.stdout.write(self.loops[self.loops_index]+"\n")
			self.ball.move()
			self.manage_loops()
			#-----
			pygame.display.update()
			ft.tick(fps)
		self.write_on_file()



if __name__=="__main__":
	home(surface).main()




#----------------
