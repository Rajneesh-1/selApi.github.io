import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin import *

cred = credentials.Certificate("smartelist.json")
firebase_admin.initialize_app(cred)

def sendPush(channelData,deeplinkData, dataObject=None):
    # See documentation on defining a message payload.
    a = 2
    message = messaging.MulticastMessage(
                data={

                    'body': "AndroidRegistrationMessage",
                    'title': "Weather Notification",
                    'clickAction': "GAME_PLAY",
                    'channel': "ALERT",
                    'displayNotification': 'YES'
                    },
                tokens=["ddq7NNNxQ7esvnuzFiEZrh:APA91bGebI50gI9qzvVx-nK-zdpWopTh-26wxHBsXUN0BYEJC2WQL96kq_A8XhFjw9COOl6UFC_UmqNmcXobYdsCjhMxrhxXq-sDoJqbqFky6Gn6q3Ay-MkWZSNBRx1Hn9bAseeek3po"],
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    

channelList=["TICKETS","TRANSACTIONS"]
deepLinkList=["NOTIFICATION_CALLBACK_TICKETS","NOTIFICATION_CALLBACK_TRANSACTIONS", "NOTIFICATION_CALLBACK_GAME_PLAY"] 
i=0
if __name__ == '__main__':
    sendPush(channelList[i],deepLinkList[i])