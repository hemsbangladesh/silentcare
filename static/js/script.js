function copy_text_to_clipboard(element)
{
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val($(element).text()).select();
  document.execCommand("copy");
  $temp.remove();

	return false;
}

function is_valid_url(string)
{
	var res = string.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g);
	if (res == null)
	{
		return false;
	}
	else
	{
		return true;
	}
};

/** START: Upload files to Cloudflare.com */
/**
 * Helper to get video dimensions
 */
function getVideoDimensions(file) {
    return new Promise((resolve) => {
        const video = document.createElement('video');
        video.preload = 'metadata';
        video.onloadedmetadata = function() {
            window.URL.revokeObjectURL(video.src);
            resolve({ width: video.videoWidth, height: video.videoHeight });
        };
        video.src = URL.createObjectURL(file);
    });
}

async function uploadFile(file, barId, config = {}) {
    const { 
        directory = "uploads", 
        allowedExt = null, 
        csrfToken = "", 
        apiUrl = "",
        check4K = false 
    } = config;

    try {
		const { directory, allowedExt, check4K, csrfToken, apiUrl } = config;
		const $progressBar = $(`#${barId}`);
		const fileName = file.name.toLowerCase();
        const dirName = directory.toLowerCase(); // Ensure directory name is available

		// 1. Extension Check
		if (allowedExt && !fileName.endsWith('.' + allowedExt.toLowerCase())) {
			$progressBar.addClass('bg-warning').text(`Rejected: Must be .${allowedExt}`);
			return;
		}

        // 2. Directory Name Check
        // This checks if the filename contains the directory name anywhere in it
        // This check will also check whether the file is not "mp4" type
        if (allowedExt !== "mp4" && !fileName.includes(dirName)) {
            $progressBar.addClass('bg-danger').text(`Rejected: File name must contain "${directory}"`);
            return;
        }

		// 3. 4K Check (Only runs if file is a video AND check4K is true)
		if (check4K && file.type.startsWith('video/')) {
			const dims = await getVideoDimensions(file);
			const is4K = (dims.width === 3840 && dims.height === 2160) || 
						(dims.width === 2160 && dims.height === 3840);

			if (!is4K) {
				$progressBar.addClass('bg-danger').text('Rejected: Not 4K Resolution');
				return;
			}
		}

        // 4. Get Presigned URL from Django
        const res = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
            body: JSON.stringify({ directory, filename: file.name, filetype: file.type })
        });
        
        const data = await res.json();
        if (!data.url) throw new Error("Upload URL generation failed");

        // 5. PUT to Cloudflare
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            xhr.open('PUT', data.url, true);
            xhr.setRequestHeader('Content-Type', file.type);

            xhr.upload.onprogress = (e) => {
                if (e.lengthComputable) {
                    const percent = Math.round((e.loaded / e.total) * 100);
                    $progressBar.css('width', percent + '%').text(percent + '%');
                }
            };

            xhr.onload = () => xhr.status === 200 ? resolve() : reject();
            xhr.onerror = () => reject();
            xhr.send(file);
        });
    } catch (err) {
        $(`#${barId}`).addClass('bg-danger').text('Error');
        throw err;
    }
}
/** END: Upload files to Cloudflare.com */