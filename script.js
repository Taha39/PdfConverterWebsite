// DOM Elements
const navLinks = document.querySelectorAll('.nav-link');
const toolCards = document.querySelectorAll('.tool-card');
//const homeSection = document.getElementById('home-section');  //M.T: In index.html uncomment home-section section before uncommenting this line
const toolsSection = document.getElementById('tools-section');
const converterSection = document.getElementById('converter-section');
const backBtn = document.getElementById('back-btn');
const getStartedBtn = document.getElementById('get-started-btn');
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const browseBtn = document.getElementById('browse-btn');
const fileList = document.getElementById('file-list');
const fileTypes = document.getElementById('file-types');
const optionsSection = document.getElementById('options-section');
const convertBtn = document.getElementById('convert-btn');
const progressSection = document.getElementById('progress-section');
const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');
const resultSection = document.getElementById('result-section');
const downloadBtn = document.getElementById('download-btn');
const converterTitle = document.getElementById('converter-title');
const toast = document.getElementById('toast');

// Current tool state
let currentTool = null;
let uploadedFiles = [];
let conversionResult = null;

// Navigation
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const section = link.getAttribute('data-section');
        
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        if (section === 'home') {
            showHome();
        } else if (section === 'tools') {
            showTools();
        }
    });
});

// Tool selection
toolCards.forEach(card => {
    card.addEventListener('click', () => {
        const tool = card.getAttribute('data-tool');
        selectTool(tool);
    });
});

// Back button
backBtn.addEventListener('click', showTools);

// Get started button
//getStartedBtn.addEventListener('click', showTools); //M.T: In index.html uncomment home-section section before uncommenting this line

// File upload handling
browseBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', handleFileSelect);

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('active');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('active');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('active');
    
    if (e.dataTransfer.files.length) {
        handleFiles(e.dataTransfer.files);
    }
});

// Convert button
convertBtn.addEventListener('click', startConversion);

// Download button
//downloadBtn.addEventListener('click', downloadResult);

// Functions
function showHome() {
    //homeSection.style.display = 'block';      //M.T: In index.html uncomment home-section section before uncommenting this line
    toolsSection.style.display = 'none';
    converterSection.style.display = 'none';
}

function showTools() {
    //homeSection.style.display = 'none';
    toolsSection.style.display = 'block';
    converterSection.style.display = 'none';
    resetConverter();
}

function showConverter() {
    //homeSection.style.display = 'none';
    toolsSection.style.display = 'none';
    converterSection.style.display = 'block';
}

function selectTool(tool) {
    currentTool = tool;
    showConverter();
    resetConverter();
    updateConverterUI();
}

function resetConverter() {
    uploadedFiles = [];
    fileList.innerHTML = '';
    convertBtn.disabled = true;
    progressSection.style.display = 'none';
    resultSection.style.display = 'none';
    fileInput.value = '';
    conversionResult = null;
}

function updateConverterUI() {
    // Update title
    const toolNames = {
        'image-to-pdf': 'Image to PDF',
        'word-to-pdf': 'Word to PDF',
        'excel-to-pdf': 'Excel to PDF',
        'txt-to-pdf': 'Text to PDF',
        'pdf-to-image': 'PDF to Image',
        'pdf-to-word': 'PDF to Word',
        'compress-pdf': 'Compress PDF',
        'pdf-to-editable': 'Make PDF Editable',
        'split-pdf': 'Split PDF',
        'merge-pdf': 'Merge PDF'
    };
    
    converterTitle.textContent = toolNames[currentTool] || 'Converter';
    
    // Update file types
    const fileTypeText = {
        'image-to-pdf': 'Supported formats: JPG, PNG, GIF, BMP, WEBP',
        'word-to-pdf': 'Supported formats: DOC, DOCX',
        'excel-to-pdf': 'Supported formats: XLS, XLSX',
        'txt-to-pdf': 'Supported formats: TXT',
        'pdf-to-image': 'Supported formats: PDF',
        'pdf-to-word': 'Supported formats: PDF',
        'compress-pdf': 'Supported formats: PDF',
        'pdf-to-editable': 'Supported formats: PDF',
        'split-pdf': 'Supported formats: PDF',
        'merge-pdf': 'Supported formats: PDF'
    };
    
    fileTypes.textContent = fileTypeText[currentTool] || 'Supported formats: Various';
    
    // Update options
    //updateOptions();  // M.T: Uncomment this to get more options for pdf operations
    updateOptionsEdit();
}

