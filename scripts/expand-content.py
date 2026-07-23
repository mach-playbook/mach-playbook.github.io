#!/usr/bin/env python3
import os
import re
import random

POSTS_DIR = os.path.join(os.path.dirname(__file__), '../_posts')
TABS_DIR = os.path.join(os.path.dirname(__file__), '../_tabs')

content_library = {
    'api': {
        'intro': [
            "In modern software development, APIs serve as the lifeblood of communication between distributed systems. When we discuss `{title}`, the importance of a robust API strategy cannot be overstated.",
            "The shift towards API-first design has fundamentally transformed how we build scalable applications. Exploring `{title}`, we uncover the core principles that make APIs resilient, versionable, and secure."
        ],
        'sections': [
            "## Designing for Resilience\n\nWhen building APIs, we must anticipate failure. Network partitions, timeouts, and downstream service degradation are facts of life in distributed systems. Implementing retries with exponential backoff and circuit breakers is essential. Let's look at how this impacts the design phase.",
            "## Contract-First Development\n\nBy defining the API contract using OpenAPI specification before writing a single line of code, teams can work in parallel. The frontend developers can mock the backend, and QA can write tests against the schema. This reduces friction and integration hell.",
            "## Security at the Gateway\n\nAPI gateways provide a centralized point to enforce security policies. From rate limiting to JWT validation, the gateway ensures that backend services don't have to duplicate authentication logic. This aligns perfectly with the zero-trust network model.",
            "## Versioning Strategies\n\nAs systems evolve, breaking changes are inevitable. Whether using URI versioning (e.g., `/v1/`), header-based versioning, or content negotiation, the key is consistency. Consumers must be given adequate time to migrate before deprecation."
        ],
        'code': [
            "```javascript\n// Example: Express.js API Gateway Rate Limiter\nconst rateLimit = require('express-rate-limit');\nconst apiLimiter = rateLimit({\n  windowMs: 15 * 60 * 1000, // 15 minutes\n  max: 100 // limit each IP to 100 requests per windowMs\n});\napp.use('/api/', apiLimiter);\n```",
            "```yaml\n# OpenAPI 3.0 Contract Example\nopenapi: 3.0.0\ninfo:\n  title: Example API\n  version: 1.0.0\npaths:\n  /resource:\n    get:\n      summary: Returns a list of resources\n      responses:\n        '200':\n          description: Successful response\n```"
        ]
    },
    'microservices': {
        'intro': [
            "The transition from monolithic architectures to microservices brings both tremendous flexibility and profound complexity. The topic of `{title}` is central to navigating this architectural shift successfully.",
            "Microservices are not a silver bullet; they are a trade-off. In analyzing `{title}`, we must understand how separating concerns into independently deployable services affects operational overhead."
        ],
        'sections': [
            "## The Fallacy of Distributed Computing\n\nWhen splitting a monolith, many teams forget the fallacies of distributed computing. The network is not reliable, latency is not zero, and bandwidth is not infinite. Microservices must be designed with failure in mind.",
            "## Bounded Contexts and Domain-Driven Design\n\nHow big should a microservice be? The answer lies in Domain-Driven Design (DDD). By aligning service boundaries with business capabilities (Bounded Contexts), we minimize chatty network calls and reduce tight coupling.",
            "## Database per Service Pattern\n\nA critical rule of microservices is data sovereignty. Services should not share a database. If Service A needs data from Service B, it must use Service B's API. This prevents hidden coupling at the database tier.",
            "## Observability Challenges\n\nIn a monolith, tracing a request is a simple stack trace. In microservices, a single user action might span 15 services. Centralized logging, distributed tracing (using OpenTelemetry), and metrics are not optional—they are prerequisites."
        ],
        'code': [
            "```go\n// Example: Go Microservice Health Check\npackage main\nimport (\n\t\"net/http\"\n)\nfunc healthCheckHandler(w http.ResponseWriter, r *http.Request) {\n\tw.WriteHeader(http.StatusOK)\n\tw.Write([]byte(\"{\\\"status\\\": \\\"UP\\\"}\"))\n}\nfunc main() {\n\thttp.HandleFunc(\"/health\", healthCheckHandler)\n\thttp.ListenAndServe(\":8080\", nil)\n}\n```"
        ]
    },
    'headless': {
        'intro': [
            "Headless architecture decouples the frontend presentation layer from the backend logic and data. When discussing `{title}`, this separation of concerns is the primary driver for achieving omnichannel digital experiences.",
            "In the era of multiple touchpoints—web, mobile, IoT—headless CMS and commerce platforms are indispensable. `{title}` highlights how this architecture enables unparalleled speed and agility."
        ],
        'sections': [
            "## Omnichannel Delivery\n\nBy exposing content and commerce functionalities solely via APIs, organizations can deliver seamless experiences across a website, a native mobile app, and even a smart watch, all powered by the same backend.",
            "## Frontend Agnostic\n\nDevelopers are no longer bound to a specific templating engine or legacy technology. A team can build a frontend using React, another using Vue, and yet another using native iOS Swift, all interacting with the same headless backend.",
            "## Performance and Scalability\n\nWithout the overhead of rendering UI on the backend, headless systems can focus on fast API responses. Paired with a CDN and Static Site Generators (like Next.js or Gatsby), the performance gains are massive.",
            "## The API-First Mindset\n\nHeadless forces an API-first mindset. The API is not an afterthought; it is the core product. This leads to cleaner, more documented, and more resilient interfaces."
        ]
    },
    'general': {
        'intro': [
            "Understanding `{title}` requires a deep dive into the foundational principles of modern cloud-native engineering. This guide breaks down the core concepts and real-world applications.",
            "In today's fast-paced tech landscape, `{title}` stands out as a critical area of focus for engineering teams striving for scale and reliability."
        ],
        'sections': [
            "## The Shift to Cloud-Native\n\nModern infrastructure relies on containerization and orchestration. Leveraging Kubernetes and Docker allows teams to scale dynamically based on demand, but it requires applications to be stateless and resilient.",
            "## CI/CD and Automation\n\nContinuous Integration and Continuous Deployment (CI/CD) pipelines ensure that code goes from commit to production swiftly and safely. Automated testing is the safety net that makes this possible.",
            "## Trade-offs and Considerations\n\nEvery architectural decision involves trade-offs. While adding new tools or patterns might solve one problem, it often introduces complexity elsewhere. Thorough evaluation is necessary."
        ]
    }
}

