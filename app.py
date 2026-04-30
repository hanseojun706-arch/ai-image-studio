<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>Free AI Image Generator | Text to Image & Image to Image</title>

  <meta name="description" content="Generate AI images for free using text prompts. Upload your own image and transform it into anime, realistic, watercolor, fantasy, or cinematic style." />

  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: Arial, sans-serif;
    }

    body {
      background:
        radial-gradient(circle at top left, rgba(168, 85, 247, 0.35), transparent 35%),
        radial-gradient(circle at top right, rgba(59, 130, 246, 0.35), transparent 35%),
        linear-gradient(135deg, #070816, #111827);
      color: white;
      min-height: 100vh;
    }

    header {
      padding: 20px 8%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      backdrop-filter: blur(15px);
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(7, 8, 22, 0.7);
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }

    .logo {
      font-size: 24px;
      font-weight: bold;
      background: linear-gradient(90deg, #c084fc, #60a5fa, #f472b6);
      -webkit-background-clip: text;
      color: transparent;
    }

    nav a {
      color: white;
      text-decoration: none;
      margin-left: 20px;
      font-size: 15px;
      opacity: 0.85;
    }

    nav a:hover {
      opacity: 1;
    }

    .hero {
      padding: 90px 8%;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 40px;
      align-items: center;
    }

    .hero h1 {
      font-size: clamp(42px, 7vw, 76px);
      line-height: 1;
      margin-bottom: 20px;
    }

    .gradient-text {
      background: linear-gradient(90deg, #c084fc, #60a5fa, #f472b6);
      -webkit-background-clip: text;
      color: transparent;
    }

    .hero p {
      color: #c7c7d9;
      font-size: 18px;
      line-height: 1.7;
      margin-bottom: 30px;
    }

    .btn {
      padding: 14px 24px;
      border-radius: 999px;
      border: none;
      cursor: pointer;
      font-weight: bold;
      font-size: 15px;
      margin-right: 10px;
      margin-top: 10px;
    }

    .primary {
      background: linear-gradient(90deg, #8b5cf6, #3b82f6, #ec4899);
      color: white;
      box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
    }

    .secondary {
      background: rgba(255,255,255,0.08);
      color: white;
      border: 1px solid rgba(255,255,255,0.18);
    }

    .glass {
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.16);
      backdrop-filter: blur(18px);
      border-radius: 28px;
      box-shadow: 0 20px 80px rgba(0,0,0,0.25);
    }

    .hero-preview {
      padding: 20px;
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 15px;
    }

    .preview-card {
      height: 180px;
      border-radius: 20px;
      background: linear-gradient(135deg, #8b5cf6, #3b82f6, #ec4899);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: bold;
      text-align: center;
      padding: 20px;
    }

    section {
      padding: 70px 8%;
    }

    .section-title {
      font-size: 40px;
      margin-bottom: 12px;
    }

    .section-subtitle {
      color: #c7c7d9;
      margin-bottom: 30px;
      line-height: 1.6;
    }

    .generator-box {
      padding: 28px;
    }

    textarea,
    input,
    select {
      width: 100%;
      padding: 15px;
      border-radius: 16px;
      border: 1px solid rgba(255,255,255,0.16);
      background: rgba(255,255,255,0.08);
      color: white;
      outline: none;
      margin-top: 10px;
      margin-bottom: 18px;
      font-size: 15px;
    }

    textarea::placeholder,
    input::placeholder {
      color: #a8a8bd;
    }

    select option {
      color: black;
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 18px;
    }

    .result-grid,
    .style-grid,
    .gallery-grid,
    .pricing-grid,
    .faq-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 22px;
      margin-top: 30px;
    }

    .result-card,
    .style-card,
    .gallery-card,
    .pricing-card,
    .faq-card {
      padding: 20px;
      border-radius: 24px;
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.16);
    }

    .fake-image {
      height: 240px;
      border-radius: 18px;
      background:
        linear-gradient(135deg, rgba(139,92,246,0.8), rgba(59,130,246,0.7), rgba(236,72,153,0.8));
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      text-align: center;
      padding: 20px;
      margin-bottom: 15px;
    }

    .upload-box {
      border: 2px dashed rgba(255,255,255,0.25);
      border-radius: 24px;
      padding: 35px;
      text-align: center;
      cursor: pointer;
      margin-bottom: 20px;
    }

    .upload-box:hover {
      background: rgba(255,255,255,0.08);
    }

    .preview-upload {
      max-width: 100%;
      border-radius: 18px;
      margin-top: 18px;
      display: none;
    }

    .notice {
      padding: 18px;
      border-radius: 18px;
      background: rgba(251, 191, 36, 0.12);
      border: 1px solid rgba(251, 191, 36, 0.3);
      color: #fde68a;
      margin-top: 20px;
      line-height: 1.6;
    }

    footer {
      padding: 40px 8%;
      border-top: 1px solid rgba(255,255,255,0.12);
      color: #c7c7d9;
    }

    .footer-links {
      margin-top: 18px;
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
    }

    .footer-links a {
      color: #c7c7d9;
      text-decoration: none;
    }

    .loading {
      display: none;
      color: #93c5fd;
      margin-top: 15px;
    }

    @media (max-width: 700px) {
      header {
        flex-direction: column;
        gap: 15px;
      }

      nav a {
        margin: 8px;
        display: inline-block;
      }

      .hero {
        padding-top: 50px;
      }
    }
  </style>
</head>

<body>

  <header>
    <div class="logo">ImagineArt AI</div>
    <nav>
      <a href="#generator">Generate</a>
      <a href="#image-upload">Image to Image</a>
      <a href="#styles">Styles</a>
      <a href="#pricing">Free Plan</a>
      <a href="#faq">FAQ</a>
    </nav>
  </header>

  <main>

    <section class="hero">
      <div>
        <h1>
          Free <span class="gradient-text">AI Image</span> Generator
        </h1>
        <p>
          Create beautiful AI images from text prompts or upload your own photo and transform it into anime, realistic, watercolor, fantasy, or cinematic style.
        </p>

        <a href="#generator">
          <button class="btn primary">Start Generating Free</button>
        </a>

        <a href="#image-upload">
          <button class="btn secondary">Upload Image</button>
        </a>

        <div class="notice">
          Free version includes daily free generations. Unlimited creative prompts are available, but image generation may depend on fair usage limits.
        </div>
      </div>

      <div class="glass hero-preview">
        <div class="preview-card">Anime Art</div>
        <div class="preview-card">Realistic Portrait</div>
        <div class="preview-card">Watercolor</div>
        <div class="preview-card">Fantasy Style</div>
      </div>
    </section>

    <section id="generator">
      <h2 class="section-title">Text to Image Generator</h2>
      <p class="section-subtitle">
        Type your idea, choose a style, select aspect ratio, and generate AI artwork.
      </p>

      <div class="glass generator-box">
        <label>Enter Your Prompt</label>
        <textarea id="promptInput" rows="5" placeholder="Example: cute anime girl in cozy kitchen, warm lighting, soft lofi anime style"></textarea>

        <div class="form-grid">
          <div>
            <label>Style</label>
            <select id="styleSelect">
              <option>Anime</option>
              <option>Soft Lofi Anime</option>
              <option>Ghibli-inspired Cozy</option>
              <option>Realistic</option>
              <option>Watercolor</option>
              <option>Cinematic</option>
              <option>Fantasy</option>
              <option>Product Photography</option>
            </select>
          </div>

          <div>
            <label>Aspect Ratio</label>
            <select id="ratioSelect">
              <option>1:1</option>
              <option>16:9</option>
              <option>9:16</option>
              <option>4:5</option>
            </select>
          </div>

          <div>
            <label>Quality</label>
            <select id="qualitySelect">
              <option>Standard</option>
              <option>High</option>
              <option>Ultra</option>
            </select>
          </div>

          <div>
            <label>Number of Images</label>
            <select id="countSelect">
              <option>1</option>
              <option>2</option>
              <option>4</option>
            </select>
          </div>
        </div>

        <button class="btn primary" onclick="generateImage()">Generate Image</button>
        <button class="btn secondary" onclick="enhancePrompt()">Enhance Prompt</button>

        <p id="loadingText" class="loading">Creating your image...</p>

        <div id="resultGrid" class="result-grid"></div>
      </div>
    </section>

    <section id="image-upload">
      <h2 class="section-title">Image to Image AI Tool</h2>
      <p class="section-subtitle">
        Upload your own image and transform it with a new AI style.
      </p>

      <div class="glass generator-box">
        <label class="upload-box">
          <strong>Click to upload image</strong>
          <p style="color:#c7c7d9; margin-top:10px;">Supported: JPG, PNG, WebP</p>
          <input type="file" id="imageUpload" accept="image/png, image/jpeg, image/webp" hidden onchange="previewImage(event)" />
        </label>

        <img id="uploadedPreview" class="preview-upload" />

        <label>Transformation Prompt</label>
        <textarea id="transformPrompt" rows="4" placeholder="Example: Turn this image into a soft cozy anime illustration"></textarea>

        <div class="form-grid">
          <div>
            <label>Transform Style</label>
            <select id="transformStyle">
              <option>Soft Lofi Anime</option>
              <option>Realistic Portrait</option>
              <option>Watercolor</option>
              <option>Cartoon</option>
              <option>Cinematic</option>
              <option>Fantasy</option>
              <option>Sketch</option>
            </select>
          </div>

          <div>
            <label>Strength</label>
            <select id="strengthSelect">
              <option>Low</option>
              <option>Medium</option>
              <option>High</option>
            </select>
          </div>
        </div>

        <button class="btn primary" onclick="transformImage()">Transform Image</button>

        <div id="transformResult" class="result-grid"></div>
      </div>
    </section>

    <section id="styles">
      <h2 class="section-title">AI Style Presets</h2>
      <p class="section-subtitle">
        Choose from popular AI image styles for faster creation.
      </p>

      <div class="style-grid">
        <div class="style-card">
          <div class="fake-image">Anime</div>
          <h3>Anime</h3>
          <button class="btn secondary">Use Style</button>
        </div>

        <div class="style-card">
          <div class="fake-image">Soft Lofi Anime</div>
          <h3>Soft Lofi Anime</h3>
          <button class="btn secondary">Use Style</button>
        </div>

        <div class="style-card">
          <div class="fake-image">Ghibli-inspired Cozy</div>
          <h3>Ghibli-inspired Cozy</h3>
          <button class="btn secondary">Use Style</button>
        </div>

        <div class="style-card">
          <div class="fake-image">Realistic</div>
          <h3>Realistic Portrait</h3>
          <button class="btn secondary">Use Style</button>
        </div>

        <div class="style-card">
          <div class="fake-image">Fantasy</div>
          <h3>Fantasy Art</h3>
          <button class="btn secondary">Use Style</button>
        </div>

        <div class="style-card">
          <div class="fake-image">Product Photo</div>
          <h3>Product Photography</h3>
          <button class="btn secondary">Use Style</button>
        </div>
      </div>
    </section>

    <section id="gallery">
      <h2 class="section-title">My AI Art Gallery</h2>
      <p class="section-subtitle">
        Your generated images will appear here.
      </p>

      <div id="galleryGrid" class="gallery-grid">
        <div class="gallery-card">
          <div class="fake-image">No images yet</div>
          <p>Create your first AI image above.</p>
        </div>
      </div>
    </section>

    <section id="pricing">
      <h2 class="section-title">Free Version Features</h2>
      <p class="section-subtitle">
        Start free with daily credits and creative prompt tools.
      </p>

      <div class="pricing-grid">
        <div class="pricing-card">
          <h3>Free Plan</h3>
          <h2>₹0</h2>
          <p>Best for beginners and creators.</p>
          <ul style="line-height:2; margin-top:15px; padding-left:20px;">
            <li>Text to image generation</li>
            <li>Image upload support</li>
            <li>Image-to-image tool</li>
            <li>Style presets</li>
            <li>Download images</li>
            <li>Daily free credits</li>
            <li>Prompt enhancer</li>
          </ul>
          <button class="btn primary">Start Free</button>
        </div>

        <div class="pricing-card">
          <h3>Premium</h3>
          <h2>Coming Soon</h2>
          <p>For heavy users and professionals.</p>
          <ul style="line-height:2; margin-top:15px; padding-left:20px;">
            <li>More daily credits</li>
            <li>HD downloads</li>
            <li>Faster generation</li>
            <li>Private gallery</li>
            <li>No watermark</li>
            <li>Priority processing</li>
          </ul>
          <button class="btn secondary">Notify Me</button>
        </div>
      </div>
    </section>

    <section id="faq">
      <h2 class="section-title">FAQ</h2>

      <div class="faq-grid">
        <div class="faq-card">
          <h3>Is this AI image generator free?</h3>
          <p>Yes, it includes a free version with daily free credits.</p>
        </div>

        <div class="faq-card">
          <h3>Can I upload my own image?</h3>
          <p>Yes, users can upload JPG, PNG, or WebP images.</p>
        </div>

        <div class="faq-card">
          <h3>Can I make anime images?</h3>
          <p>Yes, you can choose Anime, Soft Lofi Anime, and cozy anime styles.</p>
        </div>

        <div class="faq-card">
          <h3>Is it unlimited free?</h3>
          <p>Unlimited creative prompting is possible, but real image generation needs fair usage limits because API/GPU costs money.</p>
        </div>
      </div>
    </section>

  </main>

  <footer>
    <h2>ImagineArt AI</h2>
    <p>
      Free AI Image Generator, Image-to-Image AI Tool, Prompt Enhancer, and AI Art Gallery.
    </p>

    <div class="footer-links">
      <a href="#">About</a>
      <a href="#">Contact</a>
      <a href="#">Privacy Policy</a>
      <a href="#">Terms</a>
      <a href="#">Free AI Image Generator</a>
      <a href="#">Image to Image AI</a>
    </div>
  </footer>

  <script>
    function enhancePrompt() {
      const promptInput = document.getElementById("promptInput");
      const style = document.getElementById("styleSelect").value;

      if (!promptInput.value.trim()) {
        alert("Please enter a prompt first.");
        return;
      }

      promptInput.value =
        promptInput.value +
        ", " +
        style +
        ", high quality, ultra detailed, cinematic lighting, beautiful composition, sharp focus, professional AI artwork, no text, no watermark, clean background";
    }

    function generateImage() {
      const prompt = document.getElementById("promptInput").value;
      const style = document.getElementById("styleSelect").value;
      const ratio = document.getElementById("ratioSelect").value;
      const quality = document.getElementById("qualitySelect").value;
      const count = Number(document.getElementById("countSelect").value);
      const resultGrid = document.getElementById("resultGrid");
      const galleryGrid = document.getElementById("galleryGrid");
      const loadingText = document.getElementById("loadingText");

      if (!prompt.trim()) {
        alert("Please enter a prompt.");
        return;
      }

      loadingText.style.display = "block";
      resultGrid.innerHTML = "";

      setTimeout(() => {
        loadingText.style.display = "none";

        galleryGrid.innerHTML = "";

        for (let i = 1; i <= count; i++) {
          const imageText = prompt.slice(0, 40) + "...";

          const card = document.createElement("div");
          card.className = "result-card";
          card.innerHTML = `
            <div class="fake-image">
              AI Image Preview<br>
              ${style}<br>
              ${ratio}
            </div>
            <p><strong>Prompt:</strong> ${imageText}</p>
            <p><strong>Quality:</strong> ${quality}</p>
            <button class="btn secondary" onclick="downloadDemo()">Download</button>
            <button class="btn secondary" onclick="copyPrompt('${encodeURIComponent(prompt)}')">Copy Prompt</button>
          `;

          resultGrid.appendChild(card);

          const galleryCard = card.cloneNode(true);
          galleryGrid.appendChild(galleryCard);
        }

        alert("Demo image created. Connect your API to generate real AI images.");
      }, 1500);
    }

    function previewImage(event) {
      const file = event.target.files[0];
      const preview = document.getElementById("uploadedPreview");

      if (!file) return;

      const validTypes = ["image/jpeg", "image/png", "image/webp"];

      if (!validTypes.includes(file.type)) {
        alert("Please upload JPG, PNG, or WebP image.");
        return;
      }

      preview.src = URL.createObjectURL(file);
      preview.style.display = "block";
    }

    function transformImage() {
      const fileInput = document.getElementById("imageUpload");
      const prompt = document.getElementById("transformPrompt").value;
      const style = document.getElementById("transformStyle").value;
      const strength = document.getElementById("strengthSelect").value;
      const result = document.getElementById("transformResult");

      if (!fileInput.files[0]) {
        alert("Please upload an image.");
        return;
      }

      if (!prompt.trim()) {
        alert("Please enter a transformation prompt.");
        return;
      }

      result.innerHTML = `
        <div class="result-card">
          <div class="fake-image">
            Transformed Image Preview<br>
            ${style}<br>
            Strength: ${strength}
          </div>
          <p><strong>Transformation:</strong> ${prompt}</p>
          <button class="btn secondary" onclick="downloadDemo()">Download</button>
        </div>
      `;

      alert("Demo transformation created. Connect your image-to-image API for real results.");
    }

    function copyPrompt(encodedPrompt) {
      const prompt = decodeURIComponent(encodedPrompt);
      navigator.clipboard.writeText(prompt);
      alert("Prompt copied.");
    }

    function downloadDemo() {
      alert("This is demo mode. After connecting API, real images can be downloaded.");
    }
  </script>

</body>
</html>
