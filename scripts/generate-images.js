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

async function generateImage(title, index) {
  const prompt = getTopicPrompt(title);
  let hash = 0;
  for (let i = 0; i < title.length; i++) {
    hash = title.charCodeAt(i) + ((hash << 5) - hash);
  }
  const seed = Math.abs(hash) + index * 777;
  const pollinationsUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=1200&height=675&nologo=true&seed=${seed}`;

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 6000);

    const response = await fetch(pollinationsUrl, { signal: controller.signal });
    clearTimeout(timeoutId);

    if (response.ok) {
      const arrayBuffer = await response.arrayBuffer();
      return Buffer.from(arrayBuffer).toString('base64');
    }
  } catch (err) {
    console.warn(` [Fallback] Pollinations API paused for "${title.substring(0, 30)}...", using high-res visual fallback.`);
  }

  try {
    const picsumSeed = (seed % 900) + 10;
    const picsumUrl = `https://picsum.photos/seed/${picsumSeed}/1200/675`;
    const response = await fetch(picsumUrl);
    if (response.ok) {
      const arrayBuffer = await response.arrayBuffer();
      return Buffer.from(arrayBuffer).toString('base64');
    }
  } catch (err) {
    console.error(" Fallback failed:", err);
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
  const match = content.match(/^(---\r?\n)([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!match) return content;

  let yaml = match[2];
  const body = match[3];

  const lines = yaml.split(/\r?\n/);
  const cleanYamlLines = [];
  let inImageBlock = false;

  for (const line of lines) {
    if (line.trim().startsWith('image:')) {
      inImageBlock = true;
      continue;
    }
    if (inImageBlock) {
      if (line.startsWith(' ') || line.startsWith('\t') || line.trim() === '') {
        continue;
      } else {
        inImageBlock = false;
      }
    }
    cleanYamlLines.push(line);
  }

  cleanYamlLines.push('image:');
  cleanYamlLines.push(`  path: ${imgRelPath}`);

  return `---\n${cleanYamlLines.join('\n')}\n---\n${body}`;
}

async function processPosts() {
  const force = process.argv.includes('--force');
  const fixFrontmatterOnly = process.argv.includes('--fix-frontmatter');
  const files = fs.readdirSync(POSTS_DIR).filter(file => file.endsWith('.md'));

  let processedCount = 0;

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const filePath = path.join(POSTS_DIR, file);
    const fileContent = fs.readFileSync(filePath, 'utf8');

    const fileName = file.replace(/\.md$/, '.png');
    const imgPath = path.join(IMG_DIR, fileName);

    // If just fixing corrupted frontmatter
    if (fixFrontmatterOnly) {
      const updatedMarkdown = setImagePath(fileContent, `/assets/img/posts/${fileName}`);
      fs.writeFileSync(filePath, updatedMarkdown, 'utf8');
      console.log(` Cleaned frontmatter for: ${file}`);
      processedCount++;
      continue;
    }

    const hasImageMeta = fileContent.includes('image:') && fileContent.includes('/assets/img/posts/');

    if (!force && fs.existsSync(imgPath) && hasImageMeta) {
      continue;
    }

    const postTitle = parseTitle(fileContent);
    console.log(`[${i + 1}/${files.length}] Processing header for: "${postTitle}"`);
    
    const base64Data = await generateImage(postTitle, i);
    
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

    await new Promise(resolve => setTimeout(resolve, 300));
  }

  console.log(`\nFinished! Successfully processed ${processedCount} posts.`);
}

processPosts();
