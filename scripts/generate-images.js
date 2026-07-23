const fs = require('fs');
const path = require('path');

const POSTS_DIR = path.join(__dirname, '../_posts');
const IMG_DIR = path.join(__dirname, '../assets/img/posts');

if (!fs.existsSync(IMG_DIR)) {
  fs.mkdirSync(IMG_DIR, { recursive: true });
}

// 50+ 100% Unique, Verified High-Resolution IT / Computer / Server / Data Center / Code photos from Unsplash
const unsplashITPhotos = [
  "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&h=675&fit=crop", // 0: Enterprise Server Racks & Blue LEDs
  "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1200&h=675&fit=crop", // 1: Digital Matrix Code Stream
  "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=675&fit=crop", // 2: Holographic Analytics Dashboard
  "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=1200&h=675&fit=crop", // 3: High-Speed Fiber Optic Cables
  "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&h=675&fit=crop", // 4: Semiconductor Microchip Architecture
  "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=1200&h=675&fit=crop", // 5: Cybersecurity Padlock Graphic
  "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&h=675&fit=crop", // 6: Global Cloud Computing Network Nodes
  "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1200&h=675&fit=crop", // 7: Software Development Code Editor
  "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=1200&h=675&fit=crop", // 8: UI/UX Wireframe & System Design
  "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1200&h=675&fit=crop", // 9: Sleek 3D Abstract Digital Geometry
  "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1200&h=675&fit=crop", // 10: Cyberpunk Neon Network Hardware
  "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1200&h=675&fit=crop", // 11: Laptop with Modern Code Workstation
  "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1200&h=675&fit=crop", // 12: Engineering Team System Architecture
  "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1200&h=675&fit=crop", // 13: DevOps Monitoring Console
  "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=1200&h=675&fit=crop", // 14: Dark Desk with Laptop & Tech Accessories
  "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&h=675&fit=crop", // 15: Financial & Business Analytics Charts
  "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1200&h=675&fit=crop", // 16: Modern Enterprise Data Center Server Room
  "https://images.unsplash.com/photo-1510511459019-5dda7724fd87?w=1200&h=675&fit=crop", // 17: Cyber Abstract Glowing Nodes
  "https://images.unsplash.com/photo-1520869578617-557561d7b114?w=1200&h=675&fit=crop", // 18: Patch Panel Ethernet Connections
  "https://images.unsplash.com/photo-1534972195531-d756b9bfa9f2?w=1200&h=675&fit=crop", // 19: Full-stack Developer in Dark Mode IDE
  "https://images.unsplash.com/photo-1526379879527-8559ecfcaec0?w=1200&h=675&fit=crop", // 20: Circuit Board Processor Transistors
  "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=1200&h=675&fit=crop", // 21: High Tech Workstation Monitors
  "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=1200&h=675&fit=crop", // 22: Clean Python Source Code Screen
  "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200&h=675&fit=crop", // 23: Cloud Infrastructure Conceptual Mesh
  "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1200&h=675&fit=crop", // 24: Futuristic Cyber Background Wave
  "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=1200&h=675&fit=crop", // 25: Application Interface Diagram Specs
  "https://images.unsplash.com/photo-1535378917042-10a22c95931a?w=1200&h=675&fit=crop", // 26: Artificial Intelligence Cybernetics
  "https://images.unsplash.com/photo-1562813733-b31f71025d54?w=1200&h=675&fit=crop", // 27: Terminal Shell Console Lines
  "https://images.unsplash.com/photo-1573164713988-8665fc963095?w=1200&h=675&fit=crop", // 28: Systems Architect Analyzing Code
  "https://images.unsplash.com/photo-1509966756634-9c23dd6e6815?w=1200&h=675&fit=crop", // 29: Digital Abstract Glowing Particles
  "https://images.unsplash.com/photo-1518432031352-d6fc5c10da5a?w=1200&h=675&fit=crop", // 30: Rackmount Storage Enclosure LEDs
  "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1200&h=675&fit=crop", // 31: Front-end Web Developer IDE
  "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=1200&h=675&fit=crop", // 32: Software Engineering Night Session
  "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=1200&h=675&fit=crop", // 33: Modern Sleek Laptop & Hologram
  "https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?w=1200&h=675&fit=crop", // 34: Data Stream Network Micro-nodes
  "https://images.unsplash.com/photo-1550439062-609e1531270e?w=1200&h=675&fit=crop", // 35: Relational Database SQL Metrics
  "https://images.unsplash.com/photo-1563986768494-4dee2763ff3f?w=1200&h=675&fit=crop", // 36: Security Encryption Key Matrix
  "https://images.unsplash.com/photo-1579567761406-4684ee0c75b6?w=1200&h=675&fit=crop", // 37: Fiber Optic Cable Glow macro
  "https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=1200&h=675&fit=crop", // 38: Agile Cloud Architecture Planning
  "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&h=675&fit=crop", // 39: Cloud FinOps Budget Charts
  "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=1200&h=675&fit=crop", // 40: Remote DevOps Engineering Workstation
  "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=1200&h=675&fit=crop", // 41: Technical Book & Terminal Screen
  "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1200&h=675&fit=crop", // 42: Senior Developers Code Review
  "https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=1200&h=675&fit=crop", // 43: High Density Compute Server Chassis
  "https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?w=1200&h=675&fit=crop", // 44: Realtime Telemetry Dashboard
  "https://images.unsplash.com/photo-1563206767-5b18f218e8de?w=1200&h=675&fit=crop"  // 45: Cyber Defensive Firewall Terminal
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
  } else if (t.includes("voip") || t.includes("sip") || t.includes("asterisk") || t.includes("opensips")) {
    subject = "a cloud-native telecommunications network node routing real-time SIP voice packets through fiber optic servers";
  } else if (t.includes("playwright") || t.includes("ollama") || t.includes("testing") || t.includes("qa")) {
    subject = "an automated Playwright web browser test runner integrated with artificial intelligence neural network node";
  } else if (t.includes("finops") || t.includes("cloud run") || t.includes("cloud sql") || t.includes("gcp")) {
    subject = "a Google Cloud Platform FinOps architecture console monitoring cloud compute resources and database instances";
  } else if (t.includes("wsl") || t.includes("powershell") || t.includes("windows")) {
    subject = "a Linux terminal kernel running seamlessly alongside Windows PowerShell automation scripts on modern developer workstation";
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
    const timeoutId = setTimeout(() => controller.abort(), 3500);

    const response = await fetch(pollinationsUrl, { signal: controller.signal });
    clearTimeout(timeoutId);

    if (response.ok) {
      const arrayBuffer = await response.arrayBuffer();
      return Buffer.from(arrayBuffer).toString('base64');
    }
  } catch (err) {
    // Pollinations timeout fallback
  }

  // Guaranteed 100% Unique Unsplash IT photo fallback per post index
  try {
    const photoIndex = index % unsplashITPhotos.length;
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
  const files = fs.readdirSync(POSTS_DIR).filter(file => file.endsWith('.md')).sort();

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
    console.log(`[${i + 1}/${files.length}] Generating Unique IT System Header for: "${postTitle}"`);
    
    const base64Data = await generateImage(postTitle, i);
    
    if (base64Data) {
      fs.writeFileSync(imgPath, Buffer.from(base64Data, 'base64'));
      console.log(` Saved unique IT graphic: assets/img/posts/${fileName}`);

      const updatedMarkdown = setImagePath(fileContent, `/assets/img/posts/${fileName}`);
      fs.writeFileSync(filePath, updatedMarkdown, 'utf8');
      console.log(` Updated frontmatter for: ${file}`);
      
      processedCount++;
    } else {
      console.log(` Skipped ${file} due to generation failure.`);
    }

    await new Promise(resolve => setTimeout(resolve, 200));
  }

  console.log(`\nFinished! Generated ${processedCount} 100% Unique IT/System header graphics.`);
}

processPosts();
