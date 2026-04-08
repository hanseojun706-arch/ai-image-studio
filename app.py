<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI Image Generator</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(135deg, #0f172a, #1e293b);
      color: white;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    header {
      width: 100%;
      padding: 15px 30px;
      background: rgba(255,255,255,0.05);
      backdrop-filter: blur(10px);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    header h2 {
      margin: 0;
    }

    .container {
      margin-top: 80px;
      text-align: center;
      width: 90%;
      max-width: 600px;
    }

    h1 {
      font-size: 2.5rem;
      margin-bottom: 10px;
    }

    p {
      color: #cbd5f5;
    }

    .input-box {
      margin-top: 30px;
      display: flex;
      gap: 10px;
    }

    input {
      flex: 1;
      padding: 14px;
      border-radius: 10px;
      border: none;
      outline: none;
      font-size: 16px;
    }

    button {
      padding: 14px 20px;
      border-radius: 10px;
      border: none;
      background: #22c55e;
      color: white;
      font-weight: bold;
      cursor: pointer;
      transition: 0.3s;
    }

    button:hover {
      background: #16a34a;
    }

    .image-box {
      margin-top: 40px;
    }

    img {
      width: 100%;
      max-width: 400px;
      border-radius: 15px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }

    .loader {
      margin-top: 20px;
      display: none;
    }

    .download-btn {
      margin-top: 15px;
      display: none;
      background: #3b82f6;
    }

    footer {
      margin-top: 80px;
      padding: 20px;
      color: #94a3b8;
      font-size: 14px;
    }
  </style>
</head>
<body>

<header>
  <h2>✨ AI Image Generator</h2>
</header>

<div class="container">
  <h1>Create AI Images Instantly</h1>
  <p>Type your idea and let AI turn it into amazing art</p>

  <div class="input-box">
    <input type="text" id="prompt" placeholder="e.g. futuristic city, anime girl, lion in space">
    <button onclick="generateImage()">Generate</button>
  </div>

  <div class="loader" id="loader">⏳ Generating image...</div>

  <div class="image-box">
    <img id="result" src="">
    <br>
    <button class="download-btn" id="downloadBtn" onclick="downloadImage()">Download</button>
  </div>
</div>

<footer>
  © 2026 AI Generator | Free Tool
</footer>

<script>
  function generateImage() {
    let prompt = document.getElementById("prompt").value;
    let img = document.getElementById("result");
    let loader = document.getElementById("loader");
    let downloadBtn = document.getElementById("downloadBtn");

    if (prompt === "") {
      alert("Please enter a prompt");
      return;
    }

    loader.style.display = "block";
    downloadBtn.style.display = "none";
    img.src = "";

    let url = "https://image.pollinations.ai/prompt/" + encodeURIComponent(prompt);

    setTimeout(() => {
      img.src = url;
      loader.style.display = "none";
      downloadBtn.style.display = "inline-block";
    }, 1500);
  }

  function downloadImage() {
    let img = document.getElementById("result").src;
    let a = document.createElement("a");
    a.href = img;
    a.download = "ai-image.png";
    a.click();
  }
</script>

</body>
</html>
