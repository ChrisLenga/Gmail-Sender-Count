function countEmailsPerSender() {
  var sendersCount = {};
  var threads;
  var page = 0;
  var maxThreadsPerPage = 100;
  
  // Set the date range for March 2025
  var startDate = new Date('2021-03-01');
  var endDate = new Date('2025-03-31');
  
  // Format the dates for Gmail search query
  var formattedStartDate = formatDate(startDate);
  var formattedEndDate = formatDate(endDate);
  
  // Loop through all the pages of threads
  do {
    // Search for threads in the specified date range, in batches of 100
    threads = GmailApp.search('after:' + formattedStartDate + ' before:' + formattedEndDate, page * maxThreadsPerPage, maxThreadsPerPage);
    
    // Process each thread
    for (var i = 0; i < threads.length; i++) {
      var messages = threads[i].getMessages();
      
      // Process each message in the thread
      for (var j = 0; j < messages.length; j++) {
        var message = messages[j];
        var from = message.getFrom();
        
        // Increment sender count
        sendersCount[from] = (sendersCount[from] || 0) + 1;
      }
    }
    
    // Move to the next page of threads
    page++;
    
  } while (threads.length === maxThreadsPerPage); // Continue if there's another page

  // Sort senders by count in descending order
  var sortedSenders = Object.entries(sendersCount).sort(function(a, b) {
    return b[1] - a[1];
  });

  // Log the sorted senders
  for (var i = 0; i < sortedSenders.length; i++) {
    Logger.log(sortedSenders[i][0] + ': ' + sortedSenders[i][1]);
  }
}

// Helper function to format date as YYYY/MM/DD
function formatDate(date) {
  return Utilities.formatDate(date, Session.getScriptTimeZone(), 'yyyy/MM/dd');
}