function updateOptionsEdit(){
    let optionsHTML = '';
    
    switch(currentTool) {
        case 'compress-pdf':
            optionsHTML = `
                <div class="option-group">
                    <label for="compression-level">Compression Level</label>
                    <select id="compression-level">
                        <option value="high">High Compression (Smaller file, lower quality)</option>
                        <option value="medium" selected>Medium Compression (Balanced size and quality)</option>
                        <option value="low">Low Compression (Larger file, best quality)</option>
                    </select>
                </div>
                <!--<div class="option-group">
                    <label for="image-quality">Image Quality</label>
                    <select id="image-quality">
                        <option value="high">High (300 DPI)</option>
                        <option value="medium">Medium (150 DPI)</option>
                        <option value="low">Low (72 DPI)</option>
                    </select>
                </div>
                <div class="option-group">
                    <label for="optimize-images">
                        <input type="checkbox" id="optimize-images" checked>
                        Optimize Images
                    </label>
                </div>-->
            `;
            break;
        default:
            // For tools without specific options
            optionsHTML = '<p>No additional options available for this conversion.</p>';
    }
    
    optionsSection.innerHTML = optionsHTML;
}

function updateOptions() {
    let optionsHTML = '';
    
    switch(currentTool) {
        case 'image-to-pdf':
            optionsHTML = `
                <div class="option-group">
                    <label for="layout">Layout</label>
                    <select id="layout">
                        <option value="single">Single image per page</option>
                        <option value="multiple">Multiple images per page</option>
                    </select>
                </div>
                <div class="option-group">
                    <label for="orientation">Page Orientation</label>
                    <select id="orientation">
                        <option value="portrait">Portrait</option>
                        <option value="landscape">Landscape</option>
                        <option value="auto">Auto (based on images)</option>
                    </select>
                </div>
                <div class="option-group">
                    <label for="image-quality">Image Quality</label>
                    <select id="image-quality">
                        <option value="high">High (300 DPI)</option>
                        <option value="medium">Medium (150 DPI)</option>
                        <option value="low">Low (72 DPI)</option>
                    </select>
                </div>
            `;
            break;
            
        case 'split-pdf':
            optionsHTML = `
                <div class="option-group">
                    <label for="split-method">Split Method</label>
                    <select id="split-method">
                        <option value="range">By page range</option>
                        <option value="every">Every page</option>
                        <option value="odd-even">Odd/Even pages</option>
                    </select>
                </div>
                <div class="option-group" id="page-range-group">
                    <label for="page-range">Page Range (e.g., 1-3,5,7-9)</label>
                    <input type="text" id="page-range" placeholder="1-5">
                </div>
            `;
            break;
            
        case 'pdf-to-image':
            optionsHTML = `
                <div class="option-group">
                    <label for="image-format">Image Format</label>
                    <select id="image-format">
                        <option value="png">PNG</option>
                        <option value="jpg">JPG</option>
                        <option value="webp">WEBP</option>
                    </select>
                </div>
                <div class="option-group">
                    <label for="image-quality">Image Quality</label>
                    <select id="image-quality">
                        <option value="high">High</option>
                        <option value="medium">Medium</option>
                        <option value="low">Low</option>
                    </select>
                </div>
                <div class="option-group">
                    <label for="pages">Pages to Convert</label>
                    <select id="pages">
                        <option value="all">All pages</option>
                        <option value="range">Page range</option>
                        <option value="current">Current page only</option>
                    </select>
                </div>
            `;
            break;
            
        case 'pdf-to-editable':
            optionsHTML = `
                <div class="option-group">
                    <label for="ocr-language">OCR Language</label>
                    <select id="ocr-language">
                        <option value="english">English</option>
                        <option value="spanish">Spanish</option>
                        <option value="french">French</option>
                        <option value="german">German</option>
                        <option value="chinese">Chinese</option>
                    </select>
                </div>
                <div class="option-group">
                    <label for="ocr-quality">OCR Quality</label>
                    <select id="ocr-quality">
                        <option value="high">High (slower)</option>
                        <option value="medium">Medium</option>
                        <option value="low">Low (faster)</option>
                    </select>
                </div>
            `;
            break;

        case 'merge-pdf':
            optionsHTML = `
                <div class="option-group">
                    <label for="merge-order">Merge Order</label>
                    <select id="merge-order">
                        <option value="filename">By filename</option>
                        <option value="upload">By upload order</option>
                        <option value="custom">Custom order</option>
                    </select>
                </div>
            `;
            break;
            
        default:
            // For tools without specific options
            optionsHTML = '<p>No additional options available for this conversion.</p>';
    }
    
    optionsSection.innerHTML = optionsHTML;
}