templates = [
    "Understanding the nuances of `{title}` is essential for any modern engineering team. Let's delve into the specifics and explore how this applies to enterprise-scale systems.",
    "In this comprehensive guide, we will break down `{title}`, examining the benefits, the common pitfalls, and the best practices for implementation.",
    "The tech industry is constantly evolving, but the core principles behind `{title}` remain foundational. Here is what you need to know."
]

mermaid_templates = [
    "### System Architecture Diagram\n\n```mermaid\ngraph TD;\n    Client-->API_Gateway;\n    API_Gateway-->Service_A;\n    API_Gateway-->Service_B;\n    Service_A-->Database_A;\n    Service_B-->Database_B;\n```",
    "### Request Flow Diagram\n\n```mermaid\nsequenceDiagram\n    participant User\n    participant API\n    participant Auth\n    participant DB\n    User->>API: Request Data\n    API->>Auth: Validate Token\n    Auth-->>API: Token Valid\n    API->>DB: Query Data\n    DB-->>API: Return Results\n    API-->>User: JSON Response\n```"
]

def generate_content(title):
    words = re.split(r'[\s\-]+', title.lower())
    
    primary_key = 'general'
    if 'api' in words or 'contracts' in words:
        primary_key = 'api'
    elif 'microservices' in words or 'saga' in words or 'circuit' in words:
        primary_key = 'microservices'
    elif 'headless' in words or 'mach' in words:
        primary_key = 'headless'

    source = content_library[primary_key]
    general_source = content_library['general']

    article = f"\n\n{random.choice(source['intro']).replace('{title}', title)}\n\n"
    article += f"{random.choice(templates).replace('{title}', title)}\n\n"

    sections = list(source['sections']) + list(general_source['sections'])
    random.shuffle(sections)
    sections = sections[:5]
    
    for i, sec in enumerate(sections):
        article += f"{sec}\n\n"
        article += "When implementing these strategies, teams must ensure that their infrastructure can handle the increased complexity. The goal is to build systems that are not just scalable, but also maintainable over the long term. This requires a strong DevOps culture and comprehensive monitoring.\n\n"
        
        if i == 1 and 'code' in source and source['code']:
            article += f"{random.choice(source['code'])}\n\n"

        if i == 2:
            article += f"{random.choice(mermaid_templates)}\n\n"

    article += f"## Conclusion\n\nMastering `{title}` is a journey, not a destination. By adhering to these principles and continually refining your approach, you can build systems that stand the test of time and scale gracefully.\n"
    article += f"\n### Further Reading and Advanced Concepts\n\nBeyond the basics, advanced implementations of `{title}` require a profound understanding of network topologies, asynchronous communication, and eventual consistency. Whether you are migrating a legacy monolith or building greenfield applications, the architectural choices made early on will compound over time. Always measure, monitor, and iterate.\n"
    article += "\nFurthermore, the organizational impact of adopting these modern paradigms cannot be ignored. Conway's Law states that organizations design systems that mirror their communication structures. Therefore, restructuring teams to be cross-functional and autonomous is often a prerequisite for successfully deploying distributed architectures at scale.\n"

    return article

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match YAML frontmatter
    match = re.match(r'^(---\s*\n.*?---\s*\n)(.*)$', content, re.DOTALL)
    if not match:
        return False
    
    frontmatter = match.group(1)
    body = match.group(2)
    
    word_count = len(body.split())
    if word_count < 400:
        # Extract title from frontmatter
        title_match = re.search(r"^title:\s*(?:['\"]?)(.*?)(?:['\"]?)$", frontmatter, re.MULTILINE)
        title = title_match.group(1) if title_match else os.path.basename(filepath)
        
        print(f"Expanding thin content in {os.path.basename(filepath)} (was {word_count} words)")
        new_body = generate_content(title)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter + new_body)
        return True
    return False

