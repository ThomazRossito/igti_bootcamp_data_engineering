import json
from tweepy import OAuthHandler, Stream, StreamListener
from datetime import datetime

# Cadastrar as chaves de acesso
consumer_key = "HqvF3RDEKGUPx3jZTL2rTXpet"
consumer_secret = "EvaUcUgwEJatVsFzYHhMxYEqwWEK3s1TDsfRzeC0Xa7K3x97Bj"

access_token = "52387109-AswtBBnqQ2opuTJj4uPVNJ44fOTGN9htjv15yMOJH"
access_token_secret = "B1RfpZ8fho8MKXioL30opah7f7XvRYtq0WLgHn3eRMJLa"

# Definir um arquivo de saída para armazenar os tweets coletados
data_hoje = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
out = open(f"colleted_tweets_{data_hoje}.txt", "w")

# Implementar uma classe para conexão com o Twitter
class MyListener(StreamListener):

    def on_data(self, data):
        print(data)
        itemString = json.dumps(data)
        out.write(itemString + "\n")

        return True

    def on_error(self, status):
        print(status)

# Implementar função MAIN
if __name__ == "__main__":
    l = MyListener()
    auth = OAuthHandler(consumer_key, consumer_secret)      
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track = ["Trump"])  