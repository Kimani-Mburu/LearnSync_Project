function displayPDF() {
    const pdfFile = "{{ object.file.url }}";
    const pdfViewerContainer = document.getElementById("pdfViewerContainer");
    const pdfViewer = document.getElementById("pdfViewer");

    pdfjsLib.getDocument(pdfFile).promise.then(function(pdfDoc) {
        pdfDoc.getPage(1).then(function(page) {
            const viewport = page.getViewport({ scale: 1 });
            const canvas = document.createElement("canvas");
            const context = canvas.getContext("2d");
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            const renderContext = {
                canvasContext: context,
                viewport: viewport,
            };
            page.render(renderContext).promise.then(function() {
                pdfViewer.appendChild(canvas);
            });
        });
    });
}

displayPDF();