function handleFileSelect(e) {
    const files = e.target.files;
    handleFiles(files);
}

function handleFiles(files) {
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        
        // Validate file type based on current tool
        if (validateFileType(file)) {
            uploadedFiles.push(file);
            addFileToList(file);
        } else {
            showToast(`File type not supported for ${currentTool} conversion`, 'error');
        }
    }
    
    // Enable convert button if we have files
    convertBtn.disabled = uploadedFiles.length === 0;
}

function validateFileType(file) {
    const fileName = file.name.toLowerCase();
    
    switch(currentTool) {
        case 'image-to-pdf':
            return /\.(jpg|jpeg|png|gif|bmp|webp)$/i.test(fileName);
        case 'word-to-pdf':
            return /\.(doc|docx)$/i.test(fileName);
        case 'excel-to-pdf':
            return /\.(xls|xlsx)$/i.test(fileName);
        case 'txt-to-pdf':
            return /\.(txt)$/i.test(fileName);
        case 'pdf-to-image':
        case 'pdf-to-word':
        case 'compress-pdf':
        case 'pdf-to-editable':
        case 'split-pdf':
        case 'merge-pdf':
            return /\.(pdf)$/i.test(fileName);
        default:
            return false;
    }
}

function addFileToList(file) {
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    
    fileItem.innerHTML = `
        <div class="file-name">
            <span>📄</span>
            <span>${file.name} (${formatFileSize(file.size)})</span>
        </div>
        <button class="remove-file" data-name="${file.name}">×</button>
    `;
    
    fileList.appendChild(fileItem);
    
    // Add event listener to remove button
    const removeBtn = fileItem.querySelector('.remove-file');
    removeBtn.addEventListener('click', () => {
        removeFile(file.name);
        fileItem.remove();
    });
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function removeFile(fileName) {
    uploadedFiles = uploadedFiles.filter(file => file.name !== fileName);
    convertBtn.disabled = uploadedFiles.length === 0;
}

// Function to show buffering indicator
function showBufferingIndicator() {
    // Hide progress section if it was visible
    if (progressSection) {
        progressSection.style.display = 'none';
    }
    
    // Create or show buffering element
    let bufferingElement = document.getElementById('buffering-indicator');
    if (!bufferingElement) {
        bufferingElement = document.createElement('div');
        bufferingElement.id = 'buffering-indicator';
        bufferingElement.innerHTML = `
            <div class="buffering-container">
                <div class="spinner"></div>
                <p>Processing your files... Please wait</p>
            </div>
        `;
        document.body.appendChild(bufferingElement);
    }
    
    bufferingElement.style.display = 'flex';
}

// Function to hide buffering indicator
function hideBufferingIndicator() {
    const bufferingElement = document.getElementById('buffering-indicator');
    if (bufferingElement) {
        bufferingElement.style.display = 'none';
    }

    resetConverter()
    // Show result
    setTimeout(() => {
        conversionComplete();
    }, 500);
}

//Pop up after successful downloading and deleting the server file....
// function showToast(message, type = 'info') {
//     // Create toast element
//     const toast = document.createElement('div');
//     toast.className = `toast toast-${type}`;
//     toast.innerHTML = `
//         <div class="toast-content">
//             <span class="toast-message">${message}</span>
//             <button class="toast-close" onclick="this.parentElement.parentElement.remove()">×</button>
//         </div>
//     `;
    
//     // Add to page
//     document.body.appendChild(toast);
    
//     // Show toast with animation
//     setTimeout(() => toast.classList.add('show'), 100);
    
//     // Remove after 2 seconds
//     setTimeout(() => {
//         toast.classList.remove('show');
//         setTimeout(() => {
//             if (toast.parentNode) {
//                 toast.parentNode.removeChild(toast);
//             }
//         }, 300);
//     }, 2000);
// }

// Remove or modify your existing progress update function
function updateProgress(percent) {
    // You can remove this function or keep it for other uses
    console.log(`Progress: ${percent}%`);
}


// ACTUAL CONVERSION BUSINESS LOGIC
async function startConversion() {
    if (uploadedFiles.length === 0) {
        showToast('Please upload files first', 'error');
        return;
    }
	
	for (let file of uploadedFiles) {
		console.log("File name: "+file.name);
	}

    // Show progress section
    progressSection.style.display = 'block';
    convertBtn.disabled = true;

    try {
        let progress = 0;
        
        // Simulate initial processing
        const progressInterval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress >= 90) {
                progress = 90;
                clearInterval(progressInterval);
            }
            updateProgress(progress);
        }, 200);

        // Show buffering indicator immediately
        showBufferingIndicator();

        // Perform actual conversion based on tool
        conversionResult = await performConversion(uploadedFiles);

    } catch (error) {
        showToast(`Conversion failed: ${error.message}`, 'error');
        resetProgress();
    }
}