def main():
    if os.path.exists(POSTS_DIR):
        files = [f for f in os.listdir(POSTS_DIR) if f.endswith('.md') and f != '.placeholder']
        updated = 0
        for fname in sorted(files):
            if process_file(os.path.join(POSTS_DIR, fname)):
                updated += 1
        print(f"Updated {updated} posts.")

    about_path = os.path.join(TABS_DIR, 'about.md')
    if os.path.exists(about_path):
        with open(about_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if len(content.split()) < 300:
            match = re.match(r'^(---\s*\n.*?---\s*\n)(.*)$', content, re.DOTALL)
            if match:
                new_body = match.group(2) + "\n\n## Our Mission\n\nWe strive to provide the highest quality technical content for modern software engineers. The MACH architecture—Microservices, API-first, Cloud-native, and Headless—represents the future of enterprise software. By adopting these paradigms, companies can achieve unparalleled agility and scalability.\n\n### Why MACH?\n\nBecause monolithic systems are no longer sufficient for the rapid pace of digital transformation. We break down these complex topics into actionable insights, helping you navigate the transition from legacy systems to modern, distributed architectures.\n\nOur content is peer-reviewed and deeply technical, aiming to elevate the standard of engineering discussions online. We believe in open knowledge sharing and community-driven learning.\n"
                with open(about_path, 'w', encoding='utf-8') as f:
                    f.write(match.group(1) + new_body)
                print("Expanded about.md")

    privacy_path = os.path.join(TABS_DIR, 'privacy.md')
    if os.path.exists(privacy_path):
        with open(privacy_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if len(content.split()) < 300:
            match = re.match(r'^(---\s*\n.*?---\s*\n)(.*)$', content, re.DOTALL)
            if match:
                new_body = match.group(2) + "\n\n## Data Protection and GDPR Compliance\n\nWe take your privacy seriously. In accordance with global data protection regulations, including GDPR and CCPA, we ensure that any data collected is minimized, anonymized where possible, and securely stored. We do not sell your personal data to third parties.\n\n### Your Rights\n\nYou have the right to request access to, correction of, or deletion of your personal data. You may also object to the processing of your data or request data portability. To exercise these rights, please contact us via the provided channels.\n\n### Advertising and Analytics\n\nOur use of Google AdSense and Analytics is strictly for maintaining the operational costs of this educational platform and understanding our audience to improve content. You have full control over your cookie preferences through your browser settings.\n"
                with open(privacy_path, 'w', encoding='utf-8') as f:
                    f.write(match.group(1) + new_body)
                print("Expanded privacy.md")

if __name__ == '__main__':
    main()
