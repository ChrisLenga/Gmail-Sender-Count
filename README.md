# Gmail-Sender-Count

This is a simple script that when run will generate a log of senders by how many emails are in the Gmail Inbox based on the senders' email. If you're using this to clean up a massively overfilled inbox you will have to run this multiple times (due to rate limits) after deleting emails. 

You'll run this script directly from https://script.google.com/home.

function countEmailsPerSender() {
  var threads = GmailApp.getInboxThreads();
  var sendersCount = {};

  for (var i = 0; i < threads.length; i++) {
    var messages = threads[i].getMessages();
    for (var j = 0; j < messages.length; j++) {
      var message = messages[j];
      var from = message.getFrom();
      sendersCount[from] = (sendersCount[from] || 0) + 1;
    }
  }

  // Create an array of [sender, count] pairs and sort it by count in descending order
  var sortedSenders = Object.entries(sendersCount).sort(function(a, b) {
    return b[1] - a[1];
  });

  // Log the sorted senders
  for (var i = 0; i < sortedSenders.length; i++) {
    Logger.log(sortedSenders[i][0] + ': ' + sortedSenders[i][1]);
  }
}
