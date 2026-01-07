function saveUnreadGmailAttachmentsToDrive() {

  const ROOT_FOLDER_NAME = "Fitness_Challenge_Attachments";

  // 🔹 Only unread emails (inline images are NOT "attachments")
  const GMAIL_QUERY = 'is:unread';

  const threads = GmailApp.search(GMAIL_QUERY);
  if (threads.length === 0) return;

  const rootFolder = getOrCreateFolder_(ROOT_FOLDER_NAME);

  threads.forEach(thread => {
    const messages = thread.getMessages();

    messages.forEach(message => {
      if (!message.isUnread()) return;

      // ✅ Get attachments + inline images
      const attachments = message.getAttachments({
        includeInlineImages: true,
        includeAttachments: true
      });

      if (attachments.length === 0) return;

      const fromEmail = extractEmail_(message.getFrom());
      const date = message.getDate();

      const dateFolderName = Utilities.formatDate(
        date,
        Session.getScriptTimeZone(),
        "yyyy-MM-dd"
      );

      const dateFolder = getOrCreateSubFolder_(rootFolder, dateFolderName);

      const timeStamp = Utilities.formatDate(
        date,
        Session.getScriptTimeZone(),
        "yyyyMMdd_HHmmss"
      );

      attachments.forEach((att, index) => {

        // ✅ Only save images
        const contentType = att.getContentType();
        if (!contentType || !contentType.startsWith("image/")) return;

        const extension = contentType.split('/')[1] || 'png';

        const originalName = att.getName()
          ? att.getName().replace(/[^\w.\-]/g, '_')
          : `inline_image_${index + 1}.${extension}`;

        const fileName = `${fromEmail}_${timeStamp}_${originalName}`;

        dateFolder.createFile(att.copyBlob()).setName(fileName);
      });

      // ✅ Mark message as READ after saving
      message.markRead();
    });
  });
}

/* ================= HELPERS ================= */

function getOrCreateFolder_(name) {
  const folders = DriveApp.getFoldersByName(name);
  return folders.hasNext() ? folders.next() : DriveApp.createFolder(name);
}

function getOrCreateSubFolder_(parent, name) {
  const folders = parent.getFoldersByName(name);
  return folders.hasNext() ? folders.next() : parent.createFolder(name);
}

function extractEmail_(from) {
  const match = from.match(/<(.+?)>/);
  return match ? match[1] : from.replace(/\s+/g, '');
}