async function performConversion(files) {
    switch(currentTool) {
        case 'image-to-pdf':
            return await convertImagesToPDF(files);
        case 'word-to-pdf':
            return await convertWordToPDF(files);
        case 'excel-to-pdf':
            return await convertExcelToPDF(files);
        case 'txt-to-pdf':
            return await convertTextToPDF(files);
        case 'pdf-to-image':
            return await convertPDFToImages(files);
        case 'pdf-to-word':
            return await convertPDFToWord(files);
        case 'compress-pdf':
            return await compressPDF(files);
        case 'pdf-to-editable':
            return await makePDFEditable(files);
        case 'split-pdf':
            return await splitPDF(files);
        case 'merge-pdf':
            return await mergePDFs(files);
        default:
            throw new Error('Unsupported conversion type');
    }
}

// Conversion implementations
async function convertImagesToPDF(files) {
	
	const formData = new FormData();

	for (const file of files) {
	  formData.append('files[]', file);
	}

	fetch('http://localhost:5000/image_to_pdf', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		const pdfFilename = data.pdf_filename;
		const pdfFoldername = data.folder_name;
		// Create URL with query parameters
		const params = new URLSearchParams({
		  fileName: pdfFilename,
		  folderName: pdfFoldername
		});
		// Now do the GET to actually fetch and download the file:
		fetch(`http://localhost:5000/download_pdf?${params.toString()}`)
		.then(resp => resp.blob())
		.then(blob => {
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = pdfFilename; // Will set to what server provided!
			document.body.appendChild(a);
			a.click();
			a.remove();
			window.URL.revokeObjectURL(url);
			
            hideBufferingIndicator()
			fetch('http://localhost:5000/delete_file', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ folderName: pdfFoldername })  // Pass the filename here
			})
			.then(response => response.json())
			.then(data => {
                //showToast('Conversion completed successfully! Look into download folder.', 'success');
				//console.log(data.message);  // Server response about delete status
			})
			.catch(err => {
				console.error('Error deleting file:', err);
			});
		});
	})
	.catch(err => {
		console.error('Error:', err);
	});
}

