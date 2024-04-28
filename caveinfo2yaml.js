/**
 * @param {string} text 
 * @param {string} filename 
 */
function downloadTextAsFile(text, filename) {
    const blob = new Blob([text], {type: "text/plain"});
    const downloadLink = document.createElement("a");
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(blob);
    downloadLink.click();
}

$(() => {
    $('#file-upload').on('change', event => {
        const file = event.target.files[0];
        if(file){
            const reader = new FileReader();
            reader.onload = e => {
                const fileContent = e.target.result;
                $("#input-area").val(fileContent);
            };
            reader.readAsText(file);
        }
    });
    $('#download-button').on('click', () => {
        if($("#output-area").val() != ''){
            downloadTextAsFile($("#output-area").val(), 'caveinfo.yaml');
        }
    });
    $('#copy-button').on('click', () => {
        navigator.clipboard.writeText($("#output-area").val());
        alert('Copied!');
    });
    $('#clear-button').on('click', () => {
        $("#input-area").val('');
        $("#output-area").val('');
    });
});