// SIH26034 - Packaged Commodity Compliance Scanner Frontend Logic (Phase 2: OCR Active)

document.addEventListener("DOMContentLoaded", () => {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const dropzonePrompt = document.getElementById("dropzonePrompt");
  const previewContainer = document.getElementById("previewContainer");
  const imagePreview = document.getElementById("imagePreview");
  const fileMeta = document.getElementById("fileMeta");

  const scanBtn = document.getElementById("scanBtn");
  const uploadOnlyBtn = document.getElementById("uploadOnlyBtn");
  const resetBtn = document.getElementById("resetBtn");
  const statusBanner = document.getElementById("statusBanner");
  const statusTitle = document.getElementById("statusTitle");
  const statusDetail = document.getElementById("statusDetail");

  const pipelineStatus = document.getElementById("pipelineStatus");
  const resultsPlaceholder = document.getElementById("resultsPlaceholder");
  const uploadSummary = document.getElementById("uploadSummary");
  const summaryFilename = document.getElementById("summaryFilename");
  const summaryOriginal = document.getElementById("summaryOriginal");
  const summarySize = document.getElementById("summarySize");

  // OCR Results elements
  const ocrResultsContainer = document.getElementById("ocrResultsContainer");
  const metricLineCount = document.getElementById("metricLineCount");
  const metricAvgConf = document.getElementById("metricAvgConf");
  const ocrCountPill = document.getElementById("ocrCountPill");
  const ocrList = document.getElementById("ocrList");
  const rawJsonCode = document.getElementById("rawJsonCode");

  let selectedFile = null;

  // Format file size for human readability
  function formatBytes(bytes, decimals = 2) {
    if (!+bytes) return "0 Bytes";
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
  }

  // Display status banner
  function showStatus(type, title, detail) {
    statusBanner.className = `status-banner ${type}`;
    statusTitle.textContent = title;
    statusDetail.textContent = detail;
    statusBanner.style.display = "flex";
  }

  function hideStatus() {
    statusBanner.style.display = "none";
  }

  // Handle selected file
  function handleFile(file) {
    if (!file) return;

    // Validate type
    const validTypes = ["image/jpeg", "image/png", "image/webp", "image/jpg", "image/bmp", "image/tiff"];
    if (!validTypes.includes(file.type) && !file.name.match(/\.(png|jpg|jpeg|webp|bmp|tiff)$/i)) {
      showStatus("error", "Unsupported File Format", "Please upload a PNG, JPG, JPEG, or WEBP image.");
      return;
    }

    // Validate size (16MB max)
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
      showStatus("error", "File Too Large", "Maximum image size allowed is 16 MB.");
      return;
    }

    selectedFile = file;
    hideStatus();

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.src = e.target.result;
      dropzonePrompt.style.display = "none";
      previewContainer.style.display = "flex";
      fileMeta.textContent = `${file.name} (${formatBytes(file.size)})`;

      scanBtn.disabled = false;
      uploadOnlyBtn.disabled = false;
      resetBtn.disabled = false;
    };
    reader.readAsDataURL(file);
  }

  // Reset form
  function resetAll() {
    selectedFile = null;
    fileInput.value = "";
    imagePreview.src = "";
    dropzonePrompt.style.display = "flex";
    previewContainer.style.display = "none";
    scanBtn.disabled = true;
    uploadOnlyBtn.disabled = true;
    resetBtn.disabled = true;
    hideStatus();

    pipelineStatus.textContent = "Standby";
    pipelineStatus.className = "badge-status badge-idle";
    resultsPlaceholder.style.display = "flex";
    uploadSummary.style.display = "none";
    ocrResultsContainer.style.display = "none";
    ocrList.innerHTML = "";
    rawJsonCode.textContent = "";
  }

  // Click to browse
  dropzone.addEventListener("click", () => {
    if (!selectedFile) {
      fileInput.click();
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  });

  // Drag and drop
  ["dragenter", "dragover"].forEach((eventName) => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove("dragover");
    });
  });

  dropzone.addEventListener("drop", (e) => {
    if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  });

  resetBtn.addEventListener("click", resetAll);

  // 1. Phase 1: Upload Only Action
  uploadOnlyBtn.addEventListener("click", async () => {
    if (!selectedFile) return;

    scanBtn.disabled = true;
    uploadOnlyBtn.disabled = true;
    resetBtn.disabled = true;
    showStatus("info", "Uploading Image...", "Saving package image to local backend server.");
    pipelineStatus.textContent = "Uploading";
    pipelineStatus.className = "badge-status badge-active";

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.status === "success") {
        showStatus("success", "Upload Complete", data.message);
        pipelineStatus.textContent = "Uploaded";
        pipelineStatus.className = "badge-status badge-success";

        summaryFilename.textContent = data.file.filename;
        summaryOriginal.textContent = data.file.original_filename;
        summarySize.textContent = formatBytes(data.file.size_bytes);

        resultsPlaceholder.style.display = "none";
        ocrResultsContainer.style.display = "none";
        uploadSummary.style.display = "flex";
      } else {
        showStatus("error", "Upload Failed", data.message || "Could not upload file.");
        pipelineStatus.textContent = "Error";
        pipelineStatus.className = "badge-status badge-idle";
      }
    } catch (err) {
      showStatus("error", "Network Error", err.message);
      pipelineStatus.textContent = "Error";
      pipelineStatus.className = "badge-status badge-idle";
    } finally {
      resetBtn.disabled = false;
      uploadOnlyBtn.disabled = false;
      scanBtn.disabled = false;
    }
  });

  // 2. Phase 2: Run OCR Scan Action
  scanBtn.addEventListener("click", async () => {
    if (!selectedFile) return;

    scanBtn.disabled = true;
    uploadOnlyBtn.disabled = true;
    resetBtn.disabled = true;

    showStatus("info", "Running OCR & Preprocessing...", "Preprocessing image with OpenCV (CLAHE) and extracting text via PaddleOCR. This may take a few seconds.");
    pipelineStatus.textContent = "Processing OCR";
    pipelineStatus.className = "badge-status badge-active";

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await fetch("/api/ocr", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.status === "success") {
        const results = data.results || [];
        showStatus("success", "OCR Extraction Complete", `Successfully extracted ${results.length} text line(s) from label.`);
        pipelineStatus.textContent = "OCR Complete";
        pipelineStatus.className = "badge-status badge-success";

        // Calculate average confidence
        const avgConf = results.length > 0
          ? (results.reduce((acc, r) => acc + (r.confidence || 0), 0) / results.length) * 100
          : 0;

        metricLineCount.textContent = results.length;
        metricAvgConf.textContent = `${avgConf.toFixed(1)}%`;
        ocrCountPill.textContent = `${results.length} items`;

        // Render OCR items
        ocrList.innerHTML = "";
        if (results.length === 0) {
          ocrList.innerHTML = `
            <div style="text-align:center; padding: 20px; color: var(--text-muted); font-size: 0.88rem;">
              No text detected on the package label. Try uploading a clearer or higher-resolution image.
            </div>
          `;
        } else {
          results.forEach((item, index) => {
            const conf = item.confidence || 0;
            const confPct = Math.round(conf * 100);
            let confClass = "conf-high";
            if (conf < 0.7) {
              confClass = "conf-low";
            } else if (conf < 0.88) {
              confClass = "conf-medium";
            }

            const box = item.box || { x: 0, y: 0, width: 0, height: 0 };
            const itemDiv = document.createElement("div");
            itemDiv.className = "ocr-item";
            itemDiv.innerHTML = `
              <div class="ocr-text-col">
                <span class="ocr-text">${escapeHtml(item.text)}</span>
                <span class="box-chip">Box: X=${box.x}, Y=${box.y}, W=${box.width}, H=${box.height}</span>
              </div>
              <span class="conf-badge ${confClass}">${confPct}% Conf</span>
            `;
            ocrList.appendChild(itemDiv);
          });
        }

        // Render raw JSON
        rawJsonCode.textContent = JSON.stringify(data, null, 2);

        // Toggle UI sections
        resultsPlaceholder.style.display = "none";
        uploadSummary.style.display = "none";
        ocrResultsContainer.style.display = "flex";
      } else {
        const errorMsg = data.message || "Failed to process OCR. Please check image.";
        showStatus("error", "OCR Processing Failed", errorMsg);
        pipelineStatus.textContent = "Error";
        pipelineStatus.className = "badge-status badge-idle";
      }
    } catch (err) {
      showStatus("error", "Network Error", `Could not connect to OCR backend: ${err.message}`);
      pipelineStatus.textContent = "Error";
      pipelineStatus.className = "badge-status badge-idle";
    } finally {
      resetBtn.disabled = false;
      uploadOnlyBtn.disabled = false;
      scanBtn.disabled = false;
    }
  });

  // Utility to prevent XSS in rendered text
  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
});
