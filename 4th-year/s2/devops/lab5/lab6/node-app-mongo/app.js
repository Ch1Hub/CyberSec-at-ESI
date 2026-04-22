const express = require("express");
const { MongoClient } = require("mongodb");

const app = express();
app.use(express.json());

const uri = process.env.MONGO_URI;

if (!uri) {
  console.error("MONGO_URI not defined");
  process.exit(1);
}

const client = new MongoClient(uri);

let db;

async function connectDB() {
  await client.connect();
  db = client.db("mydatabase");
  console.log("Connected to MongoDB ReplicaSet");
}

connectDB();

app.post("/add", async (req, res) => {
  const result = await db.collection("test").insertOne(req.body);
  res.send(result);
});

app.get("/data", async (req, res) => {
  const data = await db.collection("test").find().toArray();
  res.send(data);
});

app.listen(3000, () => console.log("Node app running on 3000"));