async function convertWordToPDF(files) {
    const formData = new FormData();

	for (const file of files) {
	  formData.append('files[]', file);
	}

    fetch('http://localhost:5000/doc_to_pdf', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		const docFilename = data.doc_filename;
		const docFoldername = data.folder_name;
		// Create URL with query parameters
		const params = new URLSearchParams({
		  fileName: docFilename,
		  folderName: docFoldername
		});
		// Now do the GET to actually fetch and download the file:
		fetch(`http://localhost:5000/download_pdf?${params.toString()}`)
		.then(resp => resp.blob())
		.then(blob => {
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = docFilename; // Will set to what server provided!
			document.body.appendChild(a);
			a.click();
			a.remove();
			window.URL.revokeObjectURL(url);
			
            hideBufferingIndicator()
			fetch('http://localhost:5000/delete_file', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ folderName: docFoldername })  // Pass the filename here
			})
			.then(response => response.json())
			.then(data => {
				//console.log(data.message);  // Server response about delete status
			})
			.catch(err => {
				console.error('Error deleting file:', err);
			});
		});
	})
	.catch(err => {
		console.error('Error:', err);
	});
}

async function convertExcelToPDF(files) {

    const formData = new FormData();

	for (const file of files) {
	  formData.append('files[]', file);
	}

    fetch('http://localhost:5000/doc_to_pdf', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		const docFilename = data.doc_filename;
		const docFoldername = data.folder_name;
		// Create URL with query parameters
		const params = new URLSearchParams({
		  fileName: docFilename,
		  folderName: docFoldername
		});
		// Now do the GET to actually fetch and download the file:
		fetch(`http://localhost:5000/download_pdf?${params.toString()}`)
		.then(resp => resp.blob())
		.then(blob => {
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = docFilename; // Will set to what server provided!
			document.body.appendChild(a);
			a.click();
			a.remove();
			window.URL.revokeObjectURL(url);
			
            hideBufferingIndicator()
			fetch('http://localhost:5000/delete_file', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ folderName: docFoldername })  // Pass the filename here
			})
			.then(response => response.json())
			.then(data => {
				//console.log(data.message);  // Server response about delete status
			})
			.catch(err => {
				console.error('Error deleting file:', err);
			});
		});
	})
	.catch(err => {
		console.error('Error:', err);
	});
}

async function convertTextToPDF(files) {

    const formData = new FormData();

	for (const file of files) {
	  formData.append('files[]', file);
	}

    fetch('http://localhost:5000/txt_to_pdf', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		const txtFilename = data.txt_filename;
		const docFoldername = data.folder_name;
		// Create URL with query parameters
		const params = new URLSearchParams({
		  fileName: txtFilename,
		  folderName: docFoldername
		});
		// Now do the GET to actually fetch and download the file:
		fetch(`http://localhost:5000/download_pdf?${params.toString()}`)
		.then(resp => resp.blob())
		.then(blob => {
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = txtFilename; // Will set to what server provided!
			document.body.appendChild(a);
			a.click();
			a.remove();
			window.URL.revokeObjectURL(url);
			
            hideBufferingIndicator()
			fetch('http://localhost:5000/delete_file', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ folderName: docFoldername })  // Pass the filename here
			})
			.then(response => response.json())
			.then(data => {
				//console.log(data.message);  // Server response about delete status
			})
			.catch(err => {
				console.error('Error deleting file:', err);
			});
		});
	})
	.catch(err => {
		console.error('Error:', err);
	});
}

async function convertPDFToImages(files) {
    const formData = new FormData();

	for (const file of files) {
	  formData.append('files[]', file);
	}

    fetch('http://localhost:5000/pdf_to_img', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		const pdfFilename = data.pdf_filename;
		const docFoldername = data.folder_name;
		// Create URL with query parameters
		const params = new URLSearchParams({
		  fileName: pdfFilename,
		  folderName: docFoldername
		});
		// Now do the GET to actually fetch and download the file:
		fetch(`http://localhost:5000/download_pdf?${params.toString()}`)
		.then(resp => resp.blob())
		.then(blob => {
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = pdfFilename; // Will set to what server provided!
			document.body.appendChild(a);
			a.click();
			a.remove();
			window.URL.revokeObjectURL(url);
			
            hideBufferingIndicator()
			fetch('http://localhost:5000/delete_file', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ folderName: docFoldername })  // Pass the filename here
			})
			.then(response => response.json())
			.then(data => {
				//console.log(data.message);  // Server response about delete status
			})
			.catch(err => {
				console.error('Error deleting file:', err);
			});
		});
	})
	.catch(err => {
		console.error('Error:', err);
	});
}

