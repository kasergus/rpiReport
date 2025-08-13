# Project report

This project was created to transmit information through light. So far, we only have an LED and a photoresistor, but this can easily be upgraded to a laser, which will enable information to be transmitted over longer distances. The project consists of two parts: a server and a listener. The server can have many listeners (in this case, only one, since I don't have many Raspberry Pi devices). Listeners work according to the MQTT protocol, namely, a user can subscribe listeners to a topic, and they will receive messages sent to that topic.

## Server side

The server part, in turn, consists of a database that stores models, topics, and some messages, as well as a server written in nodejs.

### Database

The database contains three tables: rpis, topics, and messages. As you can see, the messages table is not related to the topics table, as it simply serves as a repository for certain messages, but not all of them (for example, audio files, which are difficult to create).

![dbDiagram](./pictures/dbDiagram.png)

### Server

On the server's main page, you can view statistics, create a new topic, subscribe a listener to a topic, and send messages to a topic. All of the above entries are saved in the database. Currently, you can send three types of messages: number, text, and audio. The front end also features input validation. To initialize new raspberry pi model, you need to do a post request from it to the server, with `{ model: yourModel }` key-value pair.

![mainPage](./pictures/mainPage.png)


## Listener

The listener consists of two Raspberry Pi devices. One of them receives information from the server, encodes it, and transmits it in the form of light signals to the other. The other Raspberry Pi receives the information and, depending on its type, performs certain actions, for example: when it receives a number, it makes the LED flash the corresponding number of times; when it receives text, it writes it to a file in its system (which can be read later); and when it receives an audio file, it plays it.
