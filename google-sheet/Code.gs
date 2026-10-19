/*
  DigiLab - saves every website form submission as a new row in this Google Sheet
  AND sends you a Gmail notification.

  Apply form   -> tab "Applications"
  Contact form -> tab "Contacts"
  (Tabs and column headings are created automatically.)

  Setup steps: see README.md, Step 4 (Sheet) and Step 5 (Gmail notification).
*/

// ------------------------------- SETTINGS -------------------------------
// Which email gets the "new application" notification?
// Leave '' to use the Gmail account that owns this Sheet/script.
// Example:  var NOTIFY_EMAIL = 'you@gmail.com';
var NOTIFY_EMAIL = '';
// -------------------------------------------------------------------------


// Open the web app link in a browser to check it is live.
function doGet() {
  return ContentService.createTextOutput('DigiLab form endpoint is working.');
}

function doPost(e) {
  var p = (e && e.parameter) || {};
  var isContact = p.form_type === 'contact';
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var lock = LockService.getScriptLock();
  var locked = false, saved = false;

  // 1) save the row first (this must never be lost)
  try {
    lock.waitLock(20000);
    locked = true;
    saveRow(ss, p, isContact ? 'Contacts' : 'Applications');
    saved = true;
  } catch (err) {
    saved = false;
  } finally {
    if (locked) lock.releaseLock();
  }

  // 2) then send the notification email. A mail problem can never lose a saved row.
  if (saved) {
    try { notify(p, isContact, ss); } catch (err) { /* ignore */ }
  }
  return ContentService.createTextOutput(saved ? 'ok' : 'error');
}

function labelOf(key) {
  var label = String(key).replace(/_/g, ' ');
  return label.charAt(0).toUpperCase() + label.slice(1);
}

function saveRow(ss, p, sheetName) {
  var sh = ss.getSheetByName(sheetName) || ss.insertSheet(sheetName);

  // make sure the first row has a heading for every field
  var lastCol = sh.getLastColumn();
  var headers = lastCol > 0 ? sh.getRange(1, 1, 1, lastCol).getValues()[0] : [];
  if (headers.length === 0) {
    headers = ['Received at'];
    sh.getRange(1, 1).setValue('Received at').setFontWeight('bold');
    sh.setFrozenRows(1);
  }
  var values = {};
  Object.keys(p).forEach(function (key) {
    if (key === 'form_type') return;
    var label = labelOf(key);
    values[label] = String(p[key]).slice(0, 5000);
    if (headers.indexOf(label) === -1) {
      headers.push(label);
      sh.getRange(1, headers.length).setValue(label).setFontWeight('bold');
    }
  });

  // add the new row (as plain text, so nothing can run as a formula)
  var stamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd HH:mm:ss');
  var row = headers.map(function (h) {
    return h === 'Received at' ? stamp : (values[h] || '');
  });
  var range = sh.getRange(sh.getLastRow() + 1, 1, 1, row.length);
  range.setNumberFormat('@');
  range.setValues([row]);
}

function notify(p, isContact, ss) {
  var to = NOTIFY_EMAIL || Session.getEffectiveUser().getEmail();
  if (!to) return;

  // keep the subject on one line and short (blocks header tricks)
  var one = function (s) { return String(s || '').replace(/[\r\n]+/g, ' ').slice(0, 80); };
  var subject = isContact
    ? 'New enquiry: ' + one(p.name)
    : 'New application: ' + one(p.role) + ' - ' + one(p.full_name);

  var lines = [];
  Object.keys(p).forEach(function (key) {
    if (key === 'form_type') return;
    lines.push(labelOf(key) + ': ' + String(p[key]).slice(0, 2000));
  });
  lines.push('', 'All entries in your Google Sheet: ' + ss.getUrl());

  var options = { to: to, subject: subject, body: lines.join('\n'), name: 'DigiLab Website' };
  // so you can just press "Reply" in Gmail to answer the person
  if (/^[^\s@,;]+@[^\s@,;]+\.[^\s@,;]+$/.test(String(p.email || ''))) options.replyTo = p.email;
  MailApp.sendEmail(options);
}

// Run this ONCE from the editor (pick "testEmail" in the function list, press Run).
// It asks for the email permission and sends you a sample notification.
// It does not add anything to the Sheet.
function testEmail() {
  notify({
    form_type: 'application',
    role: 'Test Role',
    full_name: 'Test Person',
    email: 'test@example.com',
    message: 'This is a test notification from your DigiLab Google Sheet.'
  }, false, SpreadsheetApp.getActiveSpreadsheet());
}
