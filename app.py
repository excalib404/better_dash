import dash

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Age of Coins Visualization'
app.config['suppress_callback_exceptions'] = True


#Конфиг БД
db_config = {'user': 'postgres_prod',  # имя пользователя
             'pwd': 'hE5a2Zsa7zJxTZ3',  # пароль
             'host': 'cm-analytics-prod.c7h1y1l8rp6x.eu-central-1.rds.amazonaws.com',
             'port': 5432,  # порт подключения
             'db': 'coinmaster_analytics'}  # название базы данных

# Формируем строку соединения с БД.
connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_config['user'],
                                                         db_config['pwd'],
                                                         db_config['host'],
                                                         db_config['port'],
                                                         db_config['db'])





