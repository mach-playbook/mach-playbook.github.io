const fs = require('fs');
const path = require('path');

const POSTS_DIR = path.join(__dirname, '../_posts');
const IMG_DIR = path.join(__dirname, '../assets/img/posts');

if (!fs.existsSync(IMG_DIR)) {
  fs.mkdirSync(IMG_DIR, { recursive: true });
}

// 100% Verified High-Resolution IT / Computer / Server / Code photos from Unsplash (Fallback)
const unsplashITPhotos = [
  "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&h=675&fit=crop", // Enterprise Server Racks & Blue LEDs
  "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1200&h=675&fit=crop", // Digital Matrix Code Stream
  "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=675&fit=crop", // Holographic Analytics Dashboard
  "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=1200&h=675&fit=crop", // High-Speed Fiber Optic Cables
  "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&h=675&fit=crop", // Semiconductor Microchip Architecture
  "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=1200&h=675&fit=crop", // Cybersecurity Padlock Graphic
  "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&h=675&fit=crop", // Global Cloud Computing Network Nodes
  "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1200&h=675&fit=crop", // Software Development Code Editor
  "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=1200&h=675&fit=crop", // UI/UX Wireframe & System Design
  "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1200&h=675&fit=crop", // Sleek 3D Abstract Digital Geometry
  "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1200&h=675&fit=crop", // Cyberpunk Neon Network Hardware
  "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1200&h=675&fit=crop", // Laptop with Modern Code Workstation
  "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&h=675&fit=crop", // Modern Data Center Processing Unit
  "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1200&h=675&fit=crop"  // Engineering Team Designing System Architecture
];

function getITTopicPrompt(title) {
  const t = title.toLowerCase();
  let subject = "";

  if (t.includes("security") || t.includes("oauth") || t.includes("jwt") || t.includes("rate limit")) {
    subject = "a high-tech cybersecurity vault with glowing digital padlock, cryptographic authentication shields, and dark metallic server hardware";
  } else if (t.includes("saga") || t.includes("cqrs") || t.includes("transaction") || t.includes("event")) {
    subject = "an asynchronous event stream topology with glowing message queues, Kafka event bus, and database node cluster in dark space";
  } else if (t.includes("api") || t.includes("openapi") || t.includes("rest") || t.includes("contract")) {
    subject = "an isometric 3D blueprint of API Gateway proxy routing JSON payloads between cloud microservice containers, dark glassmorphism render";
  } else if (t.includes("observability") || t.includes("tracing") || t.includes("metrics") || t.includes("logging")) {
    subject = "a futuristic holographic observability monitoring console displaying OpenTelemetry traces, latency graphs, and system metrics";
  } else if (t.includes("ci/cd") || t.includes("deploy") || t.includes("pipeline") || t.includes("flag")) {
    subject = "an automated DevOps software deployment pipeline with glowing code blocks moving through continuous integration stages";
  } else if (t.includes("headless") || t.includes("cms") || t.includes("omnichannel")) {
    subject = "decoupled headless CMS layers floating in 3D space above glowing glass mobile and web displays";
  } else if (t.includes("nike") || t.includes("sephora") || t.includes("netflix") || t.includes("case study")) {
    subject = "a global high-speed digital commerce cloud network with thousands of microservice transactions and high tech server nodes";
  } else if (t.includes("circuit") || t.includes("bulkhead") || t.includes("strangler")) {
    subject = "a resilient cloud microservice isolation barrier with protective energy shields containing system outages";
  } else if (t.includes("domain") || t.includes("boundary") || t.includes("monolith") || t.includes("granularity")) {
    subject = "a 3D modular cloud architecture with glowing bounded context nodes, microservices topology, sleek studio lighting, Octane render";
  } else {
    subject = "an enterprise data center server rack room with glowing fiber optic cables, ultra detailed IT infrastructure photography";
  }

  return `Professional IT computer system graphic: ${subject}. Dark technological background, ultra high resolution, clean architectural design, no text.`;
}

async function generateImage(title, index) {
  const prompt = getITTopicPrompt(title);
  let hash = 0;
  for (let i = 0; i < title.length; i++) {
    hash = title.charCodeAt(i) + ((hash << 5) - hash);
  }
  const seed = Math.abs(hash) + index * 999;
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
    console.warn(` [IT Fallback] Pollinations paused for "${title.substring(0, 30)}...", using curated Unsplash IT photo.`);
  }

  // Guaranteed IT / System photo fallback from Unsplash
  try {
    const photoIndex = Math.abs(hash) % unsplashITPhotos.length;
    const unsplashUrl = unsplashITPhotos[photoIndex];
    const response = await fetch(unsplashUrl);
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
    console.log(`[${i + 1}/${files.length}] Generating IT System Header for: "${postTitle}"`);
    
    const base64Data = await generateImage(postTitle, i);
    
    if (base64Data) {
      fs.writeFileSync(imgPath, Buffer.from(base64Data, 'base64'));
      console.log(` Saved IT graphic: assets/img/posts/${fileName}`);

      const updatedMarkdown = setImagePath(fileContent, `/assets/img/posts/${fileName}`);
      fs.writeFileSync(filePath, updatedMarkdown, 'utf8');
      console.log(` Updated frontmatter for: ${file}`);
      
      processedCount++;
    } else {
      console.log(` Skipped ${file} due to generation failure.`);
    }

    await new Promise(resolve => setTimeout(resolve, 300));
  }

  console.log(`\nFinished! Generated ${processedCount} 100% IT/System header graphics.`);
}

processPosts();
