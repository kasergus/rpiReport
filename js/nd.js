import express from "express"
import pgp from "pg-promise"
import cors from "cors"

const app = express();
const dataDB = pgp()("postgresql://postgres:4230@localhost:5432/data");
const mqttDB = pgp()("postgresql://postgres:4230@localhost:5432/mqtt");

const defaultError = "[!] Error: Something went wrong";

const sleep = ms => new Promise(r => setTimeout(r, ms));

function resultSend(res, msg) {
  res.send(resultPage(msg));
}

function rawErrorSend(res) {
  res.send(defaultError);
}

function errorSend(res) {
  resultSend(res, defaultError);
}

function success(res) {
  resultSend(res, "Success!");
}

function displayError(res, error) {
  errorSend(res);
  console.log("[!] Error:", error);
}

function checkDuplicates(error) {
  return error.code == "23505";
}

function determineDuplError(res, error, msg) {
  if (checkDuplicates(error)) {
    resultSend(res, msg);
  } else {
    displayError(res, error);
  }
}

function resultPage(text) {
  let successPage = `
    <!DOCTYPE html>

    <html>
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
          * {
            font-family: "IBM Plex Mono", monospace;
            margin: 5px
          }
        </style>
      </head>
      <body>
        <header>${text}</header>
        <form action="/index.html">
          <input type="submit" value="Back">
        </form>
      </body>
    </html>
  `;
  return successPage;
}

async function processQuery(req, res) {
  let body = req.body;

  try {
    let data = await doQuery(body["query"]);
    res.json(data);
  } catch (error) {
    res.json(error);
  }
}

async function rpiGetMsg(req, res) {
  let selectQuery = `
    SELECT topics.posting, topics.msg_type, topics.msg_content
    FROM topics
    JOIN rpis
    ON rpis.topic_id = topics.id
    WHERE rpis.model = $1;
  `;
  res.setHeader("Content-Type", "application/json")
  try {
    let data = await mqttDB.one(selectQuery, req.body.model);
    data.succeed = true;
    res.json(data);
  } catch (error) {
    console.log("[!] Error:", error);
    res.json({succeed: false});
  }
}

async function assign(req, res) {
  try {
    let body = req.body;
    let insertQuery = `
      UPDATE rpis 
      SET topic_id=topics.id
      FROM topics
      WHERE rpis.model IN ($1:csv) AND topics.path=$2;
    `;
    await mqttDB.any(insertQuery, [body.models, body.path]);
    success(res);
  } catch (error) {
    determineDuplError(res, error, "[!] Error: This RPi model is already assigned to that topic");
  }
}

async function init(req, res) {
  try {
    let filter = /^[A-Za-z0-9]+([_\-][A-Za-z0-9]+)*$/;
    let model = req.body.model;
    if (!filter.test(model)) {
      res.send("Model must contain only numbers, letters and have '-' or '_' as a space between symbols");
      return;
    }
    await mqttDB.any(`INSERT INTO rpis (model) VALUES ($1);`, model);
    res.send("Success!");
  } catch (error) {
    if (checkDuplicates(error)) {
      res.send("[!] Error: model already exists");
    } else {
      errorSend(res);
    }
  }
}

async function getData(column, table) {
  try {
    let safeColumn = pgp.as.name(column);
    let safeTable = pgp.as.name(table);
    let data = await mqttDB.any(`SELECT ${safeColumn} FROM ${safeTable};`)
    return data;
  } catch (error) {
    throw error;
  }
}

async function queryMessage(type, message, topics) {
  try {
    await mqttDB.any("UPDATE topics SET posting = NOT posting, msg_type=$1, msg_content=$2, amount = amount + 1 WHERE path IN ($3:csv);", [type, message, topics]);
  } catch (error) {
    throw error;
  }
}

async function sendMesssage(req, res, type) {
  try {
    let body = req.body;
    queryMessage(type, body.message, body.topics);
    success(res);
  } catch (error) {
    displayError(res, error);
  }
}

async function sendInt(req, res) {
  sendMesssage(req, res, "int");
}

async function sendText(req, res) {
  sendMesssage(req, res, "text");
}

async function sendAudio(req, res) {
  try {
    let body = req.body;
    let data = await mqttDB.one("SELECT content FROM messages WHERE type='audio' AND name=$1", body.audioName);
    let message = data.content;
    queryMessage("audio", message, body.topics);
    success(res);
  } catch (error) {
    displayError(res, error);
  }
}

async function getRpis(req, res) {
  let result = await getData("model", "rpis");
  res.send(result); 
}

async function getTopics(req, res) {
  let result = await getData("path", "topics");
  res.send(result);
}

async function getAmounts(req, res) {
  try {
    let result = await mqttDB.any("SELECT path, amount FROM topics;");
    res.send(result);
  } catch (error) {
    displayError(res, error);
  }
}

async function getSubs(req, res) {
  try {
    let getQuery = `
      SELECT topics.path, COUNT(path) AS subs
      FROM topics
      JOIN rpis
      ON topics.id = rpis.topic_id
      GROUP BY path
    `
    let result = await mqttDB.any(getQuery);
    res.send(result);
  } catch (error) {
    displayError(res, error);
  }
}

async function getAudios(req, res) {
  try {
    let data = await mqttDB.any("SELECT name FROM messages WHERE type='audio'");
    res.send(data);
  } catch (error) {
    displayError(res, error);
  }
}

async function createTopic(req, res) {
  try {
    await mqttDB.any(`INSERT INTO topics (path) VALUES ($1)`, [req.body.path]);
    success(res);
  } catch (error) {
    determineDuplError(res, error, "[!] Error: topic already exists");
  }
}

async function unkownPath(req, res) {
  res.send("What?");
}

app.use(express.json());
app.use('/', express.static("public"));
app.use("/static", express.static("public"));
// app.use(express.text("utf-8"));
// app.use(express.raw())
app.use(express.urlencoded());
app.use(cors());

// app.get('*', unkownPath);
app.post("/db", processQuery);
app.post("/assign", assign);
app.post("/init", init);
app.get("/getrpis", getRpis);
app.get("/gettopics", getTopics);
app.post("/createtopic", createTopic);
app.post("/sendint", sendInt);
app.post("/sendtext", sendText);
app.post("/sendaudio", sendAudio);
app.get("/getaudios", getAudios);
app.get("/getamounts", getAmounts);
app.get("/getsubs", getSubs);
app.post("/rpitopic", rpiGetMsg);

app.listen(8080, "0.0.0.0");
