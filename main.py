import pygame, json, time, random, sys

pygame.init()

class Game:
    def __init__(self):
        self.configs = json.load(open("configs.json", "r"))
        self.tela = pygame.display.set_mode(self.configs['tela-configs']['size'])
        self.clock = pygame.time.Clock()
        
        self.cobra = {
            "corpo":[],
            "score":0,
            "cabeca":{
                "x":0,
                "y":0
            },
            "frutas":[]
        }

        pygame.display.set_caption(self.configs['tela-configs']['caption'])

    def drawScore(self):
        fonte = pygame.font.SysFont('comicsans', 13)
        text = fonte.render(f"Pontos: {self.cobra['score']}", True, (0, 0, 0))
        self.tela.blit(text, [0, 0])

    def gameOver(self):
        self.tela.fill('white')
        fonte = pygame.font.SysFont('comicsans', 30)
        text = fonte.render(f"Game Over", True, (255, 0, 0))
        self.tela.blit(text, [130, 80])
        fonte = pygame.font.SysFont('comicsans', 13)
        text = fonte.render(f"Pontos: {self.cobra['score']}", True, (0, 0, 0))
        self.tela.blit(text, [180, 125])
        pygame.display.update()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    def drawSnake(self):
        pygame.draw.rect(self.tela, (0, 0, 255), pygame.Rect(self.cobra['cabeca']['x'], self.cobra['cabeca']['y'], 10,10))
        for corpo in self.cobra['corpo']:
            pygame.draw.rect(self.tela, (0, 0, 255), pygame.Rect(corpo[0], corpo[1], 10,10))

    def drawFruit(self):
        if len(self.cobra['frutas']) < 1:
            frutax = random.randrange(0, int(self.configs['tela-configs']['size'][0] / 10)) * 10
            frutay = random.randrange(0, int(self.configs['tela-configs']['size'][1] / 10)) * 10
            self.cobra['frutas'].append([frutax, frutay])
        pygame.draw.rect(self.tela, (0, 255, 0), pygame.Rect(self.cobra['frutas'][0][0], self.cobra['frutas'][0][1], 10, 10))
            
    def inputColision(self):
        for corpo in self.cobra['corpo'][:-1]:
            if self.cobra['cabeca']['x'] == corpo[0] and self.cobra['cabeca']['y'] == corpo[1]:
                print("[LOG] COLIDIU NO PROPRIO CORPO")
                self.gameOver()

        for fruta in self.cobra['frutas']:
            if self.cobra['cabeca']['x'] == fruta[0] and self.cobra['cabeca']['y'] == fruta[1]:
                self.cobra['corpo'].append([self.cobra['cabeca']['x'], self.cobra['cabeca']['y']])
                self.cobra['frutas'].remove(fruta)
                self.cobra['score'] += 1
                print("[LOG] COMEU")
                
        if self.cobra['cabeca']['x'] > self.configs['tela-configs']['size'][0]-10 or self.cobra['cabeca']['x'] < 0 or self.cobra['cabeca']['y'] < 0 or self.cobra['cabeca']['y'] > self.configs['tela-configs']['size'][1]-10:
            print("[LOG] COLIDIU COM A PAREDE")
            self.gameOver()
                
    def run(self):
        direcao = 'esquerda'
        velocidade = 10
        while True:
            self.tela.fill('white')

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and direcao != 'esquerda':
                        direcao = 'direita'
                    if event.key == pygame.K_RIGHT and direcao != 'direita':
                        direcao = 'esquerda'
                    if event.key == pygame.K_UP and direcao != 'baixo':
                        direcao = 'cima'
                    if event.key == pygame.K_DOWN and direcao != 'cima':
                        direcao = 'baixo'

                
            if direcao == 'esquerda':
                self.cobra['cabeca']['x'] += velocidade
            if direcao == 'direita':
                self.cobra['cabeca']['x'] -= velocidade  
            if direcao == 'cima':
                self.cobra['cabeca']['y'] -= velocidade  
            if direcao == 'baixo':
                self.cobra['cabeca']['y'] += velocidade
            
            self.drawFruit()
            self.drawSnake()            

            if (len(self.cobra['corpo']) - 1) < self.cobra['score']:
                try:
                    del self.cobra['corpo'][0]
                    self.cobra['corpo'].append([self.cobra['cabeca']['x'], self.cobra['cabeca']['y']])
                except Exception:
                    pass

            self.inputColision()
            self.drawScore()
            pygame.display.update()
            self.clock.tick(10)


            
            
Game().run()