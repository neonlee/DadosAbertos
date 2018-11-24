# coding=utf-8
# importacao do twitter
import datetime
import sqlite3
import pytz
import stream as stream
from twython import Twython
from twython import TwythonStreamer

# importacao do ibm watson
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, MetadataOptions

# classe para procurar por tags especificas
class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        result = data['text']
        response = analyse_text(result)

        print_result(response)
        # Id do twitter
        object_id = data['id']

        # Id do usuário que postou o texto
        user_id = data['user']['id']

        # Usuário que postou o texto
        user_name = data['user']['screen_name']

        # Texto postado em utf-8
        text = data['text'].encode('utf-8')

        # Localizacao
        location = data['location']

        # Data que foi publicado
        posted_at_tweet = data['created_at']

        # Data que foi publicado formatada
        fmt = '%Y-%m-%d %H:%M:%S.%f'
        new_date = datetime.strptime(posted_at_tweet, '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)

        published_date = str(new_date.strftime(fmt))

        tweet = {
            'object_id': object_id,
            'user_id': user_id,
            'user_name': user_name,
            'text': text,
            'location': location,
            'published_date': published_date,
            'create_date': published_date,
            'last_update': published_date,
        }

        print(tweet)

    def on_error(self, status_code, data):
        print(status_code)

        self.disconnect()


# chaves do ibm watson
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    iam_apikey='Ks3JElbjJ4siaCLPHEwAitNC61lIAOmk3dKoJFbc5yta',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api'
)

# chaves do twitter
KEY = 'WD6MNBdsjOSlEtOL6K7lSz3Jj'
SECRET = 'javuS4bikNZtpDqwp98hoifI3LRcLl8Or0KPeEKbZ9SH3SxrXN'
OAUTH_TOKEN = '369120217-EX4KS3ObQfe1SSIYgoskjENt1cg7XNilamxvQbqK'
OAUTH_TOKEN_SECRET = 'ttsdHxwATCOK4Eu2LMmxMVKkWfTto3zqQIPmfdVohXENU'

# instanciando o twitter
tw = Twython(KEY, SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# buscando dados pelo nome de usuario
tw_timeline = tw.get_user_timeline(screen_name="@andremourapsc_")
# E criamos nossa instância do coletor por tag especifica 130696242, 156648466, 2214964776,888059482097553410,630758039,117091723,818438978693165056,111148190
stream = MyStreamer(KEY, SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

connection = sqlite3.connect('banco.db')
c = connection.cursor()

for tweet in tw_timeline:
    nome='andremourapsc_'
    id=160543
    t = tweet['text']
    d = tweet['created_at']
    print("----")
    print(t)
    print(d)
    c.execute("""INSERT INTO dadostt (usuario, id ,tweet,data) VALUES(?,?,?,?)""", (nome, id, t, d))
    connection.commit()
#analisando o texto do twitter
def analyse_text(text):
    print("Texto: %s" % text)



    response = natural_language_understanding.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(
                emotion=True,
                sentiment=True
            ),
            keywords=KeywordsOptions(
                emotion=True,
                sentiment=True
            ),
        )
    ).get_result()

    return response



# mostrando os dados encontados e separando-os
def print_result(response):
    print("Language: %s" % response['language'])
    print("")
    print("Keywords")
    for keyword in response['keywords']:
        print("\t%s (%s, %f)" % (keyword['text'], keyword['sentiment']['label'], keyword['relevance']))

    print("")
    print("Entities")
    for entitie in response['entities']:
        print("\t%s (%s, %s)" % (entitie['text'], entitie['type'], entitie['sentiment']['label']))
        e = entitie['text']
        tipo = entitie['type']
        c.execute("""INSERT INTO entidades (id, entidade , data, tipo) VALUES(?,?,?,?)""", (id, e, d, tipo))
        connection.commit()
        print("")


# imprimindo os dados do texto do usuario
for tweet in tw_timeline:
    result = tweet['text']
    print(tweet)
    response = analyse_text(result)
    print_result(response)

# metodo para procurar por tag especifica
# stream.statuses.filter(track="brasil, #brasil")
