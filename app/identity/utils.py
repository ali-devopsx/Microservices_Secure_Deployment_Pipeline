"""
Utility functions for the Identity Portfolio app.
Contains helper functions like populate_default_data for seeding the database with default values.
"""

from .models import Profile, Skill, Project, TimelineEvent


def populate_default_data():
    """
    Populate the database with default portfolio data if it doesn't already exist.
    This function uses get_or_create to ensure data is only inserted once.
    Called on app startup (in apps.py) and on each view request as a safety measure.
    
    Defaults included:
    - One Profile record with Ali Mahmoud's information
    - 10 Skill records with various technologies
    - 3 Project records with descriptions and tech stacks
    - 4 TimelineEvent records marking career milestones
    """

    # ===== PROFILE DATA =====
    # Create or get the single Profile record
    Profile.objects.get_or_create(
        pk=1,
        defaults={
            'name': 'Ali Mahmoud',
            'title': 'Penetration Tester & Automation Engineer',
            'subtitle': 'IT Linux Engineer | DevOps Engineer | Cybersecurity Analyst',
            'bio_strong': 'I build calm, resilient systems that balance security and operations.',
            'journey': 'My path blends Linux engineering, DevOps automation, and practical cybersecurity.\nI help teams build secure infrastructure that feels smart and stable.',
            'email': 'ali@example.com',
            'logo_text': 'AM',
            'contact_phrase': 'Let\'s connect by email:',
            'youtube_url': '',
            'facebook_url': '',
            'github_url': 'https://github.com',
            'linkedin_url': 'https://linkedin.com',
        }
    )

    # ===== SKILLS DATA =====
    # Define all skills with their FontAwesome icons and display order
    skills_data = [
        {'name': 'IT Infrastructure', 'icon_class': 'fa-network-wired', 'order': 1},
        {'name': 'Linux (Kali, Ubuntu, RHEL)', 'icon_class': 'fa-linux', 'order': 2},
        {'name': 'Networking (TCP/IP, Firewalls, Wireshark)', 'icon_class': 'fa-globe', 'order': 3},
        {'name': 'DevOps', 'icon_class': 'fa-cogs', 'order': 4},
        {'name': 'Git & GitFlow', 'icon_class': 'fa-git-alt', 'order': 5},
        {'name': 'GitHub Actions', 'icon_class': 'fa-github', 'order': 6},
        {'name': 'Docker & Podman', 'icon_class': 'fa-docker', 'order': 7},
        {'name': 'Kubernetes (k8s)', 'icon_class': 'fa-cloud', 'order': 8},
        {'name': 'Python / Bash', 'icon_class': 'fa-python', 'order': 9},
        {'name': 'SIEM (Splunk, ELK)', 'icon_class': 'fa-chart-line', 'order': 10},
    ]

    # Create each skill if it doesn't already exist
    for skill_data in skills_data:
        Skill.objects.get_or_create(
            name=skill_data['name'],
            defaults={
                'icon_class': skill_data['icon_class'],
                'order': skill_data['order'],
            }
        )

    # ===== PROJECTS DATA =====
    # Define all projects with descriptions, tech stacks, and display order
    projects_data = [
        {
            'title': 'Threat-Hunter ELK Stack',
            'description': 'Built an open-source threat analysis platform using Elastic Stack with real-time attack dashboards.',
            'tech_stack': 'ELK, Docker, Python, Suricata',
            'summary': 'Tech: ELK, Docker, Python',
            'github_url': 'https://github.com/example/threat-hunter-elk',
            'order': 1,
        },
        {
            'title': 'CI/CD Security Pipeline',
            'description': 'Designed a GitHub Actions pipeline that scans for vulnerabilities before deployment, integrated with Snyk & Trivy.',
            'tech_stack': 'GitHub Actions, Docker, Snyk, Trivy',
            'summary': 'Result: Secure deployment gates with static analysis.',
            'github_url': 'https://github.com/example/cicd-security-pipeline',
            'order': 2,
        },
        {
            'title': 'Red Team Automation Tool',
            'description': 'Bash/Python tool to automate internal network penetration testing, supporting Windows and Linux targets.',
            'tech_stack': 'Bash, Python, Metasploit API',
            'summary': 'Built automation for repeatable red-team workflows.',
            'github_url': 'https://github.com/example/red-team-tool',
            'order': 3,
        },
    ]

    # Create each project if it doesn't already exist
    for project_data in projects_data:
        Project.objects.get_or_create(
            title=project_data['title'],
            defaults={
                'description': project_data['description'],
                'tech_stack': project_data['tech_stack'],
                'order': project_data['order'],
            }
        )

    # ===== TIMELINE EVENTS DATA =====
    # Define career timeline events in chronological order
    timeline_data = [
        {
            'year': 2018,
            'title': 'Beginning of Passion',
            'description': 'Discovered an XSS vulnerability in a university site and received my first acknowledgment.',
            'order': 1,
        },
        {
            'year': 2020,
            'title': 'Certified Ethical Hacker (CEH)',
            'description': 'Passed the exam and started working as a Junior Pentester.',
            'order': 2,
        },
        {
            'year': 2022,
            'title': 'Merging Security with DevOps',
            'description': 'Became responsible for DevSecOps in a team, building the first secure pipeline.',
            'order': 3,
        },
        {
            'year': 2024,
            'title': 'Present: Automating Attacks & Defense',
            'description': 'Developing offensive and defensive automation tools using Python and GitHub Actions.',
            'order': 4,
        },
    ]

    # Create each timeline event if it doesn't already exist
    for timeline_event_data in timeline_data:
        TimelineEvent.objects.get_or_create(
            year=timeline_event_data['year'],
            title=timeline_event_data['title'],
            defaults={
                'description': timeline_event_data['description'],
                'order': timeline_event_data['order'],
            }
        )
