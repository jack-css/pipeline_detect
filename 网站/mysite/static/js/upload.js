document.getElementById("download_data").addEventListener("click", function () {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'upload/load');
    xhr.responseType = 'arraybuffer'; // 将响应类型更改为arraybuffer
    xhr.onload = function () {
        if (xhr.status === 200) {
            const arrayBuffer = xhr.response;
            const contentType = xhr.getResponseHeader('Content-Type');

            const contentDisposition = xhr.getResponseHeader('Content-Disposition');
            const filename = contentDisposition.split('\'')[1];
            const decoder = new TextDecoder('utf-8');
            const decodedString = decoder.decode(new Uint8Array(filename.match(/[\da-f]{2}/gi).map(h => parseInt(h, 16)))) + contentDisposition.split('\'')[2];

            const blob = new Blob([arrayBuffer], {type: contentType});

            // 创建下载链接
            const a = document.createElement('a');
            const url = window.URL.createObjectURL(blob);
            a.href = url;
            a.download = decodedString;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        }
    };
    xhr.send();
});
