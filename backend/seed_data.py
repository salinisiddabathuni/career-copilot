import requests

API_URL = "http://127.0.0.1:8000/opportunities"

opportunities = [
    {
        "type": "hackathon",
        "title": "Smart India Hackathon 2026",
        "source": "unstop",
        "skills_required": ["Python", "React", "AI/ML"],
        "deadline": "2026-09-20",
        "url": "https://unstop.com/example-link"
    },
    {
        "type": "internship",
        "title": "Software Engineering Intern",
        "source": "internshala",
        "skills_required": ["Java", "SQL", "REST APIs"],
        "deadline": "2026-09-10",
        "url": "https://internshala.com/example-link"
    },
    # add your remaining 8-13 real entries here, same format
    {
        "type": "internship",
        "title": "Figma Designer Internship",
        "source": "unstop",
        "skills_required": ["Python", "React", "AI/ML","HTML","CSS"],
        "deadline": "2026-09-20",
        "url": "https://unstop.com/example-link"
    },
    {
        "type": "hackathon",
        "title": "ET AI Hackathon 2.0",
        "source": "unstop",
        "skills_required": ["Applied AI", "Prototyping", "Python"],
        "deadline": "2026-09-30",
        "url": "https://unstop.com"
    },
    {
        "type": "hackathon",
        "title": "ZeroBreach CTF 2026",
        "source": "unstop",
        "skills_required": ["Cybersecurity", "Cryptography", "Reverse Engineering"],
        "deadline": "2026-09-05",
        "url": "https://unstop.com"
    },
    {
        "type": "hackathon",
        "title": "Open Source Hackathon",
        "source": "devfolio",
        "skills_required": ["Git", "GitHub", "Open Source", "Documentation"],
        "deadline": "2026-09-10",
        "url": "https://devfolio.co"
    },
    {
        "type": "hackathon",
        "title": "HSBC Technology India Hackathon",
        "source": "unstop",
        "skills_required": ["Java", "Cloud", "Fintech", "APIs"],
        "deadline": "2026-09-20",
        "url": "https://unstop.com"
    },
    {
        "type": "internship",
        "title": "Full Stack Developer Intern",
        "source": "internshala",
        "skills_required": ["React", "Node.js", "MongoDB", "REST APIs"],
        "deadline": "2026-09-25",
        "url": "https://internshala.com"
    },
    {
        "type": "internship",
        "title": "AI/ML Intern",
        "source": "internshala",
        "skills_required": ["Python", "TensorFlow", "Data Analysis"],
        "deadline": "2026-09-18",
        "url": "https://internshala.com"
    },
    {
        "type": "internship",
        "title": "Cloud Engineering Intern",
        "source": "internshala",
        "skills_required": ["AWS", "Docker", "CI/CD"],
        "deadline": "2026-10-01",
        "url": "https://internshala.com"
    },
    

    
]

for opp in opportunities:
    response = requests.post(API_URL, json=opp)
    if response.status_code == 200:
        print(f"Added: {opp['title']}")
    else:
        print(f"Failed: {opp['title']} — {response.text}")