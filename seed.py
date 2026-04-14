"""
AmpUp Skill — Database Seed Script
Run this to populate the database with course content.
Usage: python seed.py
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tracks.db")


def seed():
    """Seed the database with tracks, phases, and lectures."""
    # Remove old db if exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables from schema
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
    with open(schema_path, "r") as f:
        cur.executescript(f.read())

    # =========================================================================
    # TRACKS
    # =========================================================================
    tracks = [
        (
            "blockchain",
            "Blockchain Development",
            "Master blockchain fundamentals, Solidity smart contracts, DeFi protocols, and Web3 development from scratch.",
            "🔗",
            "#f59e0b",
            "https://roadmap.sh/blockchain",
        ),
        (
            "backend",
            "Backend Engineering",
            "Learn server-side development, RESTful APIs, database design, authentication, and scalable system architecture.",
            "⚙️",
            "#3b82f6",
            "https://roadmap.sh/backend",
        ),
        (
            "devops",
            "DevOps Engineering",
            "Master Linux, containerization with Docker, CI/CD pipelines, cloud infrastructure, and infrastructure as code.",
            "🚀",
            "#10b981",
            "https://roadmap.sh/devops",
        ),
        (
            "ml",
            "Machine Learning",
            "Build a strong foundation in mathematics, Python ML libraries, deep learning, and real-world AI projects.",
            "🧠",
            "#8b5cf6",
            "https://roadmap.sh/ai-data-scientist",
        ),
    ]

    for t in tracks:
        cur.execute(
            "INSERT INTO tracks (slug, name, description, icon, color, roadmap_url) VALUES (?, ?, ?, ?, ?, ?)",
            t,
        )

    conn.commit()

    # =========================================================================
    # BLOCKCHAIN TRACK
    # =========================================================================
    blockchain_id = cur.execute("SELECT id FROM tracks WHERE slug='blockchain'").fetchone()[0]

    blockchain_phases = [
        (blockchain_id, 1, "Blockchain Fundamentals"),
        (blockchain_id, 2, "Solidity & Smart Contracts"),
        (blockchain_id, 3, "DeFi & Advanced Concepts"),
        (blockchain_id, 4, "Full-Stack Web3 Projects"),
    ]
    for p in blockchain_phases:
        cur.execute("INSERT INTO phases (track_id, phase_number, title) VALUES (?, ?, ?)", p)
    conn.commit()

    bc_p1 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=1", (blockchain_id,)).fetchone()[0]
    bc_p2 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=2", (blockchain_id,)).fetchone()[0]
    bc_p3 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=3", (blockchain_id,)).fetchone()[0]
    bc_p4 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=4", (blockchain_id,)).fetchone()[0]

    blockchain_lectures = [
        # Phase 1: Fundamentals
        (bc_p1, 1, "What is Blockchain? Full Introduction", "https://www.youtube.com/watch?v=SSo_EIwHSd4", "SSo_EIwHSd4", "25:30", '["https://ethereum.org/en/developers/docs/"]'),
        (bc_p1, 2, "How Does Bitcoin Work? (Technical)", "https://www.youtube.com/watch?v=bBC-nXj3Ng4", "bBC-nXj3Ng4", "26:21", '["https://bitcoin.org/bitcoin.pdf"]'),
        (bc_p1, 3, "Blockchain Demo — Visual Explanation", "https://www.youtube.com/watch?v=_160oMzblY8", "_160oMzblY8", "17:49", '["https://andersbrownworth.com/blockchain/"]'),
        (bc_p1, 4, "Ethereum Explained Simply", "https://www.youtube.com/watch?v=jxLkbJozKbY", "jxLkbJozKbY", "20:15", '["https://ethereum.org/en/what-is-ethereum/"]'),

        # Phase 2: Solidity & Smart Contracts
        (bc_p2, 1, "Solidity Tutorial — Full Course (Part 1)", "https://www.youtube.com/watch?v=umepbfKp5rI", "umepbfKp5rI", "1:45:00", '["https://docs.soliditylang.org/"]'),
        (bc_p2, 2, "Build Your First Smart Contract", "https://www.youtube.com/watch?v=coQ5dg8wM2o", "coQ5dg8wM2o", "32:10", '["https://remix.ethereum.org/"]'),
        (bc_p2, 3, "Hardhat & Ethers.js Development Setup", "https://www.youtube.com/watch?v=GKJBEhA8P5Y", "GKJBEhA8P5Y", "45:22", '["https://hardhat.org/docs"]'),
        (bc_p2, 4, "Smart Contract Security Fundamentals", "https://www.youtube.com/watch?v=pUWmJ86X_do", "pUWmJ86X_do", "38:15", '["https://swcregistry.io/"]'),

        # Phase 3: DeFi & Advanced
        (bc_p3, 1, "DeFi Explained — Full Guide", "https://www.youtube.com/watch?v=17QRFlml4pA", "17QRFlml4pA", "28:40", '["https://defipulse.com/"]'),
        (bc_p3, 2, "Build a DEX (Decentralized Exchange)", "https://www.youtube.com/watch?v=qB2Ulx201wY", "qB2Ulx201wY", "1:12:00", '["https://docs.uniswap.org/"]'),
        (bc_p3, 3, "NFTs and ERC-721 Standard", "https://www.youtube.com/watch?v=9yuHz6g_P50", "9yuHz6g_P50", "35:18", '["https://eips.ethereum.org/EIPS/eip-721"]'),

        # Phase 4: Full-Stack Web3 Projects
        (bc_p4, 1, "Full-Stack Web3 Development — Patrick Collins", "https://www.youtube.com/watch?v=gyMwXuJrbJQ", "gyMwXuJrbJQ", "32:00:00", '["https://github.com/smartcontractkit/full-blockchain-solidity-course-js"]'),
        (bc_p4, 2, "Build a Web3 Marketplace (Full Tutorial)", "https://www.youtube.com/watch?v=GKJBEhA8P5Y", "GKJBEhA8P5Y", "2:15:00", '["https://thegraph.com/docs/"]'),
        (bc_p4, 3, "Web3 Portfolio Project Walkthrough", "https://www.youtube.com/watch?v=a0osIaAOFSE", "a0osIaAOFSE", "58:30", '["https://wagmi.sh/"]'),
    ]

    for lec in blockchain_lectures:
        cur.execute(
            "INSERT INTO lectures (phase_id, lecture_number, title, youtube_url, youtube_id, duration, resource_links) VALUES (?, ?, ?, ?, ?, ?, ?)",
            lec,
        )

    conn.commit()

    # =========================================================================
    # BACKEND ENGINEERING TRACK
    # =========================================================================
    backend_id = cur.execute("SELECT id FROM tracks WHERE slug='backend'").fetchone()[0]

    backend_phases = [
        (backend_id, 1, "Programming Fundamentals"),
        (backend_id, 2, "APIs & Web Frameworks"),
        (backend_id, 3, "Databases & Data Modeling"),
        (backend_id, 4, "System Design & Architecture"),
    ]
    for p in backend_phases:
        cur.execute("INSERT INTO phases (track_id, phase_number, title) VALUES (?, ?, ?)", p)
    conn.commit()

    be_p1 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=1", (backend_id,)).fetchone()[0]
    be_p2 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=2", (backend_id,)).fetchone()[0]
    be_p3 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=3", (backend_id,)).fetchone()[0]
    be_p4 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=4", (backend_id,)).fetchone()[0]

    backend_lectures = [
        # Phase 1: Programming Fundamentals
        (be_p1, 1, "Python Full Course for Beginners", "https://www.youtube.com/watch?v=_uQrJ0TkZlc", "_uQrJ0TkZlc", "6:14:07", '["https://docs.python.org/3/tutorial/"]'),
        (be_p1, 2, "Data Structures & Algorithms in Python", "https://www.youtube.com/watch?v=pkYVOmU3MgA", "pkYVOmU3MgA", "5:22:00", '["https://realpython.com/python-data-structures/"]'),
        (be_p1, 3, "Git & GitHub Crash Course", "https://www.youtube.com/watch?v=RGOj5yH7evk", "RGOj5yH7evk", "1:08:29", '["https://git-scm.com/book/en/v2"]'),
        (be_p1, 4, "Linux Command Line for Beginners", "https://www.youtube.com/watch?v=ZtqBQ68cfJc", "ZtqBQ68cfJc", "4:19:52", '["https://linuxcommand.org/"]'),

        # Phase 2: APIs & Web Frameworks
        (be_p2, 1, "RESTful APIs Explained", "https://www.youtube.com/watch?v=-MTSQjw5DrM", "-MTSQjw5DrM", "8:21", '["https://restfulapi.net/"]'),
        (be_p2, 2, "Flask Full Tutorial — Build a Web App", "https://www.youtube.com/watch?v=dam0GPOAvVI", "dam0GPOAvVI", "6:58:15", '["https://flask.palletsprojects.com/"]'),
        (be_p2, 3, "Node.js & Express.js Full Course", "https://www.youtube.com/watch?v=Oe421EPjeBE", "Oe421EPjeBE", "8:16:48", '["https://expressjs.com/"]'),
        (be_p2, 4, "API Authentication with JWT", "https://www.youtube.com/watch?v=7Q17ubqLfaM", "7Q17ubqLfaM", "27:36", '["https://jwt.io/introduction"]'),

        # Phase 3: Databases
        (be_p3, 1, "SQL Full Course — freeCodeCamp", "https://www.youtube.com/watch?v=HXV3zeQKqGY", "HXV3zeQKqGY", "4:20:37", '["https://www.w3schools.com/sql/"]'),
        (be_p3, 2, "PostgreSQL Tutorial for Beginners", "https://www.youtube.com/watch?v=qw--VYLpxG4", "qw--VYLpxG4", "4:19:24", '["https://www.postgresql.org/docs/"]'),
        (be_p3, 3, "MongoDB Complete Guide", "https://www.youtube.com/watch?v=ofme2o29ngU", "ofme2o29ngU", "1:33:28", '["https://www.mongodb.com/docs/"]'),
        (be_p3, 4, "Database Design & Normalization", "https://www.youtube.com/watch?v=UrYLYV7WSHM", "UrYLYV7WSHM", "3:30:00", '["https://dbdiagram.io/"]'),

        # Phase 4: System Design
        (be_p4, 1, "System Design for Beginners", "https://www.youtube.com/watch?v=MbjObHmDbZo", "MbjObHmDbZo", "39:17", '["https://github.com/donnemartin/system-design-primer"]'),
        (be_p4, 2, "Microservices Explained", "https://www.youtube.com/watch?v=lTAcCNbJ7KE", "lTAcCNbJ7KE", "5:29", '["https://microservices.io/"]'),
        (be_p4, 3, "Caching Strategies & Redis", "https://www.youtube.com/watch?v=jgpVdJB2sKQ", "jgpVdJB2sKQ", "23:38", '["https://redis.io/docs/"]'),
    ]

    for lec in backend_lectures:
        cur.execute(
            "INSERT INTO lectures (phase_id, lecture_number, title, youtube_url, youtube_id, duration, resource_links) VALUES (?, ?, ?, ?, ?, ?, ?)",
            lec,
        )
    conn.commit()

    # =========================================================================
    # DEVOPS TRACK
    # =========================================================================
    devops_id = cur.execute("SELECT id FROM tracks WHERE slug='devops'").fetchone()[0]

    devops_phases = [
        (devops_id, 1, "Linux & Networking"),
        (devops_id, 2, "Containers & Docker"),
        (devops_id, 3, "CI/CD & Automation"),
        (devops_id, 4, "Cloud & Infrastructure as Code"),
    ]
    for p in devops_phases:
        cur.execute("INSERT INTO phases (track_id, phase_number, title) VALUES (?, ?, ?)", p)
    conn.commit()

    do_p1 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=1", (devops_id,)).fetchone()[0]
    do_p2 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=2", (devops_id,)).fetchone()[0]
    do_p3 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=3", (devops_id,)).fetchone()[0]
    do_p4 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=4", (devops_id,)).fetchone()[0]

    devops_lectures = [
        # Phase 1: Linux & Networking
        (do_p1, 1, "Linux for Beginners — Full Course", "https://www.youtube.com/watch?v=sWbUDq4S6Y8", "sWbUDq4S6Y8", "3:26:24", '["https://linuxjourney.com/"]'),
        (do_p1, 2, "Networking Fundamentals — Practical Guide", "https://www.youtube.com/watch?v=qiQR5rTSshw", "qiQR5rTSshw", "1:40:00", '["https://www.cloudflare.com/learning/"]'),
        (do_p1, 3, "Bash Scripting Full Course", "https://www.youtube.com/watch?v=tK9Oc6AEnR4", "tK9Oc6AEnR4", "1:06:30", '["https://www.gnu.org/software/bash/manual/"]'),
        (do_p1, 4, "SSH & Linux Server Administration", "https://www.youtube.com/watch?v=YS5Zh7KExvE", "YS5Zh7KExvE", "46:21", '["https://www.ssh.com/academy/ssh"]'),

        # Phase 2: Containers & Docker
        (do_p2, 1, "Docker Tutorial for Beginners — TechWorld with Nana", "https://www.youtube.com/watch?v=3c-iBn73dDE", "3c-iBn73dDE", "2:46:14", '["https://docs.docker.com/"]'),
        (do_p2, 2, "Docker Compose Full Tutorial", "https://www.youtube.com/watch?v=HG6yIjZapSA", "HG6yIjZapSA", "1:29:00", '["https://docs.docker.com/compose/"]'),
        (do_p2, 3, "Kubernetes Crash Course — TechWorld with Nana", "https://www.youtube.com/watch?v=s_o8dwzRlu4", "s_o8dwzRlu4", "3:36:45", '["https://kubernetes.io/docs/home/"]'),
        (do_p2, 4, "Container Orchestration Explained", "https://www.youtube.com/watch?v=kBF6Bvth0zw", "kBF6Bvth0zw", "15:20", '["https://www.cncf.io/"]'),

        # Phase 3: CI/CD
        (do_p3, 1, "GitHub Actions — Full Tutorial", "https://www.youtube.com/watch?v=R8_veQiYBjI", "R8_veQiYBjI", "3:32:50", '["https://docs.github.com/en/actions"]'),
        (do_p3, 2, "Jenkins Complete Tutorial", "https://www.youtube.com/watch?v=FX322RVNGj4", "FX322RVNGj4", "3:04:27", '["https://www.jenkins.io/doc/"]'),
        (do_p3, 3, "GitOps & ArgoCD Crash Course", "https://www.youtube.com/watch?v=MeU5_k9ssrs", "MeU5_k9ssrs", "1:08:33", '["https://argo-cd.readthedocs.io/"]'),

        # Phase 4: Cloud & IaC
        (do_p4, 1, "AWS Full Course for Beginners", "https://www.youtube.com/watch?v=ulprqHHWlng", "ulprqHHWlng", "3:18:00", '["https://aws.amazon.com/getting-started/"]'),
        (do_p4, 2, "Terraform Full Course — TechWorld with Nana", "https://www.youtube.com/watch?v=7xngnjfIlK4", "7xngnjfIlK4", "2:20:38", '["https://developer.hashicorp.com/terraform/docs"]'),
        (do_p4, 3, "Ansible for Beginners", "https://www.youtube.com/watch?v=1id6ERvfozo", "1id6ERvfozo", "1:04:52", '["https://docs.ansible.com/"]'),
    ]

    for lec in devops_lectures:
        cur.execute(
            "INSERT INTO lectures (phase_id, lecture_number, title, youtube_url, youtube_id, duration, resource_links) VALUES (?, ?, ?, ?, ?, ?, ?)",
            lec,
        )
    conn.commit()

    # =========================================================================
    # MACHINE LEARNING TRACK
    # =========================================================================
    ml_id = cur.execute("SELECT id FROM tracks WHERE slug='ml'").fetchone()[0]

    ml_phases = [
        (ml_id, 1, "Mathematics & Statistics"),
        (ml_id, 2, "Python for Data Science"),
        (ml_id, 3, "Machine Learning Algorithms"),
        (ml_id, 4, "Deep Learning & Neural Networks"),
    ]
    for p in ml_phases:
        cur.execute("INSERT INTO phases (track_id, phase_number, title) VALUES (?, ?, ?)", p)
    conn.commit()

    ml_p1 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=1", (ml_id,)).fetchone()[0]
    ml_p2 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=2", (ml_id,)).fetchone()[0]
    ml_p3 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=3", (ml_id,)).fetchone()[0]
    ml_p4 = cur.execute("SELECT id FROM phases WHERE track_id=? AND phase_number=4", (ml_id,)).fetchone()[0]

    ml_lectures = [
        # Phase 1: Math & Stats
        (ml_p1, 1, "Linear Algebra — Essence of Linear Algebra (3Blue1Brown)", "https://www.youtube.com/watch?v=fNk_zzaMoSs", "fNk_zzaMoSs", "15:09", '["https://www.3blue1brown.com/topics/linear-algebra"]'),
        (ml_p1, 2, "Calculus — Essence of Calculus (3Blue1Brown)", "https://www.youtube.com/watch?v=WUvTyaaNkzM", "WUvTyaaNkzM", "17:04", '["https://www.3blue1brown.com/topics/calculus"]'),
        (ml_p1, 3, "Probability & Statistics Full Course", "https://www.youtube.com/watch?v=xxpc-HPKN28", "xxpc-HPKN28", "9:27:03", '["https://www.khanacademy.org/math/statistics-probability"]'),
        (ml_p1, 4, "Mathematics for Machine Learning (Overview)", "https://www.youtube.com/watch?v=1VSZtNYMntM", "1VSZtNYMntM", "1:07:33", '["https://mml-book.github.io/"]'),

        # Phase 2: Python for Data Science
        (ml_p2, 1, "NumPy Full Tutorial", "https://www.youtube.com/watch?v=QUT1VHiLmmI", "QUT1VHiLmmI", "1:00:05", '["https://numpy.org/doc/stable/"]'),
        (ml_p2, 2, "Pandas Complete Guide", "https://www.youtube.com/watch?v=vmEHCJofslg", "vmEHCJofslg", "1:00:27", '["https://pandas.pydata.org/docs/"]'),
        (ml_p2, 3, "Matplotlib & Data Visualization", "https://www.youtube.com/watch?v=UO98lJQ3QGI", "UO98lJQ3QGI", "1:11:49", '["https://matplotlib.org/stable/tutorials/"]'),
        (ml_p2, 4, "Jupyter Notebooks & Data Analysis Workflow", "https://www.youtube.com/watch?v=HW29067qVWk", "HW29067qVWk", "44:31", '["https://jupyter.org/install"]'),

        # Phase 3: ML Algorithms
        (ml_p3, 1, "Machine Learning Full Course — freeCodeCamp", "https://www.youtube.com/watch?v=NWONeJKn6kc", "NWONeJKn6kc", "9:52:13", '["https://scikit-learn.org/stable/"]'),
        (ml_p3, 2, "Scikit-Learn Full Tutorial", "https://www.youtube.com/watch?v=0B5eIE_1vpU", "0B5eIE_1vpU", "2:09:22", '["https://scikit-learn.org/stable/user_guide.html"]'),
        (ml_p3, 3, "Feature Engineering & Model Selection", "https://www.youtube.com/watch?v=68ABAU_V8qI", "68ABAU_V8qI", "45:00", '["https://www.kaggle.com/learn/feature-engineering"]'),

        # Phase 4: Deep Learning
        (ml_p4, 1, "Deep Learning Full Course — freeCodeCamp", "https://www.youtube.com/watch?v=VyWAvY2CF9c", "VyWAvY2CF9c", "6:13:04", '["https://www.deeplearning.ai/"]'),
        (ml_p4, 2, "Neural Networks Explained (3Blue1Brown)", "https://www.youtube.com/watch?v=aircAruvnKk", "aircAruvnKk", "19:13", '["https://www.3blue1brown.com/topics/neural-networks"]'),
        (ml_p4, 3, "PyTorch Full Tutorial", "https://www.youtube.com/watch?v=c36lUUr864M", "c36lUUr864M", "9:35:27", '["https://pytorch.org/tutorials/"]'),
        (ml_p4, 4, "TensorFlow & Keras Complete Guide", "https://www.youtube.com/watch?v=tPYj3fFJGjk", "tPYj3fFJGjk", "6:52:", '["https://www.tensorflow.org/tutorials"]'),
    ]

    for lec in ml_lectures:
        cur.execute(
            "INSERT INTO lectures (phase_id, lecture_number, title, youtube_url, youtube_id, duration, resource_links) VALUES (?, ?, ?, ?, ?, ?, ?)",
            lec,
        )
    conn.commit()

    # Print summary
    track_count = cur.execute("SELECT COUNT(*) FROM tracks").fetchone()[0]
    phase_count = cur.execute("SELECT COUNT(*) FROM phases").fetchone()[0]
    lecture_count = cur.execute("SELECT COUNT(*) FROM lectures").fetchone()[0]
    print(f"✅ Seeded successfully!")
    print(f"   Tracks: {track_count}")
    print(f"   Phases: {phase_count}")
    print(f"   Lectures: {lecture_count}")

    conn.close()


if __name__ == "__main__":
    seed()