async function convertPDFToWord(files) {

    const formData = new FormData();

	for (const file of files) {
	  formData.append('files[]', file);
	}

    fetch('http://localhost:5000/pdf_to_doc', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		const docFilename = data.doc_filename;
		const docFoldername = data.folder_name;
		// Create URL with query parameters
		const params = new URLSearchParams({
		  fileName: docFilename,
		  folderName: docFoldername
		});
		// Now do the GET to actually fetch and download the file:
		fetch(`http://localhost:5000/download_pdf?${params.toString()}`)
		.then(resp => resp.blob())
		.then(blob => {
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = docFilename; // Will set to what server provided!
			document.body.appendChild(a);
			a.click();
			a.remove();
			window.URL.revokeObjectURL(url);
			
            hideBufferingIndicator()
			fetch('http://localhost:5000/delete_file', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ folderName: docFoldername })  // Pass the filename here
			})
			.then(response => response.json())
			.then(data => {
				//console.log(data.message);  // Server response about delete status
			})
			.catch(err => {
				console.error('Error deleting file:', err);
			});
		});
	})
	.catch(err => {
		console.error('Error:', err);
	});
}

async function makePDFEditable() {
    const language = document.getElementById('ocr-language')?.value || 'english';
    const quality = document.getElementById('ocr-quality')?.value || 'medium';

    const pdfFile = uploadedFiles[0];
    
    // Simulate OCR process for making PDF editable
    const editablePDF = {
        type: 'application/pdf',
        fileName: `editable_${pdfFile.name}`,
        content: `Editable PDF created from: ${pdfFile.name}`,
        metadata: {
            ocrLanguage: language,
            ocrQuality: quality,
            searchable: true,
            selectableText: true
        }
    };

    // OCR takes longer
    await simulateProcessing(5000);
    return editablePDF;
}

async function splitPDF(files) {

    const formData = new FormData();

	for (const file of files) {
	  formData.append('files[]', file);
	}

    fetch('http://localhost:5000/split_pdf', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
        console.log('data: ', data)
		const splitFilename = data.split_filename;
		const docFoldername = data.folder_name;
		// Create URL with query parameters
		const params = new URLSearchParams({
		  fileName: splitFilename,
		  folderName: docFoldername
		});
		// Now do the GET to actually fetch and download the file:
		fetch(`http://localhost:5000/download_pdf?${params.toString()}`)
		.then(resp => resp.blob())
		.then(blob => {
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = splitFilename; // Will set to what server provided!
			document.body.appendChild(a);
			a.click();
			a.remove();
			window.URL.revokeObjectURL(url);
			
            hideBufferingIndicator()
			fetch('http://localhost:5000/delete_file', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ folderName: docFoldername })  // Pass the filename here
			})
			.then(response => response.json())
			.then(data => {
				//console.log(data.message);  // Server response about delete status
			})
			.catch(err => {
				console.error('Error deleting file:', err);
			});
		});
	})
	.catch(err => {
		console.error('Error:', err);
	});
}

async function mergePDFs(files) {

    const formData = new FormData();

	for (const file of files) {
	  formData.append('files[]', file);
	}

    fetch('http://localhost:5000/merge_pdf', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
        console.log('data: ', data)
		const mergeFilename = data.merged_filename;
		const docFoldername = data.folder_name;
		// Create URL with query parameters
		const params = new URLSearchParams({
		  fileName: mergeFilename,
		  folderName: docFoldername
		});
		// Now do the GET to actually fetch and download the file:
		fetch(`http://localhost:5000/download_pdf?${params.toString()}`)
		.then(resp => resp.blob())
		.then(blob => {
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = mergeFilename; // Will set to what server provided!
			document.body.appendChild(a);
			a.click();
			a.remove();
			window.URL.revokeObjectURL(url);
			
            hideBufferingIndicator()
			fetch('http://localhost:5000/delete_file', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ folderName: docFoldername })  // Pass the filename here
			})
			.then(response => response.json())
			.then(data => {
				//console.log(data.message);  // Server response about delete status
			})
			.catch(err => {
				console.error('Error deleting file:', err);
			});
		});
	})
	.catch(err => {
		console.error('Error:', err);
	});
}

