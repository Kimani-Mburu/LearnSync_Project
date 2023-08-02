// Custom document viewer function
function openDocument(url) {
    const extension = url.split('.').pop().toLowerCase();
  
    if (extension === 'pdf') {
      // For PDF files, use the "embed" element
      const embedElement = document.createElement('embed');
      embedElement.src = url;
      embedElement.width = '100%';
      embedElement.height = '600px';
      document.getElementById('document-preview').appendChild(embedElement);
    } else if (extension === 'docx') {
      // For DOCX files, use the "iframe" element
      const iframeElement = document.createElement('iframe');
      iframeElement.src = `https://view.officeapps.live.com/op/embed.aspx?src=${url}`;
      iframeElement.width = '100%';
      iframeElement.height = '600px';
      document.getElementById('document-preview').appendChild(iframeElement);
    } else {
      // For other file formats, display a download link
      const downloadLink = document.createElement('a');
      downloadLink.href = url;
      downloadLink.innerText = 'Download Document';
      document.getElementById('document-preview').appendChild(downloadLink);
    }
  }
  
  // Call the document viewer function on page load
  document.addEventListener('DOMContentLoaded', function () {
    const documentUrl = '{{ object.file.url }}';
    openDocument(documentUrl);
  });
  