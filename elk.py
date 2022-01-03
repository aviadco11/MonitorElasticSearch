from datetime import datetime
from elasticsearch import Elasticsearch
import smtplib
import requests

def Check_Valid_ELK():

    try:
        res = requests.get('https://20.126.105.255:9200', auth=('elastic', 'PAgXaK15yCiOUvuS7PuJ'), verify=False)
        print(res.content)
        if res.status_code != 200:
            print("ConnectTimeout!")
            return False
    except Exception as e:
        print(e)
        return False
    return True


def Check_Health_ELK():
    es = Elasticsearch("20.105.254.110:9200")
    print(es.cluster.health())
    res = es.cluster.health()

    return res['status']



def Check_Alerts_Idx_ELK():
    res = requests.get('http://20.105.254.110:9200')
    es = Elasticsearch("20.105.254.110:9200")
    res = es.search(index="test", query={"match_all": {}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print(hit["_source"])

print("Monitor Running : ", datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

def SendEmail(email,password,from_address,to_address,msg):
    try:
        smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_object.starttls()
        smtp_object.login(email, password)
        smtp_object.sendmail(from_address, to_address, msg)
    except Exception as e:
        print(e)
        print("Mail Wasnt send")
        return False
    print("Mail Was send")
    return False


email = 'aviad.co1@gmail.com'
from_address = 'aviad.co1@gmail.com'
to_address = 'aviad.co1@gmail.com'
password = 'mnnonvbgyoadqyhy'

if Check_Valid_ELK():
        if Check_Health_ELK() != 'green':
            subject = "ElasticSearch Healthy - Critical Alert !!!"
            message = "ElasticSearch Status is not Healthy"
            msg = "Subject: " + subject + '\n' + message
            SendEmail(email, password, from_address, to_address, msg)
            print(msg)
        Check_Alerts_Idx_ELK()
else:
    subject = "ElasticSearch Validation - Critical Alert !!!"
    message = "ElasticSearch is Down"
    msg = "Subject: "+subject+'\n'+message
    SendEmail(email,password,from_address,to_address,msg)
    print(msg)
