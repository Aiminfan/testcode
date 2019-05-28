const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
function findDocumentsSP(db, callback) {
  // Get the documents collection
  const collection = db.collection('Addess');
  // Find some documents
  collection.find(
	{ 'geometry':
	  { $nearSphere :
	    { $geometry:
	      { type: "Point",  coordinates: [ -81.20882944910463, 42.765949307742005 ] },
	        $maxDistance: 1
	    }
	  }
	}
  ).toArray(function(err, docs) {
    assert.equal(err, null);
    console.log("Found the following records");
    console.log(docs);
    callback(docs);
  });      
}
var findDocuments = function(db,qry,srt, callback) {
  var collection = db.collection( 'Address' );
  collection.find(qry).sort(srt).toArray(function(err, docs) {
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
qry={ 'attributes.ADDRESS' : '80-92 Confederation Dr, St Thomas, Ontario, N5P 3Y2' };
srt={ 'attributes.FID': -1 }
  findDocuments(db,qry,srt, function() {
    client.close();
  });
});
