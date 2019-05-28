function create2dSphereIndex(db, callback) {
  // Get the restaurants collection
  const collection = db.collection('restaurants');
  // Create the index
  collection.createIndex(
    { 'address.coord' : "2dsphere" }, function(err, result) {
    console.log(result);
    callback(result);
  });
};

const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');

// Connection URL
const url = 'mongodb://localhost:27017';

// Database Name
const dbName = 'myproject';

// Create a new MongoClient
const client = new MongoClient(url);

// Use connect method to connect to the Server
client.connect(function(err, client) {
  assert.equal(null, err);
  console.log("Connected correctly to server");

  const db = client.db(dbName);
  create2dSphereIndex(db, function() {
    client.close();
  });
});
