# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.listview import ListItemButton
from kivy.properties import ListProperty, NumericProperty
import requests
# Dados iniciais com a lista de deputados
requested_data = requests.get('http://127.0.0.1:5000/deputados')
data = requested_data.json()
# Construtor das classes para a interface grática do APP
Builder.load_string('''
#:import la kivy.adapters.listadapter
#:import factory kivy.factory
<MenuButton>:
	size_hint_y: None
	height: dp(24)
	on_release: app.on_menu_selection(self.index)
<MenuPage>:
	BoxLayout:
    	BoxLayout:
        	size_hint:(.1, None)
    	ListView:
        	size_hint: .8,.9
        	adapter:
            	la.ListAdapter(
            	data=app.nome,
            	cls=factory.Factory.MenuButton,
            	selection_mode='single',
            	allow_empty_selection=True,
            	args_converter=root.args_converter)
    	BoxLayout:
        	size_hint:(.1, None)
<Page>:
	BoxLayout:
    	BoxLayout:
        	orientation:'vertical'
        	Button:
            	text: app.nome_deputado
            	size_hint:(1, .2)
        	Button:
            	text: "Estado: "+app.uf
            	size_hint:(1, .1)
        	Button:
            	text: "Partido: "+app.partido
            	size_hint:(1, .1)
        	AsyncImage:
            	source: 'app.foto'
            	size_hint:(1, .8)
        	Button:
            	text:'Ver todos os deputados'
            	size_hint:(1, .1)
            	on_press: root.manager.current = 'menu'
''')
# Classe utilizado para cada item da lista
class MenuButton(ListItemButton):
	index = NumericProperty(0)
# Pagina inicial com o menu listando os deputados
class MenuPage(Screen):
	def args_converter(self, row_index, title):
    	return {
        	'index': row_index,
        	'text': title
    	}
class Page(Screen):    
	pass
# Classe principal, mantendo as paginas, gerenciador de paginas e eventos
class Main(App):
	# Lista principal de deputados
	nome = ListProperty(["{}".format(i['nome'].encode('utf-8')) for i in data])
	sm = ScreenManager()
	# Página com mais informações do deputado escolhido
	page = ''
	nome_deputado = ''
	partido = ''
	foto = ''
	uf = ''
	def build(self):
    	menu = MenuPage(name='menu')
    	self.sm.add_widget(menu)
    	return self.sm
	# Evento de selecao de um dos itens do menu
	def on_menu_selection(self, index):
    	id_deputado = str(data[index]['id'])
    	# Requisicao dos detalhes do deputado escolhido
    	det = requests.get('http://127.0.0.1:5000/deputados/detalhes/{}'.format(id_deputado)).json()[0]
    	self.page = str(det['id'])
    	self.nome_deputado = str(det['nome'].encode('utf-8'))
    	self.partido = str(det['partido'])
    	self.foto = str(det['foto'])
    	self.uf = str(det['uf'])
    	# Criação e atribuição da nova página
    	page = Page(name=self.page)
    	self.sm.add_widget(page)
    	# Evento de transição para a nova página com as informações setadas
    	self.root.current = self.page
if __name__ == '__main__':
	Main().run()

