const fs = require('fs');
const path = require('path');

const POSTS_DIR = path.join(__dirname, '../_posts');
const IMG_DIR = path.join(__dirname, '../assets/img/posts');

if (!fs.existsSync(IMG_DIR)) {
  fs.mkdirSync(IMG_DIR, { recursive: true });
}

const styles = [
  "sleek 3D isometric glassmorphism render, dark minimalist background, elegant ambient studio lighting, Octane render 8k",
  "futuristic holographic telemetry UI visualization, dark cyberpunk aesthetic, deep blue and teal tones, high tech interface design",
  "clean modern 3D abstract geometry, translucent floating panels, subtle glowing neon accents, soft shadows, premium tech aesthetic",
  "macro photography of futuristic enterprise cloud hardware, glowing fiber optic cables, ultra detailed, cinematic depth of field",
  "minimalist digital architectural blueprint, floating 3D wireframe models, studio lighting, hyper detailed, 8k resolution",
  "abstract data stream visualization, fluid glowing ribbons of light in dark space, modern corporate technology aesthetic"
];

function getTopicPrompt(title) {
  const t = title.toLowerCase();
  let subject = "";

  if (t.includes("security") || t.includes("oauth") || t.includes("jwt") || t.includes("rate limit")) {
    subject = "a 3D glowing digital cyber security padlock with translucent cryptographic shields and metallic keys";
  } else if (t.includes("saga") || t.includes("cqrs") || t.includes("transaction") || t.includes("event")) {
    subject = "an intricate event-driven data flow network with glowing message streams connecting distributed database nodes";
  } else if (t.includes("api") || t.includes("openapi") || t.includes("rest") || t.includes("contract")) {
    subject = "a sleek 3D API gateway portal with glowing contract blueprints and floating data interfaces";
  } else if (t.includes("observability") || t.includes("tracing") || t.includes("metrics") || t.includes("logging")) {
    subject = "a futuristic holographic dashboard presenting distributed system metrics, telemetry charts, and trace heatmaps";
  } else if (t.includes("ci/cd") || t.includes("deploy") || t.includes("pipeline") || t.includes("flag")) {
    subject = "a high-tech automated software deployment pipeline with glowing code blocks moving through continuous delivery stages";
  } else if (t.includes("headless") || t.includes("cms") || t.includes("omnichannel")) {
    subject = "decoupled digital presentation layers floating in 3D space above multi-device glass displays";
  } else if (t.includes("nike") || t.includes("sephora") || t.includes("netflix") || t.includes("case study")) {
    subject = "a massive global digital storefront network with high-speed transaction streams and independent cloud nodes";
  } else if (t.includes("circuit") || t.includes("bulkhead") || t.includes("strangler")) {
    subject = "a resilient microservice isolation barrier with protective energy shields containing system failures";
  } else if (t.includes("domain") || t.includes("boundary") || t.includes("monolith") || t.includes("granularity")) {
    subject = "modular 3D architectural building blocks separating complex monoliths into clean bounded context domains";
  } else {
    subject = "an advanced cloud-native microservice topology with interconnected distributed nodes and low-latency network paths";
  }

  let hash = 0;
  for (let i = 0; i < title.length; i++) {
    hash = title.charCodeAt(i) + ((hash << 5) - hash);
  }
  const styleIndex = Math.abs(hash) % styles.length;
  const style = styles[styleIndex];

  return `Professional header graphic for an architectural article about ${title}: ${subject}. Style: ${style}. High resolution, clean composition, hyperrealistic, no text.`;
}

async function generateImage(title, retries = 4) {
  const prompt = getTopicPrompt(title);
  const seed = Math.floor(Math.random() * 10000000);
  const url = `https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=1200&height=675&nologo=true&seed=${seed}`;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await fetch(url);

      if (response.status === 429) {
        console.warn(` Rate limit hit (429). Retrying attempt ${attempt}/${retries} after ${6 * attempt}s...`);
        await new Promise(r => setTimeout(r, 6000 * attempt));
        continue;
      }

      if (!response.ok) {
        console.error(` Image generation failed (${response.status}):`, response.statusText);
        if (attempt < retries) {
          await new Promise(r => setTimeout(r, 4000));
          continue;
        }
        return null;
      }

      const arrayBuffer = await response.arrayBuffer();
      return Buffer.from(arrayBuffer).toString('base64');
    } catch (error) {
      console.error(" Fetch error:", error.message || error);
      if (attempt < retries) {
        await new Promise(r => setTimeout(r, 4000));
      }
    }
  }
  return null;
}

function parseTitle(content) {
  const multilineMatch = content.match(/^title:\s*>-\r?\n\s+(.+)$/m);
  if (multilineMatch) {
    return multilineMatch[1].trim();
  }
  const titleMatch = content.match(/^title:\s*['"]?(.*?)['"]?\s*$/m);
  if (titleMatch && titleMatch[1] && titleMatch[1] !== '>-') {
    return titleMatch[1].trim();
  }
  return 'technology microservices';
}

function setImagePath(content, imgRelPath) {
  if (content.includes('image:')) {
    return content.replace(/image:\s*\n\s*path:\s*.*/, `image:\n  path: ${imgRelPath}`);
  } else {
    return content.replace(/^(---\r?\n)/, `$1image:\n  path: ${imgRelPath}\n`);
  }
}

async function processPosts() {
  const force = process.argv.includes('--force');
  const files = fs.readdirSync(POSTS_DIR).filter(file => file.endsWith('.md'));

  let processedCount = 0;

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const filePath = path.join(POSTS_DIR, file);
    const fileContent = fs.readFileSync(filePath, 'utf8');

    const fileName = file.replace(/\.md$/, '.png');
    const imgPath = path.join(IMG_DIR, fileName);
    const hasImageMeta = fileContent.includes('image:') && fileContent.includes('/assets/img/posts/');

    if (!force && fs.existsSync(imgPath) && hasImageMeta) {
      continue;
    }

    const postTitle = parseTitle(fileContent);
    console.log(`[${i + 1}/${files.length}] Generating unique header for: "${postTitle}"`);
    
    const base64Data = await generateImage(postTitle);
    
    if (base64Data) {
      fs.writeFileSync(imgPath, Buffer.from(base64Data, 'base64'));
      console.log(` Saved: assets/img/posts/${fileName}`);

      const updatedMarkdown = setImagePath(fileContent, `/assets/img/posts/${fileName}`);
      fs.writeFileSync(filePath, updatedMarkdown, 'utf8');
      console.log(` Updated frontmatter for: ${file}`);
      
      processedCount++;
    } else {
      console.log(` Skipped ${file} due to generation failure.`);
    }

    // 4 second delay between requests to respect rate limits
    await new Promise(resolve => setTimeout(resolve, 4000));
  }

  console.log(`\nFinished! Generated ${processedCount} distinct topic images.`);
}

processPosts();