async function compressPDF(files){
    const compressionLevel = document.getElementById('compression-level').value;
    // let quality = 70;
    // if (compressionLevel === 'medium'){
    //     quality = 50;
    // } else if (compressionLevel === 'high'){
    //     quality = 10;
    // }

    console.log('Selection compression: ', compressionLevel);
    //console.log('Selection quality: ', quality);

    const formData = new FormData();

	for (const file of files) {
	  formData.append('files[]', file);
	}
    formData.append('compressionLevel', compressionLevel); // ageValue can be a number or string

    fetch('http://localhost:5000/compress_pdf', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
        console.log('data: ', data)
		const compressFilename = data.pdf_filename;
		const docFoldername = data.folder_name;
		// Create URL with query parameters
		const params = new URLSearchParams({
		  fileName: compressFilename,
		  folderName: docFoldername
		});
		// Now do the GET to actually fetch and download the file:
		fetch(`http://localhost:5000/download_pdf?${params.toString()}`)
		.then(resp => resp.blob())
		.then(blob => {
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = compressFilename; // Will set to what server provided!
			document.body.appendChild(a);
			a.click();
			a.remove();
			window.URL.revokeObjectURL(url);
			
            hideBufferingIndicator()
			fetch('http://localhost:5000/delete_file', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ folderName: docFoldername })  // Pass the filename here
			})
			.then(response => response.json())
			.then(data => {
				//console.log(data.message);  // Server response about delete status
			})
			.catch(err => {
				console.error('Error deleting file:', err);
			});
		});
	})
	.catch(err => {
		console.error('Error:', err);
	});
}

// Utility functions
function updateProgress(percentage) {
    progressFill.style.width = `${percentage}%`;
    progressText.textContent = `${Math.round(percentage)}%`;
}

function resetProgress() {
    progressSection.style.display = 'none';
    progressFill.style.width = '0%';
    progressText.textContent = '0%';
    convertBtn.disabled = false;
}

function conversionComplete() {
    progressSection.style.display = 'none';
    resultSection.style.display = 'block';
    showToast('Conversion completed successfully! Look into download folder.', 'success');
}

async function readFileAsText(file) {
    return new Promise((resolve) => {
        // Simulate file reading
        setTimeout(() => {
            resolve(`Content of ${file.name}\n\nThis is a simulated text content for demonstration purposes.`);
        }, 500);
    });
}

async function simulateProcessing(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function downloadResult() {
    if (!conversionResult) {
        showToast('No conversion result available', 'error');
        return;
    }

    // Create and trigger download
    const blob = new Blob([conversionResult.content], { type: conversionResult.type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = conversionResult.fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showToast('File downloaded successfully!', 'success');
    
    // Auto-delete after download (simulated)
    setTimeout(() => {
        resetConverter();
        showTools();
    }, 3000);
}

function getFileExtension() {
    switch(currentTool) {
        case 'image-to-pdf':
        case 'word-to-pdf':
        case 'excel-to-pdf':
        case 'txt-to-pdf':
        case 'pdf-to-editable':
        case 'split-pdf':
        case 'compress-pdf':
        case 'merge-pdf':
            return 'pdf';
        case 'pdf-to-image':
            return document.getElementById('image-format')?.value || 'png';
        case 'pdf-to-word':
            return 'docx';
        default:
            return 'file';
    }
}

function showToast(message, type = '') {
    toast.textContent = message;
    toast.className = 'toast';
    
    if (type) {
        toast.classList.add(type);
    }
    
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Initialize
//showHome(); //M.T: Uncomment this to have GetStarted button before showing all the tools
showTools()