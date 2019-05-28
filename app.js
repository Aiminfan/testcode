const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
const findDocuments = function(db, callback) {
  // Get the documents collection
  const collection = db.collection('Address');
  // Find some documents
  collection.find({}).toArray(function(err, docs) {
	assert.equal(err, null);
	console.log("Found the following records");
	console.log(docs)
	callback(docs);
  });
}
// Connection URL
const url = 'mongodb://localhost:27017';

// Database Name
const dbName = 'dbGIS';

// Create a new MongoClient
const client = new MongoClient(url);

// Use connect method to connect to the Server
client.connect(function(err) {
  assert.equal(null, err);
  console.log("Connected successfully to server");

  const db = client.db(dbName);

  findDocuments2(db, function() {
    client.close();
  });
});
var findDocuments2 = function(db, callback) {
  var collection = db.collection( 'Address' );
  collection.find({ 'attributes.ADDRESS' : '39316-40298 Bush Line, St Thomas, Ontario, N5P 3S9' }).sort({ 'Accuracy': 1 }).toArray(function(err, docs) {
      assert.equal(err, null);
      console.log("Found the following records");
      console.log(docs)
      callback(docs);
  });
